from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRedirect

from . import services

from .forms import EmailForm


EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def logout_btn_hx_view(request):
    if not request.htmx:
        return redirect('/')
    if request.method == "POST":
        try:
            del request.session['email_id']
        except:
            pass
        email_id_in_session = request.session.get('email_id')
        if not email_id_in_session:
            return HttpResponseClientRedirect('/')
    return render(request, "emails/hx/logout_btn.html", {}) 

def email_token_login_view(request):
    if not request.htmx:
        return redirect('/')
    email_id_in_session = request.session.get('email_id')
    template_name = "emails/hx/form.html"
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
        "show_form": not email_id_in_session,
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = services.start_verification_event(email_val)
        context['form'] = EmailForm()
        context['message'] = f"Succcess! Check your email for verification from {EMAIL_HOST_USER}"
        # return HttpResponseClientRedirect('/check-your-email')
        return render(request, template_name, context)
    else:
        print(form.errors) 
    return render(request, template_name, context)




def verify_email_token_view(request, token, *args, **kwargs):
    did_verify, msg, email = services.verify_token(token)
    if not did_verify:
        try:
            del request.session['email_id']
        except KeyError:
            pass
        messages.error(request, f"Failed to verify token: {msg}")
        return redirect("/login/")
    messages.success(request, msg)
    # Save the email ID in the session
    request.session['email_id'] = f"{email.id}"
    # Fetch next_url or default to /
    next_url = request.session.get("next_url") or "/"
    # Redirect to /courses/ if next_url is not a valid relative URL
    if not next_url.startswith("/"):
        next_url = "/"
    return redirect(next_url)

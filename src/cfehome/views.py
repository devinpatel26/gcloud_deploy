from django.shortcuts import render

from emails.forms import EmailForm

from emails import services as emails_services

from emails.models import Email, EmailVerificationEvent


def login_logout_template_view(request):
    return render(request, "auth/login-logout.html", {})

def home_view(request):
    """
    Handles the home page view with email form validation and verification event initiation.
    """
    template_name = 'home.html'
    form = EmailForm(request.POST or None)
    context = {
        'form': form,
        "message": ""
    }

    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = emails_services.start_verification_event(email_val)
        context['form'] = EmailForm()  # Reset the form after successful submission
        context['message'] = "Success! Check your email for the confirmation link."
    else:
        print("Form Errors:", form.errors)  # Debugging: Print form errors
    print("email_id" , request.session.get('email_id'))  # Debugging: Print the session email_id
    return render(request, template_name, context)

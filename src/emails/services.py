from django.conf import settings

from django.core.mail import send_mail

from emails.models import Email, EmailVerificationEvent
from django.utils import timezone

EMAIL_HOST_USER = settings.EMAIL_HOST_USER 

def verify_email(email):
    """
    Checks if an email exists in the database with `active=False`.
    """
    qs = Email.objects.filter(email=email, active=False)
    print("Queryset:", qs)  # Debugging: Print the queryset
    return qs.exists()


def get_verification_email_msg(verification_instance, as_html=False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    
    verify_link = verification_instance.get_link()
    
    if as_html:
        return f"""
        <h1>Verify your email with the following:</h1>
        <p><a href='{verify_link}'>{verify_link}</a></p>
        """
    
    # Ensure the f-string is on a single line or properly enclosed
    return f"Verify your email with the following:\n{verify_link}"


def start_verification_event(email):
    """
    Creates or retrieves the Email object and starts the verification event.
    """
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email,
    )
    send = send_verification_email(obj.id)
    return obj, send


def send_verification_email(verify_obj_id):
    verify_obj = EmailVerificationEvent.objects.get(id=verify_obj_id)
    email = verify_obj.email
    subject = "Verify your email"
    text_msg = get_verification_email_msg(verify_obj, as_html=False)
    text_html = get_verification_email_msg(verify_obj, as_html=True)
    from_user_email_user = EMAIL_HOST_USER
    to_user = email
    return send_mail(
        subject,
        text_msg,
        from_user_email_user, 
        [to_user],
        fail_silently=False,
    )


def verify_token(token, max_attempts=5): 
    """
    Verifies the email token and returns the verification event.
    """
    qs = EmailVerificationEvent.objects.filter(token=token)
    if not qs.exists() and not qs.count() == 1:
        return False, "Invalid token.", None
    """
    Has Token
    """
    has_email_expired = qs.filter(expired=True)

    if has_email_expired.exists():
        """ token expired"""
        return False, "Token expired", None
    """
    Has token not expired
    """
    max_attempts_reached = qs.filter(attempts__gte=max_attempts)

    if max_attempts_reached.exists():
        # qs.update(expired=True)
        return False, "Max attempts reached. Token expired." , None
    """Token valid"""
    """update attempts , expire token if max attempts reached"""
    obj = qs.first()
    obj.attempts += 1
    if obj.attempts >= max_attempts:
        """invalidation proccess """
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.last_attempt_at = timezone.now()
    obj.save()
    email_obj = obj.parent
    return True, "Welcome! Email verified.", email_obj








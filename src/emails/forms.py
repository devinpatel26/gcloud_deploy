from django import forms

from .css import EMAIL_FIELD_CSS
# from .models import Email, EmailVerificationEvent
from .models import Email

from . import css, services


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id" : "email",
                "placeholder": "Your email",
                "class": css.EMAIL_FIELD_CSS
            }
        )
    )

    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']    


    def clean_email(self):
        """
        Validates the email input to ensure it's not already active.
        """
        email = self.cleaned_data.get("email")
        if services.verify_email(email):
            raise forms.ValidationError("Invalid email! Please verify your email.")
        return email

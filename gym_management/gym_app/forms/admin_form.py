from django import forms
from django.core.validators import MaxLengthValidator
from gym_app.models import Admin


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["name", "phone_number", "email", "address_city", "address_street"]

    address_city = forms.CharField(
        validators=[MaxLengthValidator(255, "Address city is too long")]
    )

    address_street = forms.CharField(
        validators=[MaxLengthValidator(255, "Address street is too long")]
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number should only contain digits")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Admin.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

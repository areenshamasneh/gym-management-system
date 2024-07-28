from django import forms
from gym_app.models import Admin


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["name", "phone_number", "email", "address_city", "address_street"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name.isalpha():
            raise forms.ValidationError("Name should only contain letters")
        return name

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

    def clean_address_city(self):
        address_city = self.cleaned_data.get("address_city")
        if len(address_city) > 255:
            raise forms.ValidationError("Address city is too long")
        return address_city

    def clean_address_street(self):
        address_street = self.cleaned_data.get("address_street")
        if len(address_street) > 255:
            raise forms.ValidationError("Address street is too long")
        return address_street

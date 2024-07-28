from django import forms
from gym_app.models import Member
from django.core.exceptions import ValidationError
from datetime import date


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "birth_date", "phone_number"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("Name is required.")
        if len(name) > 255:
            raise forms.ValidationError(
                "Name length exceeds the limit of 255 characters."
            )
        return name

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if not birth_date:
            raise forms.ValidationError("Birth date is required.")
        if birth_date > date.today():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return birth_date

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and len(phone_number) > 20:
            raise forms.ValidationError(
                "Phone number length exceeds the limit of 20 characters."
            )
        return phone_number

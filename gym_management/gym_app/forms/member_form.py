from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxLengthValidator,
    RegexValidator,
)
from gym_app.models import Member
from datetime import date


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name", "birth_date", "phone_number"]

    name = forms.CharField(
        max_length=255,
        validators=[
            MaxLengthValidator(255, "Name length exceeds the limit of 255 characters."),
            RegexValidator(regex=r"^.+$", message="Name is required."),
        ],
    )

    birth_date = forms.DateField(
        validators=[
            RegexValidator(
                regex=r"^\d{4}-\d{2}-\d{2}$",
                message="Enter a valid date in YYYY-MM-DD format.",
            )
        ]
    )

    phone_number = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message="Phone number should only contain digits."
            ),
            MaxLengthValidator(
                20, "Phone number length exceeds the limit of 20 characters."
            )
        ],
    )


    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        if birth_date > date.today():
            raise ValidationError("Birth date cannot be in the future.")
        return birth_date

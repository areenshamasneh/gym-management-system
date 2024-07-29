from django import forms
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    EmailValidator,
)
from gym_app.models import Employee


class EmployeeForm(forms.ModelForm):
    name = forms.CharField(validators=[MaxLengthValidator(255, "Name is too long")])

    phone_number = forms.CharField(
        validators=[
            MinLengthValidator(1, "Phone number cannot be empty"),
            MaxLengthValidator(20, "Phone number is too long"),
            lambda value: value.isdigit()
            or forms.ValidationError("Phone number should only contain digits"),
        ]
    )

    email = forms.EmailField(
        validators=[
            EmailValidator("Enter a valid email address"),
        ]
    )

    address_city = forms.CharField(
        validators=[MaxLengthValidator(255, "Address city is too long")]
    )

    address_street = forms.CharField(
        validators=[MaxLengthValidator(255, "Address street is too long")]
    )

    positions = forms.CharField()

    class Meta:
        model = Employee
        fields = [
            "name",
            "gym_id",
            "manager_id",
            "address_city",
            "address_street",
            "phone_number",
            "email",
            "positions",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Employee.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_positions(self):
        positions = self.cleaned_data.get("positions")
        if positions:
            positions_list = [
                pos.strip() for pos in positions.split(",") if pos.strip()
            ]
            valid_positions = {"cleaner", "trainer", "system_worker"}
            if not set(positions_list).issubset(valid_positions):
                raise forms.ValidationError("Invalid position(s) provided")
        return positions

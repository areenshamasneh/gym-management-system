from django import forms
from gym_app.models import Employee


class EmployeeForm(forms.ModelForm):
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

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name.isalpha():
            raise forms.ValidationError("Name should only contain letters")
        if len(name) > 255:
            raise forms.ValidationError("Name is too long")
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number should only contain digits")
        if phone_number and len(phone_number) > 20:
            raise forms.ValidationError("Phone number is too long")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Employee.objects.filter(email=email).exists():
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

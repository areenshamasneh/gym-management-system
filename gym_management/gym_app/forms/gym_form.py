from django import forms
from gym_app.models import Gym


class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = [
            "name",
            "type",
            "description",
            "address_city",
            "address_street",
        ]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) > 255:
            raise forms.ValidationError("Name is too long")
        return name

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

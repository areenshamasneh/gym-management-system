from django import forms
from gym_app.models import Hall


class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ["name", "users_capacity", "hall_type_id"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) > 255:
            raise forms.ValidationError(
                "Name length exceeds the limit of 255 characters."
            )
        return name

    def clean_users_capacity(self):
        users_capacity = self.cleaned_data.get("users_capacity")
        if users_capacity < 1:
            raise forms.ValidationError("Users capacity must be at least 1.")
        return users_capacity

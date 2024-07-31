from django import forms
from django.core.validators import MaxLengthValidator
from gym_app.models import HallType


class HallTypeForm(forms.ModelForm):
    class Meta:
        model = HallType
        fields = ["name", "code", "type_description"]
        widgets = {
            "type_description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].error_messages = {
            "required": "Please select a valid hall type.",
        }
        self.fields["code"].error_messages = {
            "required": "Please enter a unique code.",
        }

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if not code:
            raise forms.ValidationError("Code is required.")
        if HallType.objects.filter(code=code).exists():
            raise forms.ValidationError("This code is already used.")
        return code

from django import forms
from django.forms import CharField, ChoiceField, ValidationError
from gym_app.models import HallType


class HallTypeForm(forms.Form):
    type_description = CharField(required=False, max_length=255)
    type = ChoiceField(choices=HallType.TYPE_CHOICES)

    def clean_type_description(self):
        type_description = self.cleaned_data.get("type_description")
        if type_description and len(type_description) > 255:
            raise ValidationError(
                "Type description length exceeds the limit of 255 characters."
            )
        return type_description

    def clean_type(self):
        type = self.cleaned_data.get("type")
        if type not in dict(HallType.TYPE_CHOICES).keys():
            raise ValidationError("Invalid type selected.")
        return type

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

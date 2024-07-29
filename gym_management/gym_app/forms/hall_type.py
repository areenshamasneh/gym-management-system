from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator
from gym_app.models import HallType

class HallTypeForm(forms.Form):
    type_description = forms.CharField(
        required=False,
        max_length=255,
        validators=[MaxLengthValidator(255, "Type description length exceeds the limit of 255 characters.")]
    )
    type = forms.ChoiceField(
        choices=HallType.TYPE_CHOICES,
        validators=[
            RegexValidator(
                regex="^({})$".format("|".join([choice[0] for choice in HallType.TYPE_CHOICES])),
                message="Invalid type selected."
            )
        ]
    )

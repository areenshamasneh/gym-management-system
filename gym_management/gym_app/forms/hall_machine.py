from django import forms
from django.core.validators import MinValueValidator, MaxLengthValidator


class HallMachineForm(forms.Form):
    hall_id = forms.IntegerField(
        validators=[MinValueValidator(1, "Hall ID must be a positive integer")]
    )
    machine_id = forms.IntegerField(
        validators=[MinValueValidator(1, "Machine ID must be a positive integer")]
    )
    name = forms.CharField(
        max_length=255,
        required=False,
        validators=[MaxLengthValidator(255, "Name is too long")],
    )
    uid = forms.CharField(
        max_length=100,
        required=False,
        validators=[MaxLengthValidator(100, "UID is too long")],
    )

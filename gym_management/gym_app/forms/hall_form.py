from django import forms
from django.core.validators import MaxLengthValidator, MinValueValidator
from gym_app.models.system_models import Hall

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ["name", "users_capacity", "hall_type_id", "gym_id"]
        validators = {
            'name': [MaxLengthValidator(255, "Name is too long")],
            'users_capacity': [MinValueValidator(1, "Capacity must be at least 1")],
        }

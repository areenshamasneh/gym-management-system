from django import forms


class HallMachineForm(forms.Form):
    hall_id = forms.IntegerField(required=True)
    machine_id = forms.IntegerField(required=True)
    name = forms.CharField(max_length=255, required=False)
    uid = forms.CharField(max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("hall_id") or not cleaned_data.get("machine_id"):
            raise forms.ValidationError("Hall ID and Machine ID are required.")
        return cleaned_data

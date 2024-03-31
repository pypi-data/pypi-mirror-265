from django import forms

from .models import Clock


class ResetClockForm(forms.Form):
    num_involved = forms.IntegerField(min_value=1, label='Number of people involved')
    comment = forms.CharField(required=False, widget=forms.Textarea)


class NewClockForm(forms.ModelForm):
    class Meta:
        model = Clock
        fields = ['name']
        labels = {
            'name': 'Clock name',
        }

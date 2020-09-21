from django import forms
from .models import Task,Tasker


class DateInput(forms.DateInput):
    input_type = 'date'

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'location',
            'budget',
            'date',
            'notes',
            'name',
            'mobile_number',
        )

        labels = {
            'location':"Where do you need the tasker to present?",
            'budget':"Your estimated budget for the task?",
            'date':"When do you need the tasker to present?",
            'notes':"Notes about the task, please put as much detail as possible so that we can match best tasker for your need",
        }

        widgets = {
            'notes': forms.Textarea,
            'date': DateInput(attrs={'type': 'date'}),
        }

class TaskerCreationForm(forms.ModelForm):
    class Meta:
        model = Tasker
        fields = ('verification_doc' ,'services', )
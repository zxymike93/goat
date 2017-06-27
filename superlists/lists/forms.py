from django import forms

from lists.models import Todo


EMPTY_INPUT_ERROR = "You can't have an empty input"


class TodoForm(forms.models.ModelForm):

    class Meta:
        model = Todo
        fields = ('task',)
        widgets = {
            'task': forms.fields.TextInput(attrs={
                'placeholder': 'What do you want to do?',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'task': {'required': EMPTY_INPUT_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()

from django import forms

from matching_app.models import Recruitment


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = ["title", "content"]
        exclude = ["user"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Enter your title",
                    "id": "title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "input",
                    "placeholder": "Enter your content",
                    "id": "content",
                }
            ),
        }

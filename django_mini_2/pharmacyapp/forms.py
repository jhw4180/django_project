from django import forms   # 모델과 연결 된 폼
from .models import Board, Score
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['q1_score', 'q2_score', 'q3_score', 'q4_score', 'q5_score']
        widgets = {
            'q1_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'q2_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'q3_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'q4_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
            'q5_score': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'q1_score': '질문 1',
            'q2_score': '질문 2',
            'q3_score': '질문 3',
            'q4_score': '질문 4',
            'q5_score': '질문 5',
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
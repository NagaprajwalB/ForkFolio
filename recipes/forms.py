from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Ingredient, Step, Rating


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'category', 'description', 'photo', 'prep_time', 'cook_time', 'servings', 'difficulty']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']


IngredientFormSet = forms.inlineformset_factory(
    Recipe, Ingredient,
    fields=['name', 'quantity', 'unit'],
    extra=5, can_delete=True, max_num=30
)

StepFormSet = forms.inlineformset_factory(
    Recipe, Step,
    fields=['instruction'],
    extra=3, can_delete=True, max_num=20
)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'review']
        widgets = {
            'score': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]),
            'review': forms.Textarea(attrs={'rows': 3}),
        }


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search')
    category = forms.CharField(required=False)
    difficulty = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Difficulty'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]
    )
    max_time = forms.IntegerField(required=False, min_value=1, label='Max Total Time (mins)')

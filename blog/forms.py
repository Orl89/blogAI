from django import forms
from .models import Comment
from django.forms import EmailInput, Textarea, TextInput 


# class EmailPostForm(forms.Form):
#     nom = forms.CharField(max_length=25)
#     email = forms.EmailField()
#     a    = forms.EmailField()
#     commentaire = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nom', 'email', 'commentaire']
        widgets = {
            'nom': TextInput(attrs={
                'class': "rounded w-full",
                'style': 'margin-bottom:12px',
                'placeholder': 'Nom',
                }),

            'email': EmailInput(attrs={
                'class': "rounded w-full", 
                'style': 'margin-bottom:12px',
                'placeholder': 'Email'
                }),

            'commentaire': Textarea(attrs={
                'class': "rounded w-full", 
                'style': 'margin-bottom:12px',
                'placeholder': 'Commentaire',
                "rows": 6,
                })
        }


class SearchForm(forms.Form):
    requete = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "rounded p-4 block w-full text-xl",
                "placeholder": "Rechercher un article",
            },
            
        ),)

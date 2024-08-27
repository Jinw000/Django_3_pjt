from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
        class Meta:
                model = Product
                fields = '__all__'
                exclude = ('seller', 'mark_user', 'hit', 'hashtags',)


class ProductSearchForm(forms.Form):
        search_word = forms.CharField(label='Search Word')

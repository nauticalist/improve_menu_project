from django.utils import timezone

from django import forms

from .models import Menu, Item


class MenuForm(forms.ModelForm):
    """
    Menu creation/edit form
    """
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.SelectMultiple()
    )
    expiration_date = forms.DateTimeField(
        widget=forms.SelectDateWidget()
    )

    class Meta:
        model = Menu
        fields = (
            'season',
            'expiration_date',
            'items',
        )

    def clean_expiration_date(self):
        """
        Check the expire date is greater than today
        """
        expire_date = self.cleaned_data['expiration_date']
        if expire_date:
            if expire_date <= timezone.now():
                raise forms.ValidationError(
                    "Expiration date must be greater than today's date"
                )
            else:
                return expire_date


class ItemForm(forms.ModelForm):
    """
    Menu items creation/edit form
    """
    class Meta:
        model = Item
        fields = (
            'name',
            'description',
            'standard',
            'ingredients',
        )

from django import forms


class SearchForm(forms.Form):
    min_movies_date = forms.DateField(required=True, label="Movies minimum release date")
    max_movies_date = forms.DateField(required=True, label="Movies maximum release date")
    min_planet_diameter = forms.IntegerField(required=True, label="Planet diameter greater than")
    character_gender = forms.ChoiceField(required=True, choices=(), label="Character gender")

    def __init__(self, choices, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['character_gender'].choices = choices

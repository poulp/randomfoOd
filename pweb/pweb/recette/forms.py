from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


class AddUtensil(forms.Form):
    label = forms.CharField(label=u"Label", max_length=80, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
        Field('label'),
        Submit('submit', u'Ajouter l\'ustensile'),
        )
        super(AddUtensil, self).__init__(*args, **kwargs)


from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


class AddUtensil(forms.Form):
    label = forms.CharField(label=u"Label", max_length=80, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-add'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Field('label',placeholder="Label",css_class="form-control"),
            Submit('submit', u'Ajouter', css_class="btn btn-lg"),
        )
        super(AddUtensil, self).__init__(*args, **kwargs)

class AddAction(forms.Form):
    label = forms.CharField(label=u"Label", max_length=80, required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-add'
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Field('label',placeholder="Label",css_class="form-control"),
            Submit('submit', u'Ajouter', css_class="btn btn-lg"),
        )
        super(AddAction, self).__init__(*args, **kwargs)

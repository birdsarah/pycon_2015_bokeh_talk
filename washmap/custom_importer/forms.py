from __future__ import absolute_import, unicode_literals

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class ImportFormBase(forms.Form):
    upload = forms.FileField(label="Upload CSV file")

    def get_choice_field_name(self):
        raise NotImplementedError()

    def get_choice_field_queryset(self):
        raise NotImplementedError()

    def get_choice_field(self):
        name = self.get_choice_field_name()
        field = forms.ModelChoiceField(
            queryset=self.get_choice_field_queryset(),
            empty_label="--"
        )
        return (name, field)

    def __init__(self, *args, **kwargs):
        super(ImportFormBase, self).__init__(*args, **kwargs)

        name, field = self.get_choice_field()
        self.fields[name] = field

        self.helper = FormHelper()
        # self.helper.form_action = ''
        self.helper.form_class = 'form-horizontal'
        # self.helper.render_hidden_fields = True
        self.helper.layout = Layout(
            'upload',
            ButtonHolder(
                Submit('export', 'Export Template'),
                Submit('submit', 'Submit'),
            ),
        )

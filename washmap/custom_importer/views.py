from __future__ import absolute_import, unicode_literals

from django.http import HttpResponse, HttpResponseRedirect

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


from vanilla import FormView, GenericView

from import_export.admin import ExportMixin, ImportMixin
from import_export.formats import base_formats


class ImporterBase(ImportMixin, FormView):
    template_name = 'custom_importer/base.html'
    form_class = None  # implement forms.ImportFormBase

    def get_success_url(self):
        raise NotImplementedError()

    def get_export_url(self):
        raise NotImplementedError()

    def get_import_resource_class(self):
        raise NotImplementedError()

    def get_form(self, **kwargs):
        form = super(ImporterBase, self).get_form(**kwargs)

        form.helper.layout.insert(0, form.get_choice_field_name())

        if 'export' in self.request.POST:
            form['upload'].field.required = False
        return form

    def form_valid(self, form):

        choice_field = form.get_choice_field_name()
        import_set = form.cleaned_data[choice_field]

        if 'export' in self.request.POST:
            return HttpResponseRedirect(self.get_export_url(import_set))

        input_format = base_formats.CSV()
        resource = self.get_import_resource_class()(import_set)

        uploaded_import_file = form.cleaned_data['upload']
        data = uploaded_import_file.read()

        if not input_format.is_binary() and self.from_encoding:
            data = force_text(data, self.from_encoding)
        dataset = input_format.create_dataset(data)
        result = resource.import_data(dataset, raise_errors=False)

        if result.has_errors():
            return self.form_invalid(form, result=result)

        return super(ImporterBase, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)


class ExportTemplateBase(ExportMixin, GenericView):

    model = None

    def get_export_resource_class(self):
        raise NotImplementedError()

    def get_export_set(self, kwargs):
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        file_format = base_formats.CSV()

        resource_class = self.get_export_resource_class()
        resource = resource_class(self.get_export_set(kwargs))
        query = resource.get_queryset()
        data = resource.export(query)
        response = HttpResponse(
            file_format.export_data(data),
            mimetype='application/octet-stream',
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % (
            self.get_export_filename(file_format),
        )
        return response

    def get_export_filename(self, file_format):
        filename = "%s.%s" % (
            self.model.__name__,
            file_format.get_extension())
        return filename

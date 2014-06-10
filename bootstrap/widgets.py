from django import forms
from django.template import loader, Context
from django.forms.utils import flatatt

class TemplateWidget (forms.Widget):
    """
    A widget that renders the specified ``template_name`` with the following context
    (plus any ``extra_context``):

        name
            The name of the field
        value
            The field's current value
        attrs
            Flattened HTML attributes, computed from ``self.build_attrs``
        widget
            A reference to ``self``
    """

    template_name = None
    extra_context = {}

    def __init__(self, template_name=None, attrs=None, **extra_context):
        if template_name:
            self.template_name = template_name
        self.extra_context.update(extra_context)
        super(TemplateWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        template = loader.get_template(self.template_name)
        input_attrs = flatatt(self.build_attrs(attrs, name=name))
        params = {
            'name': name,
            'value': value,
            'attrs': input_attrs,
            'widget': self,
        }
        params.update(self.extra_context)
        return template.render(Context(params))

class BootstrapWidget (object):
    """
    Base class for most widgets implemented here (with the exception of :class:`TemplateWidget`).
    """

    css_classes = ('form-control',)
    """
    A tuple of CSS classes to apply to the rendered widget, in addition to any ``class`` attribute specified.
    """

    extra_attrs = {}
    """
    Extra input attributes, defined on a class level.
    """

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = dict(self.attrs, **kwargs)
        attrs.update(self.extra_attrs)
        if extra_attrs:
            attrs.update(extra_attrs)
        new_class = '%s %s' % (attrs.get('class', ''), ' '.join(self.css_classes))
        attrs['class'] = new_class.strip()
        return attrs

class TextInput (BootstrapWidget, forms.TextInput):
    """ Bootstrap version of ``forms.TextInput`` """

class AutofocusTextInput (TextInput):
    """ Autofocusing TextInput widget. """
    extra_attrs = {'autofocus': 'autofocus'}

class Textarea (BootstrapWidget, forms.Textarea):
    """ Bootstrap version of ``forms.Textarea`` """

class DateInput (BootstrapWidget, forms.DateInput):
    """ Bootstrap version of ``forms.DateInput``. The input is rendered with an extra "date" class. """
    css_classes = BootstrapWidget.css_classes + ('date',)

class Select (BootstrapWidget, forms.Select):
    """ Bootstrap version of ``forms.Select`` """

class SelectMultiple (BootstrapWidget, forms.SelectMultiple):
    """ Bootstrap version of ``forms.SelectMultiple`` """

class NullBooleanSelect (BootstrapWidget, forms.NullBooleanSelect):
    """ Bootstrap version of ``forms.NullBooleanSelect`` """
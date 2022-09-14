from django import template
from contact_app.forms import ContactForm

register = template.Library()

@register.inclusion_tag('contact_app/tags/form.html')
def contact_form():
    return {'contact_form': ContactForm()}
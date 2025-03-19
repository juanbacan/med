
from django import forms

from applications.core.forms import BaseForm


class MensajeUsuarioForm(BaseForm):
    numero = forms.CharField(label="Número de teléfono", required=True)
    mensaje = forms.CharField(label="Mensaje", required=True, widget=forms.Textarea(attrs={'rows': 3}))
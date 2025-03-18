from core.forms import BaseForm, ModelBaseForm, BaseInline
from tinymce.widgets import TinyMCE
from django import forms
from dal import autocomplete, forward
from .models import *



class PRAMSospechosoInline(BaseInline):
    model = PRAMSospechoso
    fields = '__all__'
    extra = 0
    can_delete = False
    prefix = 'pram_sospechoso'
    verbose_name = 'Sospechoso'
    verbose_name_plural = 'Sospechosos'

class PRAMConcominanteInline(BaseInline):
    model = PRAMConcominante
    fields = '__all__'
    extra = 0
    can_delete = False
    prefix = 'pram_concominante'
    verbose_name = 'Concominante'
    verbose_name_plural = 'Concominantes'

 
class PacienteReaccionesAdversasMedicamentosForm(ModelBaseForm):
    inlines = [PRAMSospechosoInline(), PRAMConcominanteInline()]

    class Meta:
        model = PacienteReaccionesAdversasMedicamentos
        fields = '__all__'
        widgets = {
            'sexo': forms.RadioSelect(choices=CHOICES_SEXO.choices),
            'sospecha_de_reaccion': forms.RadioSelect(choices=CHOICES_TIPO_REACCION.choices),
            'descripcion_sospecha': forms.Textarea(attrs={'rows': 1, 'cols': 40}),
            'descripcion_historia_clinica': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'desaparecio_al_suspender_medicamento': forms.RadioSelect(choices=CHOICES_SELECCION.choices),   
            'reaparecio_al_administrar_nuevo_medicamento': forms.RadioSelect(choices=CHOICES_SELECCION.choices),   
            'desaparecio_al_reducir_dosis': forms.RadioSelect(choices=CHOICES_SELECCION.choices),   
            'descripcion_condicion_importante': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'paciente_recibio_tratamiento': forms.RadioSelect(choices=CHOICES_SELECCION.choices),
            'descripcion_tratamiento': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'tipo_reporte': forms.RadioSelect(choices=CHOICES_TIPO_REPORTE.choices),
            'origen_reporte': forms.RadioSelect(choices=CHOICES_ORIGEN_REPORTE.choices),
        }
    

class PacienteTecnovigilanciaForm(ModelBaseForm):

    class Meta:
        model = PacienteTecnovigilancia
        fields = '__all__'
        widgets = {
            'sexo': forms.RadioSelect(choices=CHOICES_SEXO.choices),
            'diagnostico_presuntivo_definitivo': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'dispositivo_utilizado_mas_una_vez': forms.RadioSelect(choices=CHOICES_SELECCION.choices),
            'deteccion_evento_adverso': forms.RadioSelect(choices=CHOICES_SELECCION.choices),
            'clasificacion_evento' : forms.RadioSelect(choices=CHOICES_CLASIFICACION_EVENTO.choices),
            'descripcion_evento_adverso': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'causa_sospecha_provoco_evento': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'reporto_importador': forms.RadioSelect(choices=CHOICES_SELECCION.choices),
            'envio_dispositivo_importador': forms.RadioSelect(choices=CHOICES_SELECCION.choices),
            'descripcion_dispositivo': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'tipo_dispositivo': forms.RadioSelect(choices=CHOICES_TIPO_MEDICAMENTO.choices),
            'nivel_riesgo': forms.RadioSelect(choices=CHOICES_NIVEL_RIESGO.choices),
            'informacion_adicional': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
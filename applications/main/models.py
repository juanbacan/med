from django.db import models
from core.models import ModeloBase


class Zona(ModeloBase):
    nombre = models.CharField(default='', max_length=100, verbose_name='Nombre', unique=True)
    codigo_sniese = models.CharField(default='', max_length=15, verbose_name='Código SNIESE')

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'


class Provincia(ModeloBase):
    nombre = models.CharField(default='', max_length=100, verbose_name='Nombre', unique=True)
    alias = models.CharField(default='', max_length=100, verbose_name='Alias')
    zona = models.ForeignKey(Zona, blank=True, null=True, verbose_name="Zona", on_delete=models.SET_NULL)
    codigo_sniese = models.CharField(default='', max_length=15, verbose_name='Código SNIESE')

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'



class CHOICES_SEXO(models.TextChoices):
    FEMENINO = 'F', 'Femenino'
    MASCULINO = 'M', 'Masculino'


class CHOICES_TIPO_REACCION(models.TextChoices):
    RAM = 'RAM', 'Reacción Adversa a Medicamentos'
    FT = 'FT', 'Falta de Terapéutica'
    EM = 'EM', 'Error de Medicación'


class CHOICES_SELECCION(models.TextChoices):
    SI = 'SI', 'Sí'
    NO = 'NO', 'No'
    DESCONOCIDO = 'DESCONOCIDO', 'Desconocido'
    

class CHOICES_TIPO_REPORTE(models.TextChoices):
    INICIAL = 'INICIAL', 'Inicial'
    SEGUIMIENTO = 'SEGUIMIENTO', 'Seguimiento'

class CHOICES_ORIGEN_REPORTE(models.TextChoices):
    AMBULATORIO = 'AMBULATORIO', 'Ambulatorio'
    HOSPITALARIO = 'HOSPITALARIO', 'Hospitalario'

class BaseMedicamento(ModeloBase):
    nombre_generico = models.CharField(max_length=300)
    nombre_comercial = models.CharField(max_length=300)
    lote = models.CharField(max_length=100)
    registro_sanitario = models.CharField(max_length=100)
    forma_farmaceutica = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    via_administracion = models.CharField(max_length=100)
    motivo_prescripcion = models.CharField(max_length=100)

    class Meta:
        abstract = True



class PacienteReaccionesAdversasMedicamentos(ModeloBase):
    # Información del paciente
    nombre = models.CharField(max_length=300, verbose_name='Nombre o iniciales del Paciente')
    edad = models.IntegerField(verbose_name='Edad')
    sexo = models.CharField(max_length=1, choices=CHOICES_SEXO.choices, verbose_name='Sexo')
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso')
    talla = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Talla')
    etnia = models.CharField(max_length=100, verbose_name='Etnia')
    num_hist_clinica = models.CharField(max_length=100, verbose_name='N° Historia Clínica')

    # Información sobre sospecha # utilizar choices_tipo_reaccion
    sospecha_de_reaccion = models.CharField(max_length=13, choices=CHOICES_TIPO_REACCION.choices)
    descripcion_sospecha = models.TextField(verbose_name='Descripción de la RAM, FT, EM')
    fecha_inicio_sospecha = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin_sospecha = models.DateField(verbose_name='Fecha de Fin')
    descripcion_historia_clinica = models.TextField(verbose_name='Descripción de la Historia Clínica')

    # Medicamento Sospechoso

    # Resultado del Evento Adverso
    desaparecio_al_suspender_medicamento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices)
    desaparecio_al_redusir_dosis = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices)
    reaparecio_al_administrar_nuevo_medicamento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices)
    recuperado_resuelto = models.BooleanField()
    recuperando_resolviendo = models.BooleanField()
    recuperado_resuelto_con_secuela = models.BooleanField()
    no_recuperado_no_resuelto = models.BooleanField()
    fatal = models.BooleanField()
    desconocido = models.BooleanField()

    # Severidad
    muerte = models.BooleanField()
    hospitalizacion_prolongada = models.BooleanField()
    requirio_hospitalizacion = models.BooleanField()
    anomalia_congenita = models.BooleanField()
    amenaza_vida = models.BooleanField()
    discapacidad = models.BooleanField()
    na = models.BooleanField()
    otra_condicion_importante = models.BooleanField()
    descripcion_condicion_importante = models.TextField()

    # Tratamiento
    paciente_recibio_tratamiento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices)
    descripcion_tratamiento = models.TextField()

    # Medicamentos concomitantes o utilizados

    # Información del Notificador
    nombre_iniciales_notificador = models.CharField(max_length=100)
    profesion_notificador = models.CharField(max_length=100)
    lugar_trabajo_notificador = models.CharField(max_length=100)
    servicio_medico_notificador = models.CharField(max_length=100)
    direccion_notificador = models.CharField(max_length=100)
    provincia_notificador = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    telefono_notificador = models.CharField(max_length=100)
    email_notificador = models.EmailField()
    tipo_reporte = models.CharField(max_length=13, choices=CHOICES_TIPO_REPORTE.choices)
    origen_reporte = models.CharField(max_length=13, choices=CHOICES_ORIGEN_REPORTE.choices)

    fecha_reporte = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.nombre


class PRAMSospechoso(BaseMedicamento):
    paciente = models.ForeignKey(PacienteReaccionesAdversasMedicamentos, on_delete=models.CASCADE)


class PRAMConcominantes(BaseMedicamento):
    paciente = models.ForeignKey(PacienteReaccionesAdversasMedicamentos, on_delete=models.CASCADE)

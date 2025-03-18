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


class Etnia(ModeloBase):
    nombre = models.CharField(default='', max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Etnia'
        verbose_name_plural = 'Etnias'


class CHOICES_SEXO(models.TextChoices):
    F = 'F', 'F'
    M = 'M', 'M'


class CHOICES_SEXO2(models.TextChoices):
    F = 'F', 'Hombre'
    M = 'M', 'Mujer'


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
    sexo = models.CharField(max_length=1, choices=CHOICES_SEXO.choices, verbose_name='Sexo', blank=False, null=False, default=None)
    peso = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso')
    talla = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Talla')
    etnia = models.ForeignKey(Etnia, on_delete=models.CASCADE)
    num_hist_clinica = models.CharField(max_length=100, verbose_name='N° Historia Clínica')

    # Información sobre sospecha # utilizar choices_tipo_reaccion
    sospecha_de_reaccion = models.CharField(max_length=13, choices=CHOICES_TIPO_REACCION.choices, default=None)
    descripcion_sospecha = models.TextField(verbose_name='Descripción de la RAM, FT, EM')
    fecha_inicio_sospecha = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin_sospecha = models.DateField(verbose_name='Fecha de Fin')
    descripcion_historia_clinica = models.TextField(verbose_name='Descripción de la Historia Clínica')

    # Medicamento Sospechoso

    # Resultado del Evento Adverso
    desaparecio_al_suspender_medicamento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices, default=None)
    desaparecio_al_reducir_dosis = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices, default=None)
    reaparecio_al_administrar_nuevo_medicamento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices, default=None)
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
    descripcion_condicion_importante = models.TextField(null=True, blank=True, verbose_name='Descripción de la condición importante')

    # Tratamiento
    paciente_recibio_tratamiento = models.CharField(max_length=13, choices=CHOICES_SELECCION.choices, default=None)
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
    tipo_reporte = models.CharField(max_length=13, choices=CHOICES_TIPO_REPORTE.choices, default=None)
    origen_reporte = models.CharField(max_length=13, choices=CHOICES_ORIGEN_REPORTE.choices, default=None)

    fecha_reporte = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre


class PRAMSospechoso(BaseMedicamento):
    paciente = models.ForeignKey(PacienteReaccionesAdversasMedicamentos, on_delete=models.CASCADE)


class PRAMConcominante(BaseMedicamento):
    paciente = models.ForeignKey(PacienteReaccionesAdversasMedicamentos, on_delete=models.CASCADE)





class CHOICES_TIPO_DETECCION_EVENTO(models.TextChoices):
    ANTES_USO = 'ANTES_USO', 'Antes del uso'
    DURANTE_USO = 'DURANTE_USO', 'Durante el uso'
    DESPUES_USO = 'DESPUES_USO', 'Después del uso'

class CHOICES_CLASIFICACION_EVENTO(models.TextChoices):
    EVENTO_ADVERSO = 'EVENTO_ADVERSO', 'Evento Adverso'
    INCIDENTE_ADVERSO = 'INCIDENTE_ADVERSO', 'Incidente Adverso'

class CHOICES_TIPO_MEDICAMENTO(models.TextChoices):
    NO_INVASIVO = 'NO_INVASIVO', 'Dispositivo Médico de Uso Humano No invasivo'
    INVASIVO = 'INVASIVO', 'Dispositivo Médico de Uso Humano Invasivo'
    IN_VITRO = 'IN_VITRO', 'Dispositivo Médico de Uso Humano In Vitro'
    ACTIVO = 'ACTIVO', 'Dispositivo Médico de Uso Humano Activo'

class CHOICES_NIVEL_RIESGO(models.TextChoices):
    BAJO = 'BAJO', 'Nivel de Riesgo Bajo I (Riesgo Bajo)'
    MODERADO_BAJO = 'MODERADO_BAJO', 'Nivel de Riesgo Medio II (Riesgo Moderado Bajo)'
    MODERADO_ALTO = 'MODERADO_ALTO', 'Nivel de Riesgo Medio III (Riesgo Moderado Alto)'
    ALTO = 'ALTO', 'Nivel de Riesgo Alto IV (Riesgo Alto)'

class CHOICES_SI_NO(models.TextChoices):
    SI = 'SI', 'Sí'
    NO = 'NO', 'No'

class PacienteTecnovigilancia(ModeloBase):
    # A.  Información del paciente
    identificacion = models.CharField(max_length=100, verbose_name='Identificación del Paciente')
    edad = models.IntegerField(verbose_name='Edad')
    sexo = models.CharField(max_length=1, choices=CHOICES_SEXO2.choices, verbose_name='Sexo', blank=False, null=False, default=None)
    diagnostico_presuntivo_definitivo = models.TextField(verbose_name='Diagnóstico Presuntivo o definitivo del Paciente')

    # B. Datos de ocurrencia del evento adverso/incidente adverso
    nombre_establecimiento = models.CharField(max_length=100, verbose_name='Nombre del Establecimiento (Indicar si es una empresa pública o privada)')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    fecha_inicio_evento_adverso = models.DateField(verbose_name='Fecha de Inicio del Evento Adverso / incidente adverso')
    fecha_fin_evento_adverso = models.DateField(verbose_name='Fecha de Fin del Evento Adverso / incidente adverso')
    dispositivo_utilizado_mas_una_vez = models.CharField(max_length=13, choices=CHOICES_SI_NO.choices, default=None)
    tiempo_contacto_dispositivo = models.CharField(max_length=100, verbose_name='Tiempo de contacto con el dispositivo médico (minutos, horas, días, meses, etc*)')
    deteccion_evento_adverso = models.CharField(max_length=13, choices=CHOICES_TIPO_DETECCION_EVENTO.choices, default=None)
    clasificacion_evento = models.CharField(max_length=20, choices=CHOICES_CLASIFICACION_EVENTO.choices, default=None)
    descripcion_evento_adverso = models.TextField(verbose_name='Descripción del evento adverso/incidente adverso')
    descripcion_historia_clinica = models.TextField(verbose_name='Descripción de la Historia Clínica')

    muerte = models.BooleanField(verbose_name='Muerte')
    fecha_muerte = models.DateField(verbose_name='Fecha', null=True, blank=True)
    enfermadad = models.BooleanField(verbose_name='Enfermedad o daño que amenace la vida')
    requiere_intervencion_medica = models.BooleanField(verbose_name='Requiere intervención médica o quirúrgica')
    hospitalizacion_prolongada = models.BooleanField(verbose_name='Hospitalización inicial o prolongada')
    danio_funcion_estructural_corporal = models.BooleanField(verbose_name='Daño de una función o estructura corporal')
    no_hubo_danio = models.BooleanField(verbose_name='No hubo daño')
    otro_desenlace = models.BooleanField(verbose_name='Otros (especificar)')
    causa_sospecha_provoco_evento = models.TextField(verbose_name='Causa (s) que sospeche que provocó el evento')

    reporto_importador = models.CharField(max_length=10, choices=CHOICES_SI_NO.choices, default=None)
    fecha_reporto_importador = models.DateField(verbose_name='Fecha', null=True, blank=True)

    envio_dispositivo_importador = models.CharField(max_length=10, choices=CHOICES_SI_NO.choices, default=None)
    fecha_envio_dispositivo_importador = models.DateField(verbose_name='Fecha', null=True, blank=True)

    # C. Identificación del dispositivo médico/equipo
    nombre_dispositivo = models.CharField(max_length=100, verbose_name='Nombre Comercial*')
    descripcion_dispositivo = models.TextField(verbose_name='Descripción')
    registro_sanitario = models.CharField(max_length=100, verbose_name='Registro Sanitario*')
    lote = models.CharField(max_length=100, verbose_name='Lote*')
    serie = models.CharField(max_length=100, verbose_name='Serie*', null=True, blank=True)
    fecha_elaboracion = models.DateField(verbose_name='Fecha de Elaboración*', null=True, blank=True)
    version_software = models.CharField(max_length=100, verbose_name='Versión de Software (cuando aplique)', null=True, blank=True)
    fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento*', null=True, blank=True)
    nombre_o_razon_fabricante = models.CharField(max_length=100, verbose_name='Nombre o Razón Social del Fabricante', null=True, blank=True)
    nombre_o_razon_importador = models.CharField(max_length=100, verbose_name='Nombre o Razón Social del Importador', null=True, blank=True)

    # Clasificación del dispositivo médico
    tipo_dispositivo = models.CharField(max_length=13, choices=CHOICES_TIPO_MEDICAMENTO.choices, default=None, verbose_name='1. Tipo de Dispositivo Médico de Uso Humano')
    nivel_riesgo = models.CharField(max_length=13, choices=CHOICES_NIVEL_RIESGO.choices, default=None, verbose_name='2. Nivel de Riesgo del Dispositivo Médico de Uso Humano')
    informacion_adicional = models.TextField(verbose_name='Información Adicional', null=True, blank=True)

    # Identificación del Notificador
    nombre_iniciales_notificador = models.CharField(max_length=100, verbose_name='Nombre')
    profesion_notificador = models.CharField(max_length=100, verbose_name='Profesión')
    establecimiento_notificador = models.CharField(max_length=100, verbose_name='Establecimiento/servicio de salud a la que pertenece')
    direccion_notificador = models.CharField(max_length=100, verbose_name='Dirección')
    telefono_notificador = models.CharField(max_length=100, verbose_name='Teléfono')
    email_notificador = models.EmailField(verbose_name='Email')
    fecha_reporte = models.DateTimeField(auto_now_add=True)



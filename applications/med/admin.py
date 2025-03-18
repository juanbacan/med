from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Provincia)
admin.site.register(Etnia)

admin.site.register(PacienteReaccionesAdversasMedicamentos)
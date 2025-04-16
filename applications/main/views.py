import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from applications.med.forms import PacienteReaccionesAdversasMedicamentosForm, PacienteTecnovigilanciaForm
from django.template.loader import render_to_string

from core.views import ViewClassBase
from core.notificaciones import notify_push_app_user
from core.correos import send_email_thread
from core.whatsapp import send_whatsapp_message_thread
from core.utils import error_json, success_json, get_redirect_url
from custom_forms.utils import guardar_o_actualizar_campos_respuesta

from core.models import CustomUser, AplicacionWeb
from custom_forms.models import Encuesta, Formulario, RespuestaEncuesta


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'main/home.html', context)


class PRAMView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PacienteReaccionesAdversasMedicamentosForm()
        return render(request, 'main/pram.html', context)
        
    def post(self, request, *args, **kwargs):
        context = {}
        form = PacienteReaccionesAdversasMedicamentosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formulario guardado con éxito.')
            admins = CustomUser.objects.filter(is_superuser=True)
            for admin in admins:
                try:
                    notify_push_app_user(
                        usuario_notificado=admin,
                        usuario_notifica=request.user if request.user.is_authenticated else None,
                        url=f'administracion/med/pram/?action=edit&id={form.instance.id}',
                        mensaje='Se ha registrado una nueva reacción adversa a un medicamento.',
                        tipo='nueva_reaccion_adversa'
                    )
                    application = AplicacionWeb.objects.first()
                    context = {}
                    context['application'] = application
                    context['title'] = 'Nueva Reacción Adversa'
                    context['message'] = 'Se ha registrado una nueva reacción adversa a un medicamento.'
                    template = render_to_string('correo/base_correo.html', context)
                    send_email_thread(
                        subject='Nueva reacción adversa registrada',
                        body=template,
                        to=admin.email
                    )
                except Exception as e:
                    print(f"Error al enviar notificación a {admin.email}: {e}")
            send_whatsapp_message_thread(
                number='0992011851',
                message='Se ha registrado una nueva reacción adversa a un medicamento.'
            )
            return success_json(url='/')
        else:
            print("Error en el formulario:", form.errors)
            return error_json(forms=[form])



class Tecnovigilancia2View(ViewClassBase):

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'post_{self.action}'):
            return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
        return error_json(mensaje="Acción no permitida")
    
    def post_responder_encuesta(self, request, context, *args, **kwargs):
        encuesta = Encuesta.objects.get(pk=self.data.get('id', None))
        respuestas = json.loads(request.POST.get('respuestas', None))

        respuesta = RespuestaEncuesta.objects.create(
            encuesta=encuesta,
            usuario=request.user if request.user.is_authenticated else None,
            version=encuesta.formulario.version
        )

        errores = guardar_o_actualizar_campos_respuesta(respuesta, respuestas)
        if errores:
            raise ValueError("Error al guardar las respuestas: " + str(errores))
        
        messages.success(request, "Encuesta respondida exitosamente")
        return success_json(mensaje="Encuesta respondida exitosamente", url=get_redirect_url(request, encuesta))
    
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'get_{self.action}'):
            return getattr(self, f'get_{self.action}')(request, context, *args, **kwargs)

        context['encuesta'] = encuesta = Encuesta.objects.get(pk=1)
        context['formulario'] = encuesta.formulario
        return render(request, 'main/tecnovigilancia2.html', context)


class TecnovigilanciaView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PacienteTecnovigilanciaForm()
        return render(request, 'main/tecnovigilancia.html', context)
        
    def post(self, request, *args, **kwargs):
        context = {}
        form = PacienteTecnovigilanciaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Formulario guardado con éxito.')
            admins = CustomUser.objects.filter(is_superuser=True)
            for admin in admins:
                try:
                    notify_push_app_user(
                        usuario_notificado=admin,
                        usuario_notifica=request.user if request.user.is_authenticated else None,
                        url=f'/administracion/med/tecnovigilancia/?action=edit&id={form.instance.id}',
                        mensaje='Se ha registrado una nueva reacción adversa a un medicamento.',
                        tipo='nueva_tecnovigilancia'
                    )
                    application = AplicacionWeb.objects.first()
                    context = {}
                    context['application'] = application
                    context['title'] = 'Nueva Tecnovigilancia'
                    context['message'] = 'Se ha registrado una nueva tecnovigilancia.'
                    template = render_to_string('correo/base_correo.html', context)
                    send_email_thread(
                        subject='Nueva tecnovigilancia registrada',
                        body=template,
                        to=admin.email
                    )
                except Exception as e:
                    print(f"Error al enviar notificación a {admin.email}: {e}")
            
            send_whatsapp_message_thread(
                number='0992011851',
                message='Se ha registrado una nueva tecnovigilancia.'
            )
            return success_json(url='/')
        else:
            print("Error en el formulario:", form.errors)
            return error_json(forms=[form])
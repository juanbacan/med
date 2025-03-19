from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from applications.med.forms import PacienteReaccionesAdversasMedicamentosForm, PacienteTecnovigilanciaForm
from django.template.loader import render_to_string

from core.notificaciones import notify_push_app_user
from core.correos import send_email_thread
from core.whatsapp import send_whatsapp_message_thread

from core.models import CustomUser, AplicacionWeb
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
            print("Formulario válido:", form.cleaned_data)
            form.save()
            messages.success(request, 'Formulario guardado con éxito.')
            admins = CustomUser.objects.filter(is_superuser=True)
            for admin in admins:
                notify_push_app_user(
                    usuario_notificado=admin,
                    usuario_notifica=request.user if request.user.is_authenticated else None,
                    url=f'administracion/med/pram/?action=edit&id={form.instance.id}/',
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
            send_whatsapp_message_thread(
                number='0992011851',
                message='Se ha registrado una nueva reacción adversa a un medicamento.'
            )
            return redirect('main:home')
        else:
            print("Error en el formulario:", form.errors)
            messages.error(request, 'Error al guardar el formulario.')
            context['form'] = form
            return render(request, 'main/pram.html', context)
        

class TecnovigilanciaView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PacienteTecnovigilanciaForm()
        return render(request, 'main/tecnovigilancia.html', context)
        
    def post(self, request, *args, **kwargs):
        context = {}
        form = PacienteTecnovigilanciaForm(request.POST)
        if form.is_valid():
            print("Formulario válido:", form.cleaned_data)
            form.save()
            messages.success(request, 'Formulario guardado con éxito.')
            admins = CustomUser.objects.filter(is_superuser=True)
            for admin in admins:
                notify_push_app_user(
                    usuario_notificado=admin,
                    usuario_notifica=request.user if request.user.is_authenticated else None,
                    url=f'/administracion/med/tecnovigilancia/?action=edit&id={form.instance.id}/',
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
            
            send_whatsapp_message_thread(
                number='0992011851',
                message='Se ha registrado una nueva tecnovigilancia.'
            )
            return redirect('main:home')
        else:
            print("Error en el formulario:", form.errors)
            messages.error(request, 'Error al guardar el formulario.')
            context['form'] = form
            return render(request, 'main/tecnovigilancia.html', context)
from django.shortcuts import render
from core.views import ViewAdministracionBase
from applications.whatsappbot.forms import MensajeUsuarioForm

from core.utils import error_json, success_json, get_redirect_url
from core.whatsapp import send_whatsapp_message


class WhatsappBotAdminView(ViewAdministracionBase):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'post_{self.action}'):
            return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
        return error_json(mensaje="Acción no permitida")
        
    def post_enviar_mensaje_usuario(self, request, context, *args, **kwargs):
        form = MensajeUsuarioForm(request.POST)
        if form.is_valid():
            mensaje = form.cleaned_data.get('mensaje').strip()
            numero = form.cleaned_data.get('numero').strip()
            ok = send_whatsapp_message(numero, mensaje)
            if not ok:
                return error_json(mensaje="Error al enviar el mensaje")
            return success_json()
        return error_json(mensaje="Error al enviar el mensaje", errors=form.errors)
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if self.action and hasattr(self, f'get_{self.action}'):
            return getattr(self, f'get_{self.action}')(request, context, *args, **kwargs)
        
        return render(request, 'whatsappbot/admin/whatsapp_admin.html', context)
    
    def get_enviar_mensaje_usuario(self, request, context, *args, **kwargs):
        context['form'] = MensajeUsuarioForm()
        context['title'] = "Enviar mensaje a usuarios"
        return render(request, 'core/modals/formModal.html', context)

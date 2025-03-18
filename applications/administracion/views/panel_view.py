import bson

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Q

from core.utils import success_json, bad_json, check_is_superuser, \
    get_query_params, replace_images, get_url_params

from core.models import CustomUser, CorreoTemplate
from core.views import ViewAdministracionBase
from applications.administracion.forms import *

class PanelView(ViewAdministracionBase):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'administracion/administracion.html', context)

def api(request):
    action, data = get_query_params(request)
    
    if not action:
        return bad_json(mensaje="No se ha enviado el parametro action")
    if not request.user.is_authenticated:
        return bad_json(mensaje="No estás autenticado")
    
    if request.method == 'POST':                    
        return bad_json(mensaje="No se encuentra la accion")
    
    if request.method == 'GET':
        if action == "volver_usuario":
            if request.session.get('volver_usuario', None) and request.session.get('usuario_original', None):
                usuario = CustomUser.objects.get(id=request.session['usuario_original'])
                usuario.backend = 'allauth.account.auth_backends.AuthenticationBackend'
                url = request.session.get('volver_usuario_url', "/administracion")
                logout(request)
                login(request, usuario)
                if "volver_usuario" in request.session:
                    del request.session['volver_usuario']
                if "volver_usuario_url" in request.session:
                 del request.session['volver_usuario_url']
                if "usuario_original" in request.session:
                    del request.session['usuario_original']
                return redirect(url)
            else:
                return redirect('/')
    
    else:
        return success_json(mensaje = "Ok")


def room(request, room_name):
    return render(request, "administracion/room.html", {"room_name": room_name})



def room(request, room_name):
    return render(request, "administracion/room.html", {"room_name": room_name})


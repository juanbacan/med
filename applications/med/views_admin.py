from django.shortcuts import render
from core.views import ViewAdministracionBase
from .models import *
from .forms import *

from core.utils import error_json, success_json, get_redirect_url


class PRAMAdminView(ViewAdministracionBase):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'post_{self.action}'):
            return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
        return error_json(mensaje="Acción no permitida")
    
    def post_edit(self, request, context, *args, **kwargs):
        form = PacienteReaccionesAdversasMedicamentosForm(request.POST, instance=PacienteReaccionesAdversasMedicamentos.objects.get(pk=self.data.get('id')))
        if form.is_valid():
            form.save()
            return success_json(url=get_redirect_url(request))
        return error_json(mensaje="Error al guardar el modulo", errors=form.errors)
    
    def post_delete(self, request, context, *args, **kwargs):
        object = PacienteReaccionesAdversasMedicamentos.objects.get(id=request.POST.get('id'))
        object.delete()
        return success_json(url=get_redirect_url(request)) 
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if self.action and hasattr(self, f'get_{self.action}'):
            return getattr(self, f'get_{self.action}')(request, context, *args, **kwargs)
        
        context['objects'] = PacienteReaccionesAdversasMedicamentos.objects.order_by('id')
        return render(request, 'administracion/pram/lista.html', context)
    
    def get_edit(self, request, context, *args, **kwargs):
        context['object'] = modulo = PacienteReaccionesAdversasMedicamentos.objects.get(pk=self.data.get('id'))
        context['form'] = PacienteReaccionesAdversasMedicamentosForm(instance=modulo)
        return render(request, 'administracion/pram/form_pram.html', context)
    
    def get_print(self, request, context, *args, **kwargs):
        context['object'] = object = PacienteReaccionesAdversasMedicamentos.objects.get(pk=self.data.get('id'))
        context['form'] = PacienteReaccionesAdversasMedicamentosForm(instance=object)
        return render(request, 'administracion/pram/print_pram.html', context)

    def get_delete(self, request, context, *args, **kwargs):
        id = self.data.get('id', None)
        object = PacienteReaccionesAdversasMedicamentos.objects.get(id=id)
        context['title'] = "Eliminar registro"
        context['message'] = f'¿Está seguro de que desea eliminar el registro: {object}?"'
        context['formid'] = object.id 
        context['delete_obj'] = True
        return render(request, 'core/modals/formModal.html', context)
    

class TecnovigilanciaAdminView(ViewAdministracionBase):
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.action and hasattr(self, f'post_{self.action}'):
            return getattr(self, f'post_{self.action}')(request, context, *args, **kwargs)
        return error_json(mensaje="Acción no permitida")
    
    def post_edit(self, request, context, *args, **kwargs):
        form = PacienteTecnovigilanciaForm(request.POST, instance=PacienteTecnovigilancia.objects.get(pk=self.data.get('id')))
        if form.is_valid():
            form.save()
            return success_json(url=get_redirect_url(request))
        return error_json(mensaje="Error al guardar el modulo", errors=form.errors)
    
    def post_delete(self, request, context, *args, **kwargs):
        object = PacienteTecnovigilancia.objects.get(id=request.POST.get('id'))
        object.delete()
        return success_json(url=get_redirect_url(request)) 
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if self.action and hasattr(self, f'get_{self.action}'):
            return getattr(self, f'get_{self.action}')(request, context, *args, **kwargs)
        
        context['objects'] = PacienteTecnovigilancia.objects.order_by('id')
        return render(request, 'administracion/tecnovigilancia/lista.html', context)
    
    def get_edit(self, request, context, *args, **kwargs):
        context['object'] = object = PacienteTecnovigilancia.objects.get(pk=self.data.get('id'))
        context['form'] = PacienteTecnovigilanciaForm(instance=object)
        return render(request, 'administracion/tecnovigilancia/form_tecnovigilancia.html', context)


    def get_print(self, request, context, *args, **kwargs):
        context['object'] = object = PacienteTecnovigilancia.objects.get(pk=self.data.get('id'))
        context['form'] = PacienteTecnovigilanciaForm(instance=object)
        return render(request, 'administracion/tecnovigilancia/print_tecnovigilancia.html', context)


    def get_delete(self, request, context, *args, **kwargs):
        id = self.data.get('id', None)
        object = PacienteTecnovigilancia.objects.get(id=id)
        context['title'] = "Eliminar registro"
        context['message'] = f'¿Está seguro de que desea eliminar el registro: {object}?"'
        context['formid'] = object.id 
        context['delete_obj'] = True
        return render(request, 'core/modals/formModal.html', context)

from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from applications.med.forms import PacienteReaccionesAdversasMedicamentosForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'main/home.html', context)


class PRAMView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = PacienteReaccionesAdversasMedicamentosForm()
        return render(request, 'main/pram.html', context)
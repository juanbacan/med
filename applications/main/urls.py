from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    # ******************* Base *******************
    path('', HomeView.as_view(), name='home'),
    path('pram/', PRAMView.as_view(), name='pram'),
    path('tecnovigilancia/', TecnovigilanciaView.as_view(), name='tecnovigilancia'),
    path('tecnovigilancia2/', Tecnovigilancia2View.as_view(), name='tecnovigilancia2')
]
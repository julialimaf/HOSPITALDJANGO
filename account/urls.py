from django.urls import path
from .views import (
    PacientRegisterView,
    PacientLoginView,
    MedicoRegisterView,
    MedicoLoginView,
    MedicoListView,
    ConsultaCreateView,
    ConsultaListView
)

urlpatterns = [
    path('paciente/register/', PacientRegisterView.as_view(), name='paciente_register'),
    path('paciente/login/', PacientLoginView.as_view(), name='paciente_login'),
    path('medico/register/', MedicoRegisterView.as_view(), name='medico_register'),
    path('medico/login/', MedicoLoginView.as_view(), name='medico_login'),
    path('medicos/', MedicoListView.as_view(), name='medicos_list'),
    path('consulta/agendar/', ConsultaCreateView.as_view(), name='consulta_create'),
    path('consultas/', ConsultaListView.as_view(), name='consultas_list'),
]
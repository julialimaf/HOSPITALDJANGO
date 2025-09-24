from django.urls import path
from .views import register_view, login_view, dashboard_view, medico_register_view, medico_login_view, medico_dashboard_view, meus_dados_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('meus-dados/', meus_dados_view, name='meus_dados'),
    path('medico/register/', medico_register_view, name='medico_register'),
    path('medico/login/', medico_login_view, name='medico_login'),
    path('medico/dashboard/', medico_dashboard_view, name='medico_dashboard'),
]
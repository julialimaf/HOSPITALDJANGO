from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PacientRegisterForm, MedicoRegisterForm
from django.contrib import messages

from rest_framework.response import Response
from .serializers import MyDataSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

def register_view(request):
    if request.method == 'POST':
        form = PacientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard')
    else:
        form = PacientRegisterForm()
    return render(request, 'account/register.html', {'form': form})

def medico_register_view(request):
    if request.method == 'POST':
        form = MedicoRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro médico realizado com sucesso!')
            return redirect('medico_dashboard')
    else:
        form = MedicoRegisterForm()
    return render(request, 'account/medico_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        password = request.POST['password']
        user = authenticate(request, cpf=cpf, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'CPF ou senha inválidos')
    return render(request, 'account/login.html')

def medico_login_view(request):
    if request.method == 'POST':
        crm = request.POST['crm']
        password = request.POST['password']
        user = authenticate(request, crm=crm, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login médico realizado!')
            return redirect('medico_dashboard')
        else:
            messages.error(request, 'CRM ou senha inválidos')
    return render(request, 'account/medico_login.html')

def dashboard_view(request):
    return render(request, 'account/dashboard.html', {'user': request.user})

def medico_dashboard_view(request):
    return render(request, 'account/medico_dashboard.html', {'user': request.user})

def meus_dados_view(request):
    return render(request, 'account/meusdados.html', {'user': request.user})

def mydata_view(request):
    return render(request, 'account/mydata.html', {'user': request.user})


def create_consultation(request):
    pass

class MyDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = MyDataSerializer(request.user)
        return Response(serializer.data)
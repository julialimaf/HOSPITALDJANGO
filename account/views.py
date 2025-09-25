from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import (
    PacientRegisterSerializer, 
    PacientLoginSerializer,
    MedicoRegisterSerializer,
    MedicoLoginSerializer,
    MedicoSerializer,
    ConsultaSerializer
)
from .models import Medico, Consulta, Pacient
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class PacientRegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'message': 'Endpoint para cadastro de paciente',
            'method': 'POST',
            'fields': ['cpf', 'email', 'first_name', 'last_name', 'phone', 
                       'birth_date', 'city', 'state', 'zip_code', 'password', 'password2']
        })

    def post(self, request):
        serializer = PacientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            paciente = serializer.save()
            user = User.objects.create_user(
                username=paciente.cpf,
                email=paciente.email,
                first_name=paciente.first_name,
                last_name=paciente.last_name,
                password=request.data['password']
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Paciente cadastrado com sucesso!',
                'token': token.key,
                'paciente_id': paciente.id,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PacientLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PacientLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login realizado com sucesso!',
                'token': token.key,
                'user_id': user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicoRegisterView(APIView):
    def get(self, request):
        return Response({
            'message': 'Endpoint para cadastro de médico',
            'method': 'POST',
            'fields': ['crm', 'email', 'first_name', 'last_name', 'phone', 'especialidade', 'password', 'password2']
        })
    
    def post(self, request):
        serializer = MedicoRegisterSerializer(data=request.data)
        if serializer.is_valid():
            medico = serializer.save()
            # Criar user padrão do Django para o token
            user = User.objects.create_user(
                username=medico.crm,
                email=medico.email,
                first_name=medico.first_name,
                last_name=medico.last_name
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Médico cadastrado com sucesso!',
                'token': token.key,
                'medico_id': medico.id,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MedicoLoginView(APIView):
    def post(self, request):
        serializer = MedicoLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login médico realizado com sucesso!',
                'token': token.key,
                'user_id': user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MedicoListView(APIView):
    def get(self, request):
        medicos = Medico.objects.all()
        serializer = MedicoSerializer(medicos, many=True)
        return Response(serializer.data)

class ConsultaCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ConsultaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            consulta = serializer.save()
            return Response({
                'message': f'Consulta agendada com sucesso! Código: {consulta.num_consulta}',
                'num_consulta': consulta.num_consulta,
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConsultaListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
       
        print(f"User: {request.user}")
        print(f"Username: {request.user.username}")
        
        
        try:
            paciente = Pacient.objects.get(cpf=request.user.username)
            print(f"Paciente encontrado: {paciente}")
            
            consultas = Consulta.objects.filter(paciente=paciente)
            print(f"Consultas encontradas: {consultas.count()}")
            
            
            todas_consultas = Consulta.objects.all()
            print(f"Total de consultas no banco: {todas_consultas.count()}")
            for c in todas_consultas:
                print(f"Consulta: {c.num_consulta} - Paciente: {c.paciente.cpf}")
            
            serializer = ConsultaSerializer(consultas, many=True)
            return Response(serializer.data)
        except Pacient.DoesNotExist:
            print(f"Paciente com CPF {request.user.username} não encontrado")
            return Response({'error': 'Paciente não encontrado'}, status=status.HTTP_404_NOT_FOUND)
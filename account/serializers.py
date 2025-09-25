from rest_framework import serializers 
from .models import Pacient, Medico, Consulta
from django.contrib.auth import authenticate, password_validation
from django.core import exceptions

class PacientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Pacient
        fields = ('cpf', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'city', 'state', 'zip_code', 'password', 'password2')
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        user = Pacient(
            cpf=attrs['cpf'],
            email=attrs['email'],
            first_name=attrs.get('first_name', ''),
            last_name=attrs.get('last_name', ''),
            phone=attrs.get('phone', ''),
            birth_date=attrs.get('birth_date'),
            city=attrs.get('city', ''),
            state=attrs.get('state', ''),
            zip_code=attrs.get('zip_code', '')
        )
        
        password = attrs.get('password')
        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = Pacient.objects.create_user(**validated_data)
        return user

class MedicoRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[password_validation.validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Medico
        fields = ('crm', 'email', 'first_name', 'last_name', 'phone', 'especialidade', 'password', 'password2')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = Medico.objects.create_user(**validated_data)
        return user

class PacientLoginSerializer(serializers.Serializer):
    cpf = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        cpf = attrs.get('cpf')
        password = attrs.get('password')
        
        if cpf and password:
            user = authenticate(request=self.context.get('request'), cpf=cpf, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.", code='authorization')
        else:
            raise serializers.ValidationError("Must include 'cpf' and 'password'.", code='authorization')
        
        attrs['user'] = user
        return attrs

class MedicoLoginSerializer(serializers.Serializer):
    crm = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        crm = attrs.get('crm')
        password = attrs.get('password')
        
        if crm and password:
            user = authenticate(request=self.context.get('request'), crm=crm, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.", code='authorization')
        else:
            raise serializers.ValidationError("Must include 'crm' and 'password'.", code='authorization')
        
        attrs['user'] = user
        return attrs

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ('id', 'crm', 'first_name', 'last_name', 'especialidade')

class ConsultaSerializer(serializers.ModelSerializer):
    medico_nome = serializers.CharField(source='medico.first_name', read_only=True)
    medico_especialidade = serializers.CharField(source='medico.especialidade', read_only=True)
    
    class Meta:
        model = Consulta
        fields = ('num_consulta', 'medico', 'medico_nome', 'medico_especialidade', 'data_consulta', 'motivo', 'status')
        read_only_fields = ('num_consulta', 'status')
    
    def create(self, validated_data):
        # Buscar o paciente pelo CPF do user
        user = self.context['request'].user
        try:
            paciente = Pacient.objects.get(cpf=user.username)
            validated_data['paciente'] = paciente
        except Pacient.DoesNotExist:
            raise serializers.ValidationError('Paciente não encontrado')
        return super().create(validated_data)
    

class MyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = ('cpf', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'city', 'state', 'zip_code')
from rest_framework import serializers 
from .models import Pacient
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
        
        user = Pacient(**attrs)
        password = attrs.get('password')
        
        errors = dict() 
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = Pacient.objects.create_user(**validated_data)
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
    

class MyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = ('cpf', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'city', 'state', 'zip_code')
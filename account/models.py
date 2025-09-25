from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, cpf=None, crm=None, email=None, password=None, **extra_fields):
        if not (cpf or crm):
            raise ValueError('CPF ou CRM REQUIRED')
        if not email:
            raise ValueError('EMAIL REQUIRED')
        
        email = self.normalize_email(email)
        if cpf:
            user = self.model(cpf=cpf, email=email, **extra_fields)
        else:
            user = self.model(crm=crm, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, cpf=None, crm=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf=cpf, crm=crm, email=email, password=password, **extra_fields)

class MedicoManager(BaseUserManager):
    def create_user(self, crm, email, password=None, **extra_fields):
        if not crm:
            raise ValueError('CRM REQUIRED')
        if not email:
            raise ValueError('EMAIL REQUIRED')
        
        email = self.normalize_email(email)
        user = self.model(crm=crm, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Pacient(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last_name", max_length=30)
    phone = models.CharField("Phone", max_length=11)
    birth_date = models.DateField("Birth Date", null=True, blank=True)
    city = models.CharField("City", max_length=30)
    state = models.CharField("State", max_length=30)
    zip_code = models.CharField("Zip Code", max_length=10)
    username = None
    user_type = models.CharField(max_length=10, default='pacient')
    groups = models.ManyToManyField('auth.Group', related_name='pacient_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='pacient_set', blank=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'account_pacient'

    def __str__(self):
        return str(self.cpf)

class Medico(AbstractUser):
    crm = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last_name", max_length=30)
    phone = models.CharField("Phone", max_length=11)
    especialidade = models.CharField("Especialidade", max_length=50)
    username = None
    user_type = models.CharField(max_length=10, default='medico')
    groups = models.ManyToManyField('auth.Group', related_name='medico_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='medico_set', blank=True)

    USERNAME_FIELD = 'crm'
    REQUIRED_FIELDS = ['email']
    objects = MedicoManager()
    
    class Meta:
        db_table = 'account_medico'

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.especialidade}"

import uuid

class Consulta(models.Model):
    num_consulta = models.CharField(max_length=8, unique=True, editable=False)
    paciente = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data_consulta = models.DateTimeField()
    motivo = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('agendada', 'Agendada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada')
    ], default='agendada')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.num_consulta:
            self.num_consulta = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'account_consulta'
    
    def __str__(self):
        return f"#{self.num_consulta} - {self.paciente.first_name} - {self.medico.first_name}"
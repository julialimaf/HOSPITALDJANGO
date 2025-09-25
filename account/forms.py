from django import forms
from .models import Pacient, Medico, Consulta

class PacientRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    class Meta:
        model = Pacient
        fields = ('cpf', 'email', 'first_name', 'last_name', 'phone', 'birth_date', 'city', 'state', 'zip_code', 'password', 'password2')
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class MedicoRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = Medico
        fields = ('crm', 'email', 'first_name', 'last_name', 'phone', 'especialidade', 'password', 'password2')
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ConsultaForm(forms.ModelForm):
    data_consulta = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = Medico.objects.all()
        self.fields['medico'].empty_label = "Selecione um médico"
    
    class Meta:
        model = Consulta
        fields = ('medico', 'data_consulta', 'motivo')
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3})
        }
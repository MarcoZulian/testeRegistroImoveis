from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from .models import Estado, Cidades, CircunscricaoTerritorial, EspecieDeDominio, ReservaLegalAverbada, Imovel, \
    ProprietarioPF, ProprietarioPJ, Proprietario
from .validators import validate_cpf, validate_cnpj


class ImovelForm(forms.Form):
    cns = forms.IntegerField(label="CNS")
    numero = forms.IntegerField(label="Número")
    dia = forms.DateField(label="Data")
    registro_tipo = forms.ChoiceField(label="Tipo de registro", choices=[('M', 'M'), ('B', 'B')],
                                      widget=forms.RadioSelect)
    proprietario_tipo = forms.ChoiceField(label="Tipo de proprietário",
                                          choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')],
                                          widget=forms.RadioSelect)
    cpf = forms.CharField(label="CPF", max_length=11, required=False)
    cnpj = forms.CharField(label="CNPJ", max_length=14, required=False)
    #cpf = forms.CharField(label="CPF", max_length=11, validators=[validate_cpf], required=False)
    #cnpj = forms.CharField(label="CNPJ", max_length=14, validators=[validate_cnpj], required=False)
    nome = forms.CharField(label="Nome Proprietário", max_length=100)
    endereco = forms.CharField(label="Endereço", max_length=100)
    #    estado = forms.ModelChoiceField(label="Estado", queryset=Estado.objects.all().order_by('nome'))
    #    cidade = forms.ModelChoiceField(label="Cidade", queryset=Cidades.objects.all().order_by('nome'))
    imovel_tipo = forms.ChoiceField(label="Tipo de imóvel", choices=[('R', 'Rural'), ('U', 'Urbano')],
                                    widget=forms.RadioSelect)
    inscricao_imobiliaria_municipal = forms.CharField(max_length=20, required=False)
    sncr = forms.CharField(label="SNCR", max_length=13, required=False)
    nirf = forms.CharField(label="NIRF", max_length=100, required=False)
    car = forms.CharField(label="CAR", max_length=100, required=False)
    cert_polig = forms.CharField(label="Certidão poligonal", max_length=100, required=False)
    reserva_legal = forms.ModelChoiceField(label="Reserva Legal Averbada",
                                           queryset=ReservaLegalAverbada.objects.all().order_by('descricao'),
                                           required=False)
    coordenadas_georref = forms.BooleanField(label="Coordenadas Georreferenciadas", required=False)
    circunscricao_territorial = forms.ModelChoiceField(label="Circunscrição",
                                                       queryset=CircunscricaoTerritorial.objects.all().order_by(
                                                           'descricao'))
    sobreposicao_de_area = forms.CharField(label="Sobreposição de área", max_length=200, required=False)
    cns_anterior = forms.IntegerField(label="CNS anterior", required=False)
    numero_anterior = forms.IntegerField(label="Número anterior", required=False)
    especie_de_dominio = forms.ModelChoiceField(label="Espécie de domínio",
                                                queryset=EspecieDeDominio.objects.all().order_by('descricao'))
    adm_direta = forms.BooleanField(label="Administração direta", required=False)
    especie_imovel = forms.CharField(label="Espécie de imóvel", max_length=50, required=False)
    legislacao_ou_ato_adm = forms.CharField(label="Legislação ou Ato Administrativo", max_length=200, required=False)
    encerramento = forms.BooleanField(label="Encerramento", required=False)
    bloqueio = forms.BooleanField(label="Bloqueio", required=False)
    usucapiao = forms.CharField(label="Usucapião", max_length=200, required=False)
    decisao = forms.CharField(label="Decisão", max_length=200, required=False)

    def save(self):
        pass


class ImovForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['cns', 'numero', 'dia', 'registro_tipo', 'endereco', 'coordenadas_georref',
                  'circunscricao_territorial', 'sobreposicao_de_area', 'cns_anterior', 'numero_anterior',
                  'especie_de_dominio', 'encerramento', 'bloqueio', 'usucapiao', 'decisao']


class PFForm(forms.ModelForm):
    nome = forms.CharField(label="Nome", max_length=100)

    class Meta:
        model = ProprietarioPF
        fields = ['cpf']


class PJForm(forms.ModelForm):
    nome = forms.CharField(label="Nome", max_length=100)

    class Meta:
        model = ProprietarioPJ
        fields = ['cnpj']


class ProprietarioForm(forms.ModelForm):
    proprietario_tipo = forms.ChoiceField(label="Tipo de proprietário",
                                          choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')],
                                          widget=forms.RadioSelect)
    documento = forms.CharField(max_length=14, label="CPF/CNPJ")

    class Meta:
        model = Proprietario
        fields = '__all__'

    def clean(self):
        if self.cleaned_data['DELETE']:
            return self.cleaned_data
        tipo = self.cleaned_data['proprietario_tipo']
        documento = self.cleaned_data['documento']

        if tipo == 'PF' and len(documento) != 11:
            raise ValidationError("O CPF deve conter 11 dígitos")
        elif tipo == 'PJ' and len(documento) != 14:
            raise ValidationError("O CNPJ deve conter 14 dígitos")

        return self.cleaned_data

class EnderecoForm(forms.Form):
    estado = forms.ModelChoiceField(label="Estado", queryset=Estado.objects.all().order_by('nome'))
    cidade = forms.ModelChoiceField(label="Cidade", queryset=Cidades.objects.all().order_by('nome'))

    def save(self):
        pass

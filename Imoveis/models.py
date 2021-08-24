from django.db import models


class Proprietario(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class ProprietarioPF(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proprietario', 'cpf'], name='proprietario_pf')
        ]

    proprietario = models.ForeignKey('Proprietario', on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.proprietario.nome + " (" + self.cpf + ")"


class ProprietarioPJ(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proprietario', 'cnpj'], name='proprietario_pj')
        ]

    proprietario = models.ForeignKey('Proprietario', on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.proprietario.nome + " (" + self.cnpj + ")"


class Estado(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Cidades(models.Model):
    estado = models.ForeignKey('Estado', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=30)

    def __str__(self):
        return self.nome + " - " + self.estado.nome


class CircunscricaoTerritorial(models.Model):
    descricao = models.CharField(max_length=30)

    def __str__(self):
        return self.descricao


class EspecieDeDominio(models.Model):
    descricao = models.CharField(max_length=20)

    def __str__(self):
        return self.descricao


class Imovel(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cns', 'numero'], name='codigo_imovel')
        ]

    cns = models.IntegerField()
    numero = models.IntegerField()
    dia = models.DateField()
    registro_tipo = models.CharField(max_length=1)
    proprietario = models.ManyToManyField('Proprietario')
    endereco = models.CharField(max_length=100)
    cidade = models.ManyToManyField('Cidades')
    coordenadas_georref = models.BooleanField()
    circunscricao_territorial = models.ForeignKey('CircunscricaoTerritorial', on_delete=models.DO_NOTHING)
    sobreposicao_de_area = models.CharField(max_length=200, default="", blank=True)
    # CNS e número anterior não foram colocados como Foreign Keys porque essa abordagem só funcionaria se todos os
    # registros fossem adicionados do mais antigo para o mais recente
    cns_anterior = models.IntegerField(null=True, blank=True)
    numero_anterior = models.IntegerField(null=True, blank=True)
    especie_de_dominio = models.ForeignKey('EspecieDeDominio', on_delete=models.DO_NOTHING)
    encerramento = models.BooleanField()
    bloqueio = models.BooleanField()
    usucapiao = models.CharField(max_length=200, default="", blank=True)
    decisao = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return str(self.cns) + " - " + str(self.numero)


class ImovelPublico(models.Model):
    imovel = models.OneToOneField('Imovel', on_delete=models.DO_NOTHING)
    adm_direta = models.BooleanField()
    especie_imovel = models.CharField(max_length=50, default="", blank=True)
    legistacao_ou_ato_adm = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return "Imóvel Público: " + str(self.imovel)


class ImovelUrbano(models.Model):
    imovel = models.OneToOneField('Imovel', on_delete=models.DO_NOTHING)
    inscricao_imobiliaria_municipal = models.CharField(max_length=20, default="", blank=True)

    def __str__(self):
        return "Imóvel Urbano: " + str(self.imovel)


class ReservaLegalAverbada(models.Model):
    descricao = models.CharField(max_length=11)

    def __str__(self):
        return self.descricao


class ImovelRural(models.Model):
    imovel = models.OneToOneField('Imovel', on_delete=models.DO_NOTHING)
    sncr = models.CharField(max_length=13, default="", blank=True)
    nirf = models.CharField(max_length=100, default="", blank=True)
    car = models.CharField(max_length=100, default="", blank=True)
    cert_polig = models.CharField(max_length=100, default="", blank=True)
    reserva_legal = models.ForeignKey('ReservaLegalAverbada', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return "Imóvel Rural: " + str(self.imovel)

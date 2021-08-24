from django.shortcuts import render
from django.forms import modelform_factory, modelformset_factory, formset_factory

from .models import Imovel, Cidades, ImovelRural, ImovelUrbano, ImovelPublico, ProprietarioPF, ProprietarioPJ, \
    Proprietario
from .forms import ImovForm, EnderecoForm, ProprietarioForm

ImovelRuralForm = modelform_factory(ImovelRural, exclude=["imovel"])
ImovelUrbanoForm = modelform_factory(ImovelUrbano, exclude=["imovel"])
ImovelPublicoForm = modelform_factory(ImovelPublico, exclude=["imovel"])
PForm = formset_factory(ProprietarioForm, extra=0, can_delete=True, min_num=1)
EndForm = formset_factory(EnderecoForm, extra=0, can_delete=True, min_num=1)

def new(request):
    if request.method == "POST":
        form = ImovForm(request.POST)
        form2 = ImovelRuralForm(request.POST)
        form3 = ImovelUrbanoForm(request.POST)
        form7 = EndForm(request.POST)
        form8 = PForm(request.POST, prefix='form2')
        form9 = ImovelPublicoForm(request.POST)

        forms_to_validate = [form, form7, form8, form3 if request.POST['tipo_imovel'] == 'U' else form2]
        if request.POST['especie_de_dominio'] != 1:
            forms_to_validate.append(form9)

        for f in forms_to_validate:
            if f.is_valid():
                print('é válido')
                continue
            else:
                return render(request, "Imoveis/new.html", {"form": form,
                                                            "form2": form2,
                                                            "form3": form3,
                                                            "formset": form7,
                                                            "formset2": form8,
                                                            "form9": form9})

        imovel = Imovel(**form.cleaned_data)
        imovel.save()
        if request.POST['tipo_imovel'] == 'U':
            imovel_r_u = ImovelUrbano(**form3.cleaned_data)
        else:
            imovel_r_u = ImovelRural(**form2.cleaned_data)
        imovel_r_u.imovel = imovel
        imovel_r_u.save()

        if request.POST['especie_de_dominio'] != 1:
            imovel_publico = ImovelPublico(**form9.cleaned_data)
            imovel_publico.imovel = imovel
            imovel_publico.save()

        for f in form7:
            cd = f.cleaned_data
            imovel.cidade.add(cd['cidade'])

        for f in form8:
            cd = f.cleaned_data
            print(cd)
            prop = Proprietario()
            prop.nome = cd['nome']
            prop.save()
            imovel.proprietario.add(prop)
            if cd['proprietario_tipo'] == "PF":
                proppf = ProprietarioPF()
                proppf.proprietario = prop
                proppf.cpf = cd['documento']
                proppf.save()
            else:
                proppj = ProprietarioPJ()
                proppj.proprietario = prop
                proppj.cnpj = cd['documento']
                proppj.save()
            print(cd)


 #       if form.is_valid():
 #           imovel = Imovel(**form.cleaned_data)
 #           print(request.POST)
 #           tipo_imovel = request.POST['tipo_imovel']
 #           if tipo_imovel == 'U':
 #               if form3.is_valid():
 #                   imovel_r_u = ImovelUrbano(**form3.cleaned_data)
 #           else:
 #               if form2.is_valid():
 #                   imovel_r_u = ImovelRural(**form2.cleaned_data)
 #           imovel_r_u.imovel = imovel

 #           is_imovel_publico = request.POST['especie_de_dominio'] != 1
 #           if is_imovel_publico and form9.is_valid():
 #               imovel_publico = ImovelPublico(**form9.cleaned_data)
 #               imovel_publico.imovel = imovel

 #           imovel.save()
 #           imovel_publico.save()
 #           imovel_r_u.save()

 #           if form7.is_valid():
 #               print("Form7 válido")
 #               for f in form7:
 #                   cd = f.cleaned_data
 #                   imovel.cidade.add(cd['cidade'])
 #                   print(cd)

 #           else:
 #               print("Form7 invalido")

 #           if form8.is_valid():
 #               print("Form8 válido")
 #               for f in form8:
 #                   cd = f.cleaned_data
 #                   print(cd)
 #                   prop = Proprietario()
 #                   prop.nome = cd['nome']
 #                   prop.save()
 #                   imovel.proprietario.add(prop)
 #                   if cd['proprietario_tipo'] == "PF":
 #                       proppf = ProprietarioPF()
 #                       proppf.proprietario = prop
 #                       proppf.cpf = cd['documento']
 #                       proppf.save()
 #                   else:
 #                       proppj = ProprietarioPJ()
 #                       proppj.proprietario = prop
 #                       proppj.cnpj = cd['documento']
 #                       proppj.save()
 #                   print(cd)
 #           else:
 #               print("Form8 invalido")

 #           print(imovel)
 #           print("Valido")

    else:
        form = ImovForm()
        form2 = ImovelUrbanoForm()
        form3 = ImovelRuralForm()
        form7 = EndForm()
        form8 = PForm(prefix='form2')
        form9 = ImovelPublicoForm()

    return render(request, "Imoveis/new.html", {"form": form,
                                                "form2": form2,
                                                "form3": form3,
                                                "formset": form7,
                                                "formset2": form8,
                                                "form9": form9})

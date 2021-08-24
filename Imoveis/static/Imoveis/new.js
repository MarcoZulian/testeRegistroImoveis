function hideFieldAndLabel(id) {
     var full_id = '#id_' + id;
     var label = 'label[for="id_' + id + '"]'
     $(full_id).hide();
     $(label).hide();
}

function showFieldAndLabel(id) {
     var full_id = '#id_' + id;
     var label = 'label[for="id_' + id + '"]'
     $(full_id).show();
     $(label).show();
}

$('#pessoa_fisica').change(function() {
    $('#pessoa_juridica_form').hide();
    $('#pessoa_fisica_form').show();
});

$('#pessoa_juridica').change(function() {
    $('#pessoa_juridica_form').show();
    $('#pessoa_fisica_form').hide();
});

$('#imovel_urbano').change(function() {
    ["sncr", "nirf", "car", "cert_polig", "reserva_legal"].forEach(hideFieldAndLabel);
    showFieldAndLabel("inscricao_imobiliaria_municipal");
});

$('#imovel_rural').change(function() {
    ["sncr", "nirf", "car", "cert_polig", "reserva_legal"].forEach(showFieldAndLabel);
    hideFieldAndLabel("inscricao_imobiliaria_municipal");
});

$('#add_items_cidade').click( function() {
    var form_index = $('#id_form-TOTAL_FORMS').val();
    $('#form_set_cidade').append($('#empty_form_cidade').html().replace(/__prefix__/g, form_index));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_index) + 1);
})

$('#add_items_proprietario').click( function() {
    var form_index = $('#id_form2-TOTAL_FORMS').val();
    $('#form_set_proprietario').append($('#empty_form_proprietario').html().replace(/__prefix__/g, form_index));
    $('#id_form2-TOTAL_FORMS').val(parseInt(form_index) + 1);
})

$('#id_especie_de_dominio').change(function () {
   if ($('#id_especie_de_dominio').val() != 1) {
        $('#form_publicos').show()
   } else {
        $('#form_publicos').hide()
   }
});













$('#id_proprietario_tipo').change(function() {
    if ($('#id_proprietario_tipo_0').is(':checked')) {
        hideFieldAndLabel("cnpj");
        showFieldAndLabel("cpf");
    } else {
        showFieldAndLabel("cnpj");
        hideFieldAndLabel("cpf");
    };
});


$('#id_imovel_tipo').change(function() {
    if ($('#id_imovel_tipo_0').is(':checked')) {
        ["sncr", "nirf", "car", "cert_polig", "reserva_legal"].forEach(showFieldAndLabel);
        hideFieldAndLabel("inscricao_imobiliaria_municipal");
    } else {
        ["sncr", "nirf", "car", "cert_polig", "reserva_legal"].forEach(hideFieldAndLabel);
        showFieldAndLabel("inscricao_imobiliaria_municipal");
    };
});


$('#id_especie_de_dominio').change(function () {
   if ($('#id_especie_de_dominio').val() == 1) {
        ['adm_direta', 'especie_imovel', 'legislacao_ou_ato_adm'].forEach(hideFieldAndLabel);
   } else {
        ['adm_direta', 'especie_imovel', 'legislacao_ou_ato_adm'].forEach(showFieldAndLabel);
   }
});

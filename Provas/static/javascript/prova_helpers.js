// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function salvar_valor(id_questao, valor_questao, id_prova) {

    toastr.options = {
        "debug": false,
        "positionClass": "toast-bottom-right",
        "onclick": null,
        "fadeIn": 300,
        "fadeOut": 1000,
        "timeOut": 5000,
        "extendedTimeOut": 1000,
        "progressBar": true,
    };

    valor_questao = valor_questao.replace(",", ".");

    var dataToSend = {id_prova: id_prova, id_questao: id_questao, valor_questao: valor_questao};
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        cache: false
    });

    $.ajax({
        url: '/atualiza_valor_questao/',
        type: 'POST',
        contentType: 'application/x-www-form-urlencoded',
        dataType: 'json',
        data: JSON.stringify(dataToSend),

        complete: function(result) {
            if(result.statusText === 'OK') {

                let statusTextAndValue = result.responseText.split(":");

                if(statusTextAndValue[0] === 'OK') {
                    toastr.success("Mudança de valor realizada com sucesso", "Prova atualizada");
                }
                else if(statusTextAndValue[0] === 'ACIMA'){
                    toastr.warning("Mudança de valor atualizada. A soma total das questões está acima do valor da prova!", "Prova atualizada")
                }
                else if(statusTextAndValue[0] === 'ABAIXO') {
                    toastr.warning("Mudança de valor atualizada. A soma total das questões está abaixo do valor da prova!","Prova atualizada")
                }

                $('#soma_valores').html("Valor atual da soma das questões: " + parseFloat(statusTextAndValue[1]).toLocaleString());

            }
            else {
                toastr.error("Erro ao atualizar prova!")
            }
        }

    });
}

function mudar_ordem(id_questao, ordem, dir, id_prova) {

    var dataToSend = {id_prova: id_prova, id_questao: id_questao, ordem_atual: ordem, direcao: dir};
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        cache: false
    });

    $.ajax({
        url: '/atualiza_ordem_questao/',
        type: 'POST',
        contentType: 'application/x-www-form-urlencoded',
        dataType: 'json',
        data: JSON.stringify(dataToSend),

        complete: function(result) {
            if (result.statusText === "OK") {
                window.location.reload();
            }
        }
    });
}
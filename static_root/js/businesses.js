
$(document).ready(function () {
    $('#cardDiv').hide();
    $('#payBtn').hide();
    if ($('#cartContent').attr("data-empty")) {
        $('#removeFrom').hide();
    }
});

$('.addTo').on('click', function(e) {
   e.stopPropagation();
   e.stopImmediatePropagation();
   $.ajax({
        url: $(this).attr("data-url"),
        data: {
          'pk': $(this).attr("data-pk"),
          'cartID': $('#cartTitle').attr("data-id")
        },
        success: function (response) {
            location.reload();
        }
    });
});

$('.removeFrom').on('click', function (e) {
   e.stopPropagation();
   e.stopImmediatePropagation();
   $.ajax({
        url: $(this).attr("data-url"),
        data: {
          'pk': $(this).attr("data-pk"),
          'cartID': $('#cartTitle').attr("data-id")
        },
        success: function (response) {
            location.reload();
        }
    });
});

$('#payBtn').on('click', function (e) {
    e.stopPropagation();
    e.stopImmediatePropagation();

    var address = `${$('#inputAddress').val()} ${$('#inputAddress2').val()} ${$('#inputCity').val()} ${$('#inputPostal').val()}`;

    $.ajax({
        url: $(this).attr("data-url"),
        method: 'POST',
        data: {
            'name': $('#name').val(),
            'number': $('#number').val(),
            'cvc': $('#cvc').val(),
            'expiry': $('#exp').val(),
            'quote': $('#payBtn').attr('data-quote'),
            'cartID': $('#cartTitle').attr('data-id'),
            'address': address,
            'coupon': $('#couponCode').val()
        },
        success: function (response) {
            var text = $('#messageBox').html();
            if (response['errors'].length > 0) {
                for (var error in response['errors']) {
                    text += `<div class="alert alert-danger alert-dismissible fade show" role="alert">${response['errors'][error]}<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>`
                }
            } else {
                text += `<div class="alert alert-success alert-dismissable fade show" role="alert">Delivery Created!</div>`;
                if ('discount' in response) {
                    text += `<div class="alert alert-success alert-dismissable fade show" role="alert">${response['discount']}</div>`;
                }
                $('#name').val("");
                $('#number').val("");
                $('#cvc').val("");
                $('#exp').val("");
                $('#payBtn').attr('data-quote', "");
            }
            $('#messageBox').html(text);
        }
    })
});

$('#addressForm').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
            'address1': $('#inputAddress').val(),
            'address2': $('#inputAddress2').val(),
            'city': $('#inputCity').val(),
            'zip': $('#inputPostal').val()
        },
        success: function(response) {
            if (response == "True") {
                var address = `${$('#inputAddress').val()} ${$('#inputAddress2')} ${$('#inputCity')} ${$('#inputPostal')}`;
                $('#messageBox').html(" ");
                $.ajax({
                    url: $('#quoteSubmit').attr('data-url'),
                    data: {
                        'storeID': $('#storeID').attr('data-id'),
                        'cartID': $('#cartTitle').attr('data-id'),
                        'address1': $('#inputAddress').val(),
                        'address2': $('#inputAddress2').val(),
                        'city': $('#inputCity').val(),
                        'zip': $('#inputPostal').val()
                    },
                    success: function (response) {
                        var quote = response;
                        $('#payBtn').attr('data-quote', quote);
                        if ($("#storeID").attr('data-user') == 'auth') {
                            $.ajax({
                                url: $('#closeBtn').attr('data-url'),
                                method: 'POST',
                                success: function (response) {
                                    $('#formDiv').hide();
                                    $('#quoteSubmit').hide();
                                    var dropoff = `${$('#inputAddress2').val()} ${$('#inputAddress').val()} ${$('#inputCity').val()} ${$('#inputPostal').val()}`;
                                    var cards = `<h5>Select A Payment Method ($${quote})</h5><ul class="list-group mx-auto m-2">`;
                                    var i = 0;
                                    for (var obj in response["data"]) {
                                        i++;
                                        cards += `<li class="list-group-item"><i class="fab fa-cc-${response["data"][obj]["card"]["brand"]}"></i> •••• •••• •••• ${response["data"][obj]["card"]["last4"]} | ${JSON.stringify(response["data"][obj]["card"]["exp_month"])}/${JSON.stringify(response["data"][obj]["card"]["exp_year"])}<a href="${$('#closeBtn').attr('data-final')}?card=${response["data"][obj]["id"]}&quote=${quote}&pickup=${$('#storeAddress').html()}&dropoff=${dropoff}&cartID=${$('#cartTitle').attr('data-id')}&coupon=${$('#couponCode').val()}" class="fas fa-check text-success ml-4"></a></li>`
                                    }
                                    if (i === 0) {
                                        cards += `<li class="list-group-item">You do not have a saved payment method. Add one <a href="${$('#closeBtn').attr('data-payment')}">here.</a></li>`
                                    }

                                    cards += `</ul>`
                                    $("#paymentDiv").html(cards);
                                }
                            })
                        } else {
                            $('#formDiv').hide();
                            $('#cardDiv').show();
                            $('#quoteSubmit').hide();
                            $('#payBtn').show();
                        }
                    }
                })
            } else {
                $('#messageBox').html($('#messageBox').html() + `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                  Address was not verified successfully. Please check your input and try again.
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                `
                );
            }
        }
    });
});


$(document).ready(function () {
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
          'pk': $(this).attr("data-pk")
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
          'pk': $(this).attr("data-pk")
        },
        success: function (response) {
            location.reload();
        }
    });
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
                                    cards += `<li class="list-group-item"><i class="fab fa-cc-${response["data"][obj]["card"]["brand"]}"></i> •••• •••• •••• ${response["data"][obj]["card"]["last4"]} | ${JSON.stringify(response["data"][obj]["card"]["exp_month"])}/${JSON.stringify(response["data"][obj]["card"]["exp_year"])}<a href="${$('#closeBtn').attr('data-final')}?card=${response["data"][obj]["id"]}&quote=${quote}&pickup=${$('#storeAddress').html()}&dropoff=${dropoff}&cartID=${$('#cartTitle').attr('data-id')}" class="fas fa-check text-success ml-4"></a></li>`
                                }
                                if (i === 0) {
                                    cards += `<li class="list-group-item">You do not have a saved payment method. Add one <a href="${$('#closeBtn').attr('data-payment')}">here.</a></li>`
                                }

                                cards += `</ul>`
                                $("#paymentDiv").html(cards);
                            }
                        })
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

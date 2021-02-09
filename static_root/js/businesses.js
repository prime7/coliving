
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
                alert('Address Verified');
            } else {
                alert('Address Not Verified');
            }
        }
    });
});

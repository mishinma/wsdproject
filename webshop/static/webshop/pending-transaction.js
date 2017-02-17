// $('#id_is_gift').click(function() {
//   giftRecipientSelector = $('#gift-recipient-selector');
//   if(this.checked) {
//     giftRecipientSelector.show();
//   } else {
//     giftRecipientSelector.hide();
//   }
// });

$(document).ready(function () {
    'use strict';
    $("#pending-transaction-form").submit(function (evt) {
        evt.preventDefault();
        var form = this;
        var amount = $.trim($("#game-price").text());

        $.ajax({
            method: "POST",
            data: {'amount': amount},
            dataType: "json",
            success: function (data) {
                populateForm(data);
                form.submit()
            },
            error: function () {
                $('#ajax-error').show();
            }
        });
    });
});

function populateForm(data) {
    'use strict';
    $("#id_pid").val(data.pid);
    $("#id_sid").val(data.sid);
    $("#id_amount").val(data.amount);
    $("#id_success_url").val(data.success_url);
    $("#id_cancel_url").val(data.cancel_url);
    $("#id_error_url").val(data.error_url);
    $("#id_checksum").val(data.checksum);
}

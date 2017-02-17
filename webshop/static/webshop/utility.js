// $('#id_is_gift').click(function() {
//   giftRecipientSelector = $('#gift-recipient-selector');
//   if(this.checked) {
//     giftRecipientSelector.show();
//   } else {
//     giftRecipientSelector.hide();
//   }
// });
$(document).ready(function() {
  $("#pending-transaction-form").submit(function(e){
    e.preventDefault();
    var form = this;
    // if($('#id_is_gift').is(':checked')) {
    //   alert('Gift to ' + $('select[name=gift_recipient]').val())
    // }
    var data = {
      'game': {{game.id}},
      'amount': {{price}},
      'csrfmiddlewaretoken': '{{csrf_token}}'
    };
    $.ajax({
      method: "POST",
      url: "{% url 'webshop:purchase-pending' %}",
      data: data,
      statusCode: {
        200: function(data) {
          populateForm(data);
          form.submit();
        },
        400: function() {
          $('#ajax-error').show();
        }
      }
    });
  });
});

function populateForm(data) {
  $("#id_pid").val(data.pid);
  $("#id_sid").val(data.sid);
  $("#id_amount").val(data.amount);
  $("#id_success_url").val(data.success_url);
  $("#id_cancel_url").val(data.cancel_url);
  $("#id_error_url").val(data.error_url);
  $("#id_checksum").val(data.checksum);
}

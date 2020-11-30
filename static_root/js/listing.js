
$(document).on("click","#sfv_form_submit", sfv_form_submit);

function sfv_form_submit(){
  var ad_id   = $('#ad_id').html();
  var sfv_name = $('[name="sfv_name"]').val();
  var sfv_phone = $('[name="sfv_phone"]').val();
  var sfv_notes = $('[name="sfv_notes"]').val();
  var sfv_avail = [];

  if(!ad_id || !sfv_name || !sfv_phone || !sfv_notes){
    alert("Please fill all the fields");
    return;
  }


  $('#ama_area').children().each(function() {
      sfv_avail.push($(this).val());
  });

   var sfv_avail_string = sfv_avail.toString();
   if(!sfv_avail_string){
     alert("Please select a day");
     return;
   }


  var data = {
    'ad_id' : ad_id,
    'sfv_name' : sfv_name,
    'sfv_phone' : sfv_phone,
    'sfv_notes' : sfv_notes,
    'sfv_avail' : sfv_avail_string,
  }


  console.log(data);

  $.ajax({
      url:'/rentals/ajax/sqv/application',
      data:data,
      async: true,
      success:function(result_data) {
        
          if(result_data == 'error'){
            alert("Please try again later. There is a technical difficulty.");
            window.location.reload();
          }
          else{
            alert("Thanks for you Availabilty. We will reply soon. Please check your dashboard.");
            window.location.reload();
          }
      },
      error:function(result_data){
         console.log(result_data);
          return ;
      }
  });

  console.log(data);

}

$(document).on("click","#add_more_avail", add_more_avail);

function add_more_avail(){
  var el= $("#ama_area");
  var el_len = el.children().length;

  if(el_len >= 3){
    alert("Maximum 3 Days allowed");
    return;
  }
  var dd = $('<input>').attr({
      type : 'date',
      id: 'foo',
      name: 'bar'
  });

  el.append(dd);
}

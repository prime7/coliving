
$(document).on("click","#sfv_form_submit", sfv_form_submit);


function sfv_form_submit(){
  alert("erawsd");
  var ad_id   = $('#ad_id').html();
  var sfv_name = $('[name="sfv_name"]').val();
  var sfv_phone = $('[name="sfv_phone"]').val();
  var sfv_num = $('[name="sfv_num"]').val();
  var sfv_notes = $('[name="sfv_notes"]').val();
  var sfv_mon = $('[type=radio][name="sfv_mon"]:checked').val();
  var sfv_tue = $('[type=radio][name="sfv_tue"]:checked').val();
  var sfv_wed = $('[type=radio][name="sfv_wed"]:checked').val();
  var sfv_thr = $('[type=radio][name="sfv_thr"]:checked').val();
  var sfv_fri = $('[type=radio][name="sfv_fri"]:checked').val();
  var sfv_sat = $('[type=radio][name="sfv_sat"]:checked').val();
  var sfv_sun = $('[type=radio][name="sfv_sun"]:checked').val();

  var data = {
    'ad_id' : ad_id,
    'sfv_name' : sfv_name,
    'sfv_phone' : sfv_phone,
    'sfv_num' : sfv_num,
    'sfv_notes' : sfv_notes,
    'sfv_mon' : sfv_mon,
    'sfv_tue' : sfv_tue,
    'sfv_wed' : sfv_wed,
    'sfv_thr' : sfv_thr,
    'sfv_fri' : sfv_fri,
    'sfv_sat' : sfv_sat,
    'sfv_sun' : sfv_sun,
  }

 console.log(data);
  $.ajax({
      url:'/rentals/ajax/sqv/application',
      data:data,
      async: true,
      success:function(result_data) {
          alert("nice");
      },
      error:function(result_data){
         console.log(result_data);
          return ;
      }
  });

  console.log(data);

}

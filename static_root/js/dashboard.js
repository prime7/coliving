
$(document).on('click' , '#dashnavbar3_click' , dashnavbar3_click);


function dashnavbar3_click(){
   var target_el      = $(this).parent().parent().children().eq(1)
   var current_state  = target_el.css('display').trim();


   if(current_state == 'none')
   {
       target_el.css('display' , 'flex');
       $(this).parent().children().eq(1).css('display' , 'flex');
       $(this).parent().children().eq(0).css('display' , 'none');
   }

   else if(current_state == 'flex')
   {
       target_el.css('display' , 'none');
          $(this).parent().children().eq(1).css('display' , 'none');
          $(this).parent().children().eq(0).css('display' , 'flex');
   }
}


$(document).on('click' , '#dmc_click1' , dmc_click1);
function dmc_click1(){

   var target_el      = $(this).parent().parent().parent().children().eq(1)
   var current_state  = target_el.css('display').trim();


   if(current_state == 'none')
   {
       target_el.css('display' , 'flex');
       $(this).children().eq(1).css('display' , 'flex');
       $(this).children().eq(0).css('display' , 'none');
   }

   else if(current_state == 'flex')
   {
       target_el.css('display' , 'none');
       $(this).children().eq(1).css('display' , 'none');
       $(this).children().eq(0).css('display' , 'flex');
   }
}


$(document).on('click' , '#dnav3_updown' , dmc_click1);
function dmc_click1(){
   //lesson.
}




$(document).on('change', "#id_dashboard_types" , dashtype_submit);
function dashtype_submit(){
  var selected_value = $(this).find('option').filter(':selected').val();
  //alert(selected_value);
  $("#dash_type_form").submit();
}

$(document).on('click', "#listing_ads_oc" , listing_ads_oc);
function listing_ads_oc(){
  var el = $(this).parent().parent().children().eq(1);
  var val = el.css('display');

  if(val.trim() == 'flex'){
      el.css('display' , 'none');
  }
  else if(val.trim() == 'none'){
      el.css('display' , 'flex');
  }
}


//Book Scheduling.
$(document).on('click' , '#select_sfv_day' , select_sfv_day);
function select_sfv_day(){
   var sfv_id = $(this).parent().children().eq(0).html();
   var data = { 'sfv_id' : sfv_id };

   $.ajax({
       url:'select_day/',
       data:data,
       async: true,
       success:function(result_data) {
           if(result_data == 'error'){
             alert("Only 1 day can be selected.");
           }
           else if(result_data == 'done'){
             alert("Sent. Please wait for the acceptance response.");
           }
       },
       error:function(result_data){
          console.log(result_data);
           return ;
       }
   });
}





//Accept Scheduling.
$(document).on('click' , '#accept_sfv_day' , accept_sfv_day);
function accept_sfv_day(){
   var sfv_id = $(this).parent().children().eq(0).html();
   var data = { 'sfv_id' : sfv_id };

   $.ajax({
       url:'accept_day/',
       data:data,
       async: true,
       success:function(result_data) {
           if(result_data == 'error'){
             alert("Only 1 day can be selected.");
           }
           else if(result_data == 'done'){
             alert("Sent. Please wait for the acceptance response.");
             window.location.reload();
           }
       },
       error:function(result_data){
          console.log(result_data);
           return ;
       }
   });
}


$(document).on('click' , '#land_delete_listing' , land_delete_listing);
function land_delete_listing(){
  var ad_id = $(this).parent().parent().children().eq(0).children().eq(0).text();

  var data = {'ad_id' : ad_id};
  $.ajax({
      url:'delete/listing/',
      data:data,
      async: true,
      success:function(result_data) {
          alert("Listing has been deleted");
          window.location.reload();

      },
      error:function(result_data){
         console.log(result_data);
          return ;
      }
  });
}

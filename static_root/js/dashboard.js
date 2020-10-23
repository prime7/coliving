
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



$(document).on('change', "#id_dashboard_types" , dashtype_submit);
function dashtype_submit(){
  var selected_value = $(this).find('option').filter(':selected').val();
  alert(selected_value);
  $("#dash_type_form").submit();
}

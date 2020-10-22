
$(document).on('click' , '#dashnavbar3_click' , dashnavbar3_click);
function dashnavbar3_click(){

   var target_el      = $(this).parent().parent().children().eq(1)
   var current_state  = target_el.css('display').trim();
   if(current_state == 'none')
   {
       target_el.css('display' , 'flex');
   }

   else if(current_state == 'flex')
   {
       target_el.css('display' , 'none');
   }


}

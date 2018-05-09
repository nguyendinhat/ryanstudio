var $form_login = $("#form-login");
var $form_guest = $("#form-guest");
$form_guest.toggle();
$("#btn-guest").on("click", function(e) {   
    $form_guest.toggle();
    $form_login.toggle();
});
$("#btn-login").on("click", function(e) { 
    $form_login.toggle();
    $form_guest.toggle();
});
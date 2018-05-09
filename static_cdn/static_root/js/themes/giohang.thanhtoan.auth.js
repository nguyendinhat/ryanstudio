// Visa, MasterCard, American Express, Diners Club, Discover, and JCB cards
// const regex = /^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/g;
// const str = ``;
// let m;

// while ((m = regex.exec(str)) !== null) {
//     // This is necessary to avoid infinite loops with zero-width matches
//     if (m.index === regex.lastIndex) {
//         regex.lastIndex++;
//     }
    
//     // The result can be accessed through the `m`-variable.
//     m.forEach((match, groupIndex) => {
//         console.log(`Found match, group ${groupIndex}: ${match}`);
//     });
// }
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
var $credit_card = $("#payment-method-credit");
$credit_card.toggle();

$('#pttt-credit').on('ifChanged', function(event){
    $credit_card.toggle();
});

(function ($) {   
    $(document).ready(function() {
        var current_fs, next_fs, previous_fs;
        var form        = $("#msform");
        var hoten       = $("#hoten");
        var sdt         = $("#sdt");
        var diachi      = $("#diachi");        
        var sothe       = $("#sothe");
        var hotenthe    = $("#hotenthe");
        var ngayhethan  = $("#ngayhethan");
        var ccv         = $("#ccv");
        var tinhthanh, quanhuyen, xaphuong = null;  

        $('input[value="cod"]').prop('checked', true);

        $('#tinhthanh').change(function(){
            if ($(this).find(':selected').attr("rel")==-1){
                tinhthanh = null;
            } else {                
                tinhthanh = $(this).find(':selected').attr("rel");
            }
            console.log(tinhthanh);
        });
        $('#quanhuyen').change(function(){
            if ($(this).find(':selected').attr("rel")==-1){
                quanhuyen = null;
            } else {                
                quanhuyen = $(this).find(':selected').attr("rel");
            }
            console.log(quanhuyen);
        });
        $('#xaphuong').change(function(){
            if ($(this).find(':selected').attr("rel")==-1){
                xaphuong = null;
            } else {                
                xaphuong = $(this).find(':selected').attr("rel");
            }
            console.log(xaphuong);
        });
        $(".next").click(function(){
            var check1 = true;
            var check2 = true;
            var sdt_reg = new RegExp('^(01[2689]|09)[0-9]{8}$');
            
            if (hoten.val().length < 5) {
                showValidate(hoten);
                check1=false;
            }

            if (!sdt_reg.test(sdt.val())) {
                showValidate(sdt);
                check1=false;
            }

            if (diachi.val() == ""){
                showValidate(diachi);
                check1 = false;
            }
            if (tinhthanh == null){
                showValidate($('#tinhthanh'));
                check1 = false;
            }
            if (quanhuyen == null){
                showValidate($('#quanhuyen'));
                check1 = false;
            }
            if (xaphuong == null){
                showValidate($('#xaphuong'));
                check1 = false;
            }

            if (($('input[name=pttt]:radio:checked').val()=="credit")) {
                if (sothe.val() == ""){
                    showValidate(sothe);
                    check2 = false;
                }
                if (hotenthe.val() == ""){
                    showValidate(hotenthe);
                    check2 = false;
                }
                if (ngayhethan.val() == ""){
                    showValidate(ngayhethan);
                    check2 = false;
                }
                if (ccv.val() == ""){
                    showValidate(ccv);
                    check2 = false;
                }
            } 
            
            if (check1 && check2){
                current_fs = $(this).parent();
                next_fs = $(this).parent().next();
                current_fs.attr("class", "animated fadeOut");
                next_fs.show();
                next_fs.attr("class", "animated fadeIn");         
                current_fs.hide();            
                $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
                beforeCheckout();
            }
        });
        $(".previous").click(function(){
            current_fs = $(this).parent();
            previous_fs = $(this).parent().prev();
            current_fs.attr("class", "animated fadeOut");
            previous_fs.show();
            previous_fs.attr("class", "animated fadeIn");            
            current_fs.hide();            
            $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");           
        });
    });
    function beforeCheckout() {
        $(".pre-hoten").text($("#hoten").val());
        $(".pre-sdt").text($("#sdt").val());
        $(".pre-diachi").text($("#diachi").val()+', ' + $('#xaphuong').find(':selected').attr("path"));
        $(".pre-pttt").text($('input[name=pttt]:radio:checked').attr("text"));
        $(".pre-credit-sothe").text($("#sothe").val());
        $(".pre-credit-hotenthe").text($("#hotenthe").val());
        $(".pre-credit-ngayhethan").text($("#ngayhethan").val());
        $(".pre-credit-ccv").text($("#ccv").val());
    }
    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }
    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }
})(jQuery);

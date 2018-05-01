$("#amount").text(formatMoney(parseInt($("#amount").attr("data-tongcong"))));
// Count Input (Quantity)
//------------------------------------------------------------------------------
$(".incr-btn").on("click", function(e) {
    var $button     = $(this);
    var $item       = $button.parent().find('.item-giohang');
    var $total      = $button.parent().parent().find('.item-total');
    
    var sanpham     = $item.attr("data-sanpham");
    var limit       = parseInt($item.attr("data-soluong-limit"));
    var thanhtien   = parseInt($total.attr("data-thanhtien"));
    var dongia      = parseInt($item.attr("data-dongia"));
    var oldValue    = $button.parent().find('.quantity').val();
    var newVal      = 1;
    $button.parent().find('.incr-btn[data-action="decrease"]').removeClass('inactive');
    if ($button.data('action') == "increase") {
        if (limit ==0) {
            newVal = 0;
            $button.addClass('inactive');
        } else {
            newVal = parseInt(oldValue) + 1;
            if (newVal > limit) {
                newVal = limit;
            }
        } 
        thanhtien = newVal * dongia;
    } else {
        // Don't allow decrementing below 1
        if (limit ==0) {
            newVal = 0;
            $button.addClass('inactive');
        } else {
            if (oldValue > 1) {
                newVal = parseInt(oldValue) - 1;				
            } else {
                newVal = 1;
                $button.addClass('inactive');
            }
        }        
        thanhtien = newVal * dongia;
    }		
    $total.text(formatMoney(thanhtien));
    $total.attr("data-thanhtien",thanhtien);
    $button.parent().find('.quantity').val(newVal);
    $('#amount').attr("data-tongcong",tinhTongTien(get_item()));
    $("#amount").text(formatMoney(parseInt($("#amount").attr("data-tongcong"))));
    if (oldValue!=newVal){
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        var data = "csrfmiddlewaretoken="+csrftoken+"&id_sanpham="+sanpham+"&soluong="+newVal;
        $.ajax({
            url: '/giohang/update/',
            method: 'POST',
            data: data,
            error: function(error){
                console.log(error);
            }        
        });
    }
    e.preventDefault();
});
// remove item from cart
//------------------------------------------------------------------------------
$(".item-remove").on("click", function(e) {
    var $button = $(this);
    var $itembox = $button.parent().children().find('.item-box-total');
    var $item = $itembox.children().find('.item-giohang');
    var sanpham = $item.attr("data-sanpham");
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var data = "csrfmiddlewaretoken="+csrftoken+"&id_sanpham="+sanpham;
    $.ajax({
        url: '/giohang/update/',
        method: 'POST',
        data: data,
        success: function(data){            
            $button.parent().animate({
                opacity: 0,
                'margin-bottom':'-160px',
            }, 100, function() {                    
                $(this).remove();
                $('#amount').attr("data-tongcong",tinhTongTien(get_item()));
                $("#amount").text(formatMoney(parseInt($("#amount").attr("data-tongcong"))));    
            });
            if (!data.hethang) {
                $(".het-hang").remove();
            }
            if (data.giohangItemsCount>0){
                $(".had-item").text(data.giohangItemsCount);
                $(".navbar-giohang-count").text(data.giohangItemsCount);
                $(".navbar-giohang-count").addClass("count");                
            } else {                        
                $(".had-cart").remove();
                $(".cart-empty").text("RỖNG");                
                $(".navbar-giohang-count").text("");
                $(".navbar-giohang-count").removeClass("count");
                positionFooter();
            }            
            $('#amount').text(formatMoney(tinhTongTien(get_item())));
            $('#amount').attr("data-tongcong",tinhTongTien(get_item()));
            
        }
    });		
});
// update subtotal
//----------------------------------------------------------------------------

function giohangJSON(id_sanpham, id_giohang, dongia ,soluong, thanhtien) {
    var itemGioHang = {
        "id_sanpham"	: id_giohang,
        "id_giohang"	: id_giohang,
        "dongia"		: dongia, 
        "soluong"		: soluong,
        "thanhtien"		: thanhtien,
    };
    return itemGioHang;
}
get_item();
function get_item(){
    var $item = $(".item-true");
    var objectGioHang = JSON.parse('{"ghsp":[]}');
    objectGioHang.ghsp = [];
    $item.each(function(i){
        if($item.lenght==0)
            return;
        var $itembox 	= $(this).children().find(".item-box-total");
        var giohang 	= parseInt($itembox.children().find(".item-giohang").attr("data-giohang"));
        var sanpham 	= parseInt($itembox.children().find(".item-giohang").attr("data-sanpham"));
        var dongia 		= parseInt($itembox.children().find(".item-giohang").attr("data-dongia"));
        var soluong 	= parseInt($itembox.children().find(".quantity").val());
        var thanhtien 	= parseInt($itembox.find(".item-total").attr("data-thanhtien"));
        $itembox.find(".item-price").text(formatMoney(dongia));
        $itembox.find(".item-total").text(formatMoney(thanhtien));

        objectGioHang["ghsp"].push(giohangJSON(giohang, sanpham, dongia ,soluong, thanhtien));
    });
    return objectGioHang;
}

function tinhTongTien(arrJSON){
    var sum = 0;
    Object.keys(arrJSON.ghsp).forEach(function(index) {
        sum += parseInt(arrJSON.ghsp[index].thanhtien);
    });
    return sum;
}
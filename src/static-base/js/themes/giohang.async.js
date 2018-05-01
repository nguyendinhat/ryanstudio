$("#tamtinh").text(formatMoney(parseInt($("#tamtinh").attr("data-tamtinh"))));
$("#shipping-fee").text(formatMoney(parseInt($("#shipping-fee").attr("data-phigiaohang"))));
$("#giamgia").text(formatMoney(parseInt($("#giamgia").attr("data-giamgia"))));
$("#tongcong").text(formatMoney(parseInt($("#tamtinh").attr("data-tamtinh")) + parseInt($("#shipping-fee").attr("data-phigiaohang")) - parseInt($("#giamgia").attr("data-giamgia"))));
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
    $('#tamtinh').attr("data-tamtinh",tinhTongTien(get_item()));
    $("#tamtinh").text(formatMoney(parseInt($("#tamtinh").attr("data-tamtinh"))));
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
                $('#tamtinh').attr("data-tamtinh",tinhTongTien(get_item()));
                $("#tamtinh").text(formatMoney(parseInt($("#tamtinh").attr("data-tamtinh"))));    
            });
            if (!data.hethang) {
                $(".het-hang").remove();
                $("#btn-thanhtoan").addClass("btn-primary");
                $("#btn-thanhtoan").removeClass("btn-danger");
                $("#btn-thanhtoan").removeClass("disabled");
                $("#btn-thanhtoan").attr("aria-disabled","false");                
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
            $('#tamtinh').text(formatMoney(tinhTongTien(get_item())));
            $('#tamtinh').attr("data-tamtinh",tinhTongTien(get_item()));
            
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
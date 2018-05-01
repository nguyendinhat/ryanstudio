// them gio hang
$(document).ready(function(){
	var navbarCount = $(".navbar-giohang-count")
	var formSanPham = $(".form-sanpham-ajax")    
	formSanPham.submit(function(event){
		event.preventDefault();
		var thisForm = $(this);
		var actionEndpoint = thisForm.attr("data-endpoint");
		var httpMethod = thisForm.attr("method");
		var formData = thisForm.serialize();
		$.ajax({
		url: actionEndpoint,
		method: httpMethod,
		data: formData,
		success: function(data){
			console.log(data)
			var submitBtn1 = thisForm.find(".shop-item-tools");
			var submitBtn2 = thisForm.find(".shop-product-tools");
			if (data.added){
				submitBtn1.html('<button type="submit" class="btn-simple add-to-cart"><i class="material-icons remove_circle_outline"></i></button>');
				submitBtn2.html('<button type="submit" class="btn btn-sm btn-warning btn-m-0 float-right waves-effect waves-light scale-up">Xóa khỏi giỏ hàng</button>');
			} else {
				submitBtn1.html('<button type="submit" class="btn-simple add-to-cart"><i class="material-icons add_circle_outline"></i></button>');
				submitBtn2.html('<button type="submit" class="btn btn-sm btn-primary btn-m-0 float-right waves-effect waves-light scale-up">Thêm vào giỏ hàng</button>');
			}                        
			if (data.giohangItemsCount>0){
                $(".navbar-giohang-count").text(data.giohangItemsCount);
                $(".navbar-giohang-count").addClass("count");
            } else {
                $(".navbar-giohang-count").text("");
                $(".navbar-giohang-count").removeClass("count");
            }
		},
		error: function(errorData){
			console.log("error");
			console.log(errorData);
		}
		});
	});
});
$(".dob").keypress(function (event) {
	if (event.charCode >= 48 && event.charCode <= 57) {
		if ($(this).val().length === 4) {
			$(this).val($(this).val() + event.key + "/");
		} else if ($(this).val().length === 3) {
			if (event.key == 1 || event.key == 0) {
				day = event.key;
				return event.charCode;
			} else {
				$(this).val($(this).val() + 0 + event.key + "/");
			}
		} else if ($(this).val().length === 1) {
			$(this).val($(this).val() + event.key + "/");
		} else if ($(this).val().length === 0) {
			if (event.key == 3 || event.key == 2 || event.key == 1 || event.key == 0) {
				day = event.key;
				return event.charCode;
			} else {
				$(this).val(0 + event.key + "/");
			}
		} else if ($(this).val().length > 2 && $(this).val().length < 10) {
			return event.charCode;
		}
	}
	return false;
});
function isValidDate(s) {
	var bits = s.split('/');
	var d = new Date(bits[2], bits[1] - 1, bits[0]);
	return d && (d.getMonth() + 1) == bits[1];
}
function convertDate(s) {
	var bits = s.split('/');
	return bits[2]+"-"+bits[1]+"-"+bits[0];
}

(function ($) {
    var default_gt = $("#gioitinh").attr("data-gioitinh");
    $("input[name=gioitinh][value='"+default_gt+"']").prop("checked",true);
    $("#btn-account").click(function(e) {   
        var hoten = $("#hoten");
        var sdt = $("#sdt");
        var sdt_reg = new RegExp('^(01[2689]|0[89])[0-9]{8}$');
        var ngaysinh  = $("#ngaysinh");
        var check = true;
        

        if (hoten.val().length < 5) {
            showValidate(hoten);
            check=false;
        }
        if (!sdt_reg.test(sdt.val())) {
            showValidate(sdt);
            check=false;
        }
        if (!isValidDate(ngaysinh.val())){
            showValidate(ngaysinh);
            check = false;
        } 
        if(check) {
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            var data;
            data = "csrfmiddlewaretoken="+csrftoken+"&hoten="+$("#hoten").val()+"&sdt="+$("#sdt").val()+"&ngaysinh="+convertDate($("#ngaysinh").val())+"&gioitinh="+$('input[name=gioitinh]:radio:checked').val();
            $.ajax({
                type: "POST",
                url: '/taikhoan/',
                data: data,
                success: function(data){
                    toastr.success('Thông tin cá nhân của bạn đa được lưu', 'Đã lưu!');
                },                    
                error : function(){
                    toastr.error('Kiểm tra mọi thứ một lần nữa trước khi lưu','Có gì đó sai sai!');
                }
            });            
        }
        e.preventDefault();
    });
    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }
    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }
})(jQuery);
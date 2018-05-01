$(".selection-2").select2({
    minimumResultsForSearch: 20,
    dropdownParent: $('#dropDownSelect1')
});
$(document).ready(function(){
    $.get('http://ryanstudio.com:8000/static/json/phan_cap_hanh_chinh_vietnam.json',function(data){
        var ma_tinhthanh;
        var ma_quanhuyen;
        var ma_xaphuong;        
        $.each(data, function (index, value) {
            $("#tinhthanh").append('<option rel="' + index + '" value="'+value.code+'">'+value.name_with_type+'</option>');
        });
        $("#tinhthanh").change(function () {
            ma_tinhthanh = $(this).find('option:selected').attr('rel');
            $("#quanhuyen, #xaphuong").find("option:gt(0)").remove();
            $("#quanhuyen").find("option:first").text("Loading...");
            $.each(data, function (index, value) {
                if (index==ma_tinhthanh){
                    var data_child = this;
                    $.each(data_child['quan-huyen'], function (index, value) {
                        $("#quanhuyen").find("option:first").text("Chọn Quận/Huyện");
                        $("#quanhuyen").find("option:first").attr("rel", "-1");
                        $("#quanhuyen").append('<option rel="' + index + '" value="'+value.code+'">'+value.name_with_type+'</option>');
                    });
                }
                
            });
            
        });
        $("#quanhuyen").change(function () {
            ma_quanhuyen = $(this).find('option:selected').attr('rel'); 
            $("#xaphuong").find("option:gt(0)").remove();
            $("#xaphuong").find("option:first").text("Loading...");
            $.each(data, function (index, value) {
                if (index==ma_tinhthanh){
                    var data_child = this;
                    $.each(data_child['quan-huyen'], function (index, value) {
                        if (index==ma_quanhuyen){
                            var data_child = this;
                            $.each(data_child['xa-phuong'], function (index, value) {
                                $("#xaphuong").find("option:first").text("Chọn Xã/Phường");
                                $("#xaphuong").find("option:first").attr("rel", "-1");
                                $("#xaphuong").append('<option rel="' + index + '" value="'+value.code+'" path="'+value.path_with_type+'">'+value.name_with_type+'</option>');
                            });
                        }
                    });
                }
                
            });
            
        });        
    });
});
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
            $("#tinhthanh").append('<option rel="' + index + '" value="'+value.name_with_type+'">'+value.name_with_type+'</option>');
        });
        $("#tinhthanh").change(function () {
            ma_tinhthanh = $(this).find('option:selected').attr('rel');
            $("#quanhuyen, #xaphuong").find("option:gt(0)").remove();
            $.each(data, function (index, value) {
                if (index==ma_tinhthanh){
                    var data_child = this;
                    $.each(data_child['quan-huyen'], function (index, value) {
                        $("#quanhuyen").append('<option rel="' + index + '" value="'+value.name_with_type+'">'+value.name_with_type+'</option>');
                    });
                }                
            });            
        });
        $("#quanhuyen").change(function () {
            ma_quanhuyen = $(this).find('option:selected').attr('rel'); 
            $("#xaphuong").find("option:gt(0)").remove();
            $.each(data, function (index, value) {
                if (index==ma_tinhthanh){
                    var data_child = this;
                    $.each(data_child['quan-huyen'], function (index, value) {
                        if (index==ma_quanhuyen){
                            var data_child = this;
                            $.each(data_child['xa-phuong'], function (index, value) {
 
                                $("#xaphuong").append('<option rel="' + index + '" value="'+value.name_with_type+'" path="'+value.path_with_type+'">'+value.name_with_type+'</option>');
                            });
                        }
                    });
                }
                
            });
            
        });        
    });
});
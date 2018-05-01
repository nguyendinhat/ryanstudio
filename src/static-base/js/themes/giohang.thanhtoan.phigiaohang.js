function get_shipping_fee_kerry1(ma_tinhthanh, kg) {
    var result = 0;
    $.get('http://ryanstudio.com:8000/static/json/KerryExpress_van_chuyen_duong_bo.json',function(data){        
        $.each(data, function (index, value) {
            var data_child = this;
            $.each(data_child.city, function (index1, value1) {           
                if (ma_tinhthanh==index1) {
                    x = parseInt(index);
                    var base = 0;
                    var upper = kg-20;
                    var upper_fee = 0;
                    var upper_sum = 0;
                    if (kg<=20) {
                        if (kg<=5) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="<5") {
                                    result = parseInt(value2);
                                }
                            });                            
                        } else {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    result = parseInt(value2);
                                }
                            });
                        }
                    } else {
                        if (kg<=50) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="20-50") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (var i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;

                        } else if (kg<=200) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="50-200") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg<=500) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="200-500") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg<=1000) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="500-1000") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg<=3000) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="1000-3000") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg<=5000) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="3000-5000") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg<=10000) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2=="5000-10000") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        } else if (kg>10000) {
                            $.each(data_child['fee<20'], function (index2, value2) {
                                if (index2=="5-20") {
                                    base = parseInt(value2);
                                }
                            });
                            $.each(data_child['fee>20'], function (index2, value2) {
                                if (index2==">10000") {
                                    upper_fee = parseInt(value2);
                                }
                            });
                            for (i = 0; i < upper; i++) {
                                upper_sum += upper_fee;
                                
                            }
                            result = upper_sum + base;
                        }
                    }  
                    $("#shipping-fee").attr("data-phigiaohang",result);
                    $("#shipping-fee").text(formatMoney(parseInt($("#shipping-fee").attr("data-phigiaohang"))));
                    $("#tongcong").text(formatMoney(parseInt($("#tamtinh").attr("data-tamtinh")) + parseInt($("#shipping-fee").attr("data-phigiaohang")) - parseInt($("#giamgia").attr("data-giamgia"))));
                }
            });
        });
    });
}
var tinhthanh;
var trongluong = parseFloat($("#tongtrongluong").val());
$('#tinhthanh').change(function(){
    $("#shipping-fee").attr("data-phigiaohang","0");
    $("#shipping-fee").text(formatMoney(parseInt($("#shipping-fee").attr("data-phigiaohang"))));
});
$('#xaphuong').change(function(){
    if ($('#tinhthanh').find(':selected').attr("rel")=="-1"){
        tinhthanh = null;
    } else {                
        tinhthanh = $('#tinhthanh').find(':selected').attr("rel");
        get_shipping_fee_kerry1(tinhthanh, trongluong);
    }
});
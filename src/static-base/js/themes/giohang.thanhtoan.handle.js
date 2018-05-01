function previewPayment() {
    $(".pre-hoten").html($("input[name=hoten]").val());
    $(".pre-sdt").html($("input[name=sdt]").val());
    $(".pre-diachi").html($("input[name=ten]").val());
    $(".pre-pttt").html($("input[name=pttt]").val());
    $(".pre-pre-pttt-chitiet").html($("#datetimepicker1").find("input").val());
}

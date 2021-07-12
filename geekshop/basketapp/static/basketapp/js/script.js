window.onload = function () {
    $('.basket-items').on('click', 'input[type="number"]', function(){
        var t_href = event.target;
        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: function(data) {
                $('.basket-items').html(data.result);
                $('.basket-summary').html(data.result2);
            },
        });
        event.preventDefault();
    });
}
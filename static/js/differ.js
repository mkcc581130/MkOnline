$(function() {
    $('img').each(function () {
	    var $_t = $(this);
        var image = new Image();
        var src = $_t.data('src');
        image.src = src;
        image.onload = function () {
            $_t.attr('src',src).css('opacity','100');
        }
    });
    var mySwiper2 = new Swiper('.swiper-container2', {
        slidesPerView: 5.5,
        slidesPerColumn: 1,
        spaceBetween: 0
    });
    $('.swiper-container2').on('click','.swiper-slide',function () {
        var $_t = $(this);
        $_t.addClass('active').siblings().removeClass('active');
        var li = $('.contain-main').eq($_t.index());
        if (!li.html()) {
            $.get('',
                {
                    cid: $_t.data('id')
                },
                function (data) {
                    var html = '';
                    var goods = data.goods;
                    for (var i = 0; i < goods.length; i++) {
                        html += '<div class="contain-item"> \
                            <a href="'+'/detail/'+goods[i].id+'"><img src="'+goods[i].img+'" width="100%" /> \
                            <p class="goods-title"><span class="brand">慧绣</span> '+goods[i].name+'</p></a> \
                            <p class="goods-prices">￥<span class="lfont">'+goods[i].price.slice(0,goods[i].price.indexOf('.'))+'</span>'+goods[i].price.slice(goods[i].price.indexOf('.'))+'</p> \
                        </div>';
                    }
                    li.append(html);
                    $('.contain-item').each(function(){
                        if($(this).index()%2 == 0){
                            if(!$(this).hasClass('contain-item-left')) $(this).addClass('contain-item-left');
                        };
                    });
                    li.show().siblings().hide();
                }
            )
        } else {
            li.show().siblings().hide();
        }
    });
	$('.classify-one').on('click','a',function () {
		$('.classify-two').find('ul').eq($(this).index()).show().siblings('ul').hide();
	});
});
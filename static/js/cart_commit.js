setCookie("delivery_to",window.location.href);
$(function(){
	$('.nav-c').click(function(){
		$('.nav-dropdown').slideToggle();
	});
	var c = $('.item .cart-item');
	var h = c.length;
	if(h>3){
		$('.item').append($('<p class="remain"><span>还有'+(h-3)+'件</span> <i class="icon iconfont icon-jtbottom"></i></p>')).css('height','284px');
		$('.remain').click(function(){
			if($(this).hasClass('active')){
				var $_this = $(this);
				$('.item').css('height','284px');
					setTimeout(function(){
					$_this.removeClass('active').find('span').text('还有'+(h-3)+'件').next().removeClass('icon-jttop').addClass('icon-jtbottom');
				},500);
			}else{
				$(this).addClass('active').find('span').text('收起').next().removeClass('icon-jtbottom').addClass('icon-jttop');
				$('.item').css('height',86*h + 26 + 'px');
			}
		});
	}
	// var sum = 0.00;
	// c.each(function () {
	// 	var $_t = $(this);
	// 	var $_text = $_t.find('.cart-item-title span').text();
	// 	sum += parseInt($_text.slice($_text.indexOf('X')+1))*(parseFloat($_t.find('.cart-item-price').text().slice(1)));
    // });
	// $('section.price .goods-price').text('￥'+sum.toFixed(2));
	// var dis = $('.coupon .dis').text();
	// if(dis){
	// 	var ac = (sum - parseFloat(dis.slice(2))).toFixed(2)+'';
	// 	$('footer span').html('实付款：￥<span class="big">'+ac.slice(0,ac.indexOf('.'))+'</span>'+ac.slice(ac.indexOf('.')))
	// }else{
	// 	var ac = sum.toFixed(2)+'';
	// 	$('footer span').html('实付款：￥<span class="big">'+ac.slice(0,ac.indexOf('.'))+'</span>'+ac.slice(ac.indexOf('.')))
	// }
});
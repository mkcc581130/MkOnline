
$(function() {
	(function(){
		window.setTimeout(
			function(){
				if($(window).scrollTop()>=($(window).height()/2)){
					$('#mainHeader').css('background-color','rgba(58,58,58,'+$(window).height()/600+')');
				}else{
					$('#mainHeader').css('background-color','rgba(58,58,58,'+$(window).scrollTop()/350+')');
				};
			},100
		)
		var image = new Image();
		var img = $('.show-coupon img');
		var src = img.data('src');
		image.src = src;
		image.onload = function () {
			img.attr('src',src);
			$('.show-coupon').fadeIn();
		}
	})();
	if($(window).width()> 640){
		$('#mainHeader').css('margin-left',(-$('#mainHeader').width()/2)+'px').css('left','50%');
	};
	$(window).scroll(function(){
		if($(window).scrollTop()>=($(window).height()/2)){
			$('.to-top').show();
		}else{
			$('#mainHeader').css('background-color','rgba(58,58,58,'+$(window).scrollTop()/350+')');
			$('.to-top').hide();
		};
	});
	var mySwiper1 = new Swiper('.swiper-container1', {
		pagination: '.swiper-pagination',
		paginationClickable: true,
		autoplay: 2500,
		loop: true,
		autoplayDisableOnInteraction: false,
	});
	var mySwiper2 = new Swiper('.swiper-container2', {
        slidesPerView: 3.5,
        slidesPerColumn: 1,
        spaceBetween: 30
	});
	$('.show-coupon').click(function () {
		var $_cart_modal = $('.cart-modal');
		$_cart_modal.find('p').text('恭喜您领取成功').end().fadeIn();
		window.setTimeout(function(){
			$_cart_modal.fadeOut();
			$('.show-coupon').fadeOut();
		},1000);
    });
	$('.show-coupon .close').click(function () {
		$('.show-coupon').fadeOut();
	});
});
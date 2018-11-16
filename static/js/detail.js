$(function(){
	var price=$('.inner-price span').text();
	(function(){
		$('.contain-item').each(function(){
			if($(this).index()%2 == 0){
				$(this).addClass('contain-item-left');
			}
		});
	})();

	$(window).resize(function(){
		$('.swiper-container .swiper-slide').css('width',$(window).width()+'px');
	})
	var mySwiper1 = new Swiper('.swiper-container1', {
		onInit: function(swiper){
	      //Swiper初始化后执行
	    	$('.now-swiper').text(swiper.activeIndex+1);
	    	$('.all-swiper').text('/'+swiper.slides.length);
	   },
		onSlideChangeEnd: function(swiper){
			$('.now-swiper').text(swiper.activeIndex+1);
		},
	});
	var mySwiper2 = new Swiper('.swiper-container2', {
        pagination: '.swiper-pagination',
		paginationClickable: true,
        slidesPerView: 2,
        slidesPerColumn: 3,
        spaceBetween: 30,
	});
	var mySwipers = new Swiper('.swiper-containers', {
		autoHeight: true,
		onSlideChangeEnd: function(swiper){
			$('.top-nav li a').removeClass('nav-active');
			$('.top-nav li').eq(swiper.activeIndex).find('a').addClass('nav-active');
		},
	});
	$('.more-info-nav').on('click','li',function(){
		$(this).addClass('more-info-nav-active').siblings().removeClass('more-info-nav-active');
		if($(this).index() == 0){
			$('.more-info-canshu').hide();
			$('.more-info-shouhou').hide();
			$('body').css('background-color','rgb(240,242,245)');
			$('.more-info-goods').show();
			mySwipers.update();
		}else if($(this).index() == 1){
			$('.more-info-goods').hide();
			$('.more-info-shouhou').hide();
			$('body').css('background-color','#fff');
			$('.more-info-canshu').show();
			mySwipers.update();
		}else{
			$('.more-info-goods').hide();
			$('.more-info-canshu').hide();
			$('body').css('background-color','#fff');
			$('.more-info-shouhou').show();
			mySwipers.update();
		};
	})
	$('.top-nav').on('click','li',function(){
		mySwipers.slideTo($(this).index());
		$(this).siblings().find('a').removeClass('nav-active');
		$(this).find('a').addClass('nav-active');
	});
	
	$('.icon-show').click(function(){
		if($(this).hasClass('icon-jtbottom')){
			$('.icon-jtbottom').hide();
			$('.icon-jttop').show();
			$('.main-gift-right dt').show();
			$('.gift-c').css('overflow','visible').css('word-break','inherit').css('white-space','inherit');
			$('.gift-c .icon-jtright').show();
		}else{
			$('.icon-jttop').hide();
			$('.icon-jtbottom').show();
			$('.main-gift-right dt').hide();
			$('.gift-c').css('overflow','hidden').css('word-break','keep-all').css('white-space','nowrap');
			$('.gift-c .icon-jtright').hide();
		};
	});
	$('.style').on('click','li',function(){
		if(!$(this).hasClass('active')){
			var txt = $(this).text();
			var img = $('.swiper-container1 img');
			var index = $(this).index();
			var img_index = img.eq(index);
			var stocks = 0;
			$.ajax({
				async: false,
				data:{img_id:img_index.data('id')},
				success:function (data) {
					stocks = data.stocks;
				},
				error:function (data) {
					zeroModal.alert({
						content: '服务器错误！',
						width:'80%',
						height:'260px'
					});
				}
			});
			$(this).addClass('active').siblings().removeClass('active');
			$('.goods-style').text(txt);
			$('.goods-img img').attr('src',img_index.attr('src'));
			$('.stocks').text('库存：'+stocks);
			$('#detailForm').find('input').eq(0).val(img_index.data('id'));
			$(".wan-spinner").WanSpinner({
                maxValue: stocks,
                minValue: 1,
                inputWidth: 34,
                valueChanged: function(element, val) {
                    $('.goods-num').text(val+'件');
                    $('.inner-price span').text((parseFloat(price)*val).toFixed(2));
                    $('#detailForm').find('input').eq(1).val(val);
                }
            });
		};
	});
	$('.main-choice .icon-three').click(function(){
		$('.style-modal').show();
		$('.shadow').show();
		$('.footer-right').css('width','100%');
		$('.footer-left').css('display','none');
	});
	$('.shadow,.close').click(function(){
		$('.style-modal').hide();
		$('.shadow').hide();
		$('.footer-left').css('display','block');
		$('.footer-right').css('width','50%');
		var nowprice=$('.inner-price span').text();
		$('.big-price').text(nowprice.slice(0,nowprice.indexOf('.')));
		$('.small-price').text(nowprice.slice(nowprice.indexOf('.')));
	});
	$('.shadow1').click(function(){
		$('.local-modal').animate({marginRight:'-80%'},500);
		setTimeout(function(){
			$('.shadow1').hide();
		},490);
	});
	// $('.icon-dingwei').click(function(){
	// 	$('.local-modal').animate({marginRight:'0%'},500);
	// 	setTimeout(function(){
	// 		$('.shadow1').show();
	// 	},490);
	// });
	$('.local-modal-first').on('click','.modal-item',function(){
		if(!$(this).hasClass('active')){
			$(this).append($('.local-modal-first .active').find('i')).addClass('active').siblings().removeClass('active');
		} 
		$('.local-modal-first').hide();
		$('.local-modal-second').show();
	});
	$('.local-modal-second').on('click','.modal-item',function(){
		if(!$(this).hasClass('active')){
			$(this).append($('.local-modal-second .active').find('i')).addClass('active').siblings().removeClass('active');
		} 
		$('.local-modal-second').hide();
		$('.local-modal-third').show();
	});
	$('.local-modal-third').on('click','.modal-item',function(){
		if(!$(this).hasClass('active')){
			$(this).append($('.local-modal-third .active').find('i')).addClass('active').siblings().removeClass('active');
		} 
		$('.locate-sheng').text($('.local-modal-first .modal-item.active').text());
		$('.locate-shi').text($('.local-modal-second .modal-item.active').text());
		$('.locate-qu').text($(this).text());
		$('.local-modal').animate({marginRight:'-80%'},500);
		setTimeout(function(){
			$('.shadow1').hide();
		},490);
		$('.local-modal-third').hide();
		$('.local-modal-first').show();
		
	});
	$('.local-modal .title i').click(function(){
		if($('.local-modal-first').css('display')=='block'){
			$('.local-modal').animate({marginRight:'-80%'},500);
			setTimeout(function(){
				$('.shadow1').hide();
			},490);
		}else if($('.local-modal-second').css('display')=='block'){
			$('.local-modal-second').hide();
			$('.local-modal-first').show();
		}else{
			$('.local-modal-third').hide();
			$('.local-modal-second').show();
		}
	});
	$('.add-to-cart').click(function(){
		var $_i =$('#detailForm input');
		var stock = $('.stocks span').text();
		if(stock == '0'){
			zeroModal.alert({
				content: '无库存，无法加入购物车！',
				width:'80%',
				height:'260px'
			});
		}else{
			$.ajax({
				url:'',
				type:'post',
				data:{
					'method':'add',
					'img_id':$_i.eq(0).val(),
					'number':$_i.eq(1).val(),
					'csrfmiddlewaretoken': $_i.eq(2).val()
				},
				success:function (data) {
					$('.bedage').text(data.len);
					var $_cart_modal = $('.cart-modal');
					$_cart_modal.find('p').text('加入购物车成功').end().fadeIn();
					window.setTimeout(function(){
						$_cart_modal.fadeOut();
					},1000);
				},
				error:function () {
					zeroModal.alert({
						content: '无库存，无法加入购物车！',
						width:'80%',
						height:'260px'
					});
				}
			});
		}
	});
	$('.buy-now').click(function () {
		var stock = $('.stocks span').text();
		if(stock == '0'){
			zeroModal.alert({
				content: '无库存，无法购买！',
				width:'80%',
				height:'260px'
			});
		}else{
			$('#detailForm').submit();
        }
    });
	$('.share').click(function () {
		$(this).hide();
		$('.shadow2').show();
		$('.popup').css('bottom', "0");
    });
	$('.share-modal').click(function () {
		$(this).hide();
		$('.share').show();
    });
	$('.erwei-model .close').click(function () {
		$('.erwei-model').hide();
		$('.share').show();
    });
});
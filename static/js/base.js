$('.contain-item').each(function(){
	var $_t = $(this),img=$_t.find('img');
	img.css('height',img.width+'px');
	if($_t.index()%2 == 0){
		if(!$_t.hasClass('contain-item-left')) $_t.addClass('contain-item-left');
	}
	var image = new Image();
	var src = img.data('src');
	image.src = src;
	image.onload = function () {
		img.attr('src',src).css('opacity','100');
    }
});
function setCookie(name,value){
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days*24*60*60*1000);
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString() + ";path=/";
}


function getCookie(name){
	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg)){
		return unescape(arr[2]);
	}else{
		return null;
	}
}
$(function(){
	$('.nav-c').click(function(){
		$('.nav-dropdown').slideToggle();
	});
	$('.goods-item .goods-content').width($(window).width()-134+'px');
	$(window).scroll(function(){
		if($(window).scrollTop()>=($(window).height()/2)){
			$('.to-top').show();
		}else{
			$('.to-top').hide();
		}
	});
	$('.to-top').click(function(){
		$(window).scrollTop(0);
	});
});

//返回到目录页
$(".return").bind("touchend", function() {
	$(".flipbook").turn('page','2'); //跳转页数
});
var count = [];
//判断手机类型
window.onload = function() {
	// alert($(window).height());
	var u = navigator.userAgent;
	if(u.indexOf('Android') > -1 || u.indexOf('Linux') > -1) { //安卓手机
	} else if(u.indexOf('iPhone') > -1 || u.indexOf('iPad') > -1) { //苹果手机
		//屏蔽ios下上下弹性
		$(window).on('scroll.elasticity', function(e) {
			e.preventDefault();
		}).on('touchmove.elasticity', function(e) {
			e.preventDefault();
		});
	} else if(u.indexOf('Windows Phone') > -1) { //winphone手机
	}
	//预加载
	
	loading();
}

//加载页面
function loading() {
	// var numbers=0;
	// var length;
	// var img;
	// $.ajax({
	// 	type:"get",
	// 	url:"getPros.php",
	// 	async:false,
	// 	typeData:'json',
	// 	success:function(data){
	// 		imgs = $.parseJSON(data);
	// 		length = imgs.length;
	// 	}
	// });
	// $(function progressbar() {
	// 	var tagHtml = "";
	// 	for(var i = 2; i < length; i++) {
	// 		if(i == length-1) {
	// 			tagHtml += ' <div id="end" style="background:url(img/products/' + imgs[i] + ') center top no-repeat;background-size:contain;"></div>';
	// 		} else {
	// 			tagHtml += ' <div style="background:url(img/products/' + imgs[i] + ') center top no-repeat;background-size:contain;"></div>';
	// 		}
	// 	}
	// 	$(".flipbook").append(tagHtml);
	// 	loadApp();
	// });
	// for(var i = 2; i < length; i++) {
	// 	var img = new Image();
	// 	img.src = "./img/products/"+imgs[i];
	// 	img.onerror = function(e){
	// 		console.info(e);
	// 	}
	// 	img.onload = function() {
	// 		numbers += (1 / (length-2)) * 100;
	// 		$('.number').html(parseInt(numbers) + "%");
	// 		if(Math.round(numbers) == 100) {
	// 			$('.shade').hide();
	// 			$(".flipbook-viewport").show();
	// 		};
	//
	// 	}
	// 	img = '';
	// }
	// for(var i = 2; i < length; i++){
	// 	if(imgs[i].slice(4,7) == '101'){
	// 		count.push(i+1);
	// 	}

	function loadApp() {
		$('.flipboox').width($(window).width()).height($(window).height());
		$(window).resize(function() {
			$('.flipboox').width($(window).width()).height($(window).height());
		});
		$('.flipbook').turn({
			width: $(window).width(),
			height: $(window).height(),
			display: 'single',
			gradients: true,
			autoCenter: true,
			when: {
				turning: function(e, page, view) {
					document.getElementById("audioPlay").play();
				},
				turned: function(e, page, view) {
					if(page == 1) {
						$(".return").css("display", "none");
					} else {
						$(".return").css("display", "block");
					}
					if(page == 2) {
						count = [3, 4, 109, 119, 134];
						$('.contents .main').find('p').each(function(){
							var $_t = $(this);
							$_t.on("touchend",function(){$(".flipbook").turn('page',count[$_t.index()]);});
						});
					}
				}
			}
		});
	}
	loadApp();
}
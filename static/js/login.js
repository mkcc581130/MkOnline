$(function(){
	var enable = true;
	function jump(){
		enable = false;
		$('.jump-modal').removeClass('none');
		setTimeout(function () {
			location.replace('http://'+location.hostname+':'+location.port);
		},1000);
	};
	$('input').on('input',function(){
		if($(this).val().length>0){
			$(this).nextAll('i').show();
		}else{
			$(this).nextAll('i').hide();
		}
	}).on('focus',function(){
		$('.error-info').addClass('none');
		if($(this).val().length>0){
			$(this).nextAll('i').show();
		}else{
			$(this).nextAll('i').hide();
		}
	}).on('blur',function(){
		var $_val = $(this).val(),$_i = $(this).nextAll('i');
		
		window.setTimeout(function(){
			if($_val.length>0){
				$_i.hide();
			}
		},10);
		
	});
	$('.login-tab').on('click','ul',function () {
		var $_t = $(this);
		if(!$_t.hasClass('login-selected')){
			$_t.addClass('login-selected').siblings().removeClass('login-selected');
			$('form').eq($_t.index()).show().siblings().hide()
		}
    });
	$('.icon-cha').click(function(){
		$(this).prevAll('input').val('');
	});
	$('.form-group-tel .icon-cha').click(function(){
		$(this).prevAll('input').val('');
		$(this).prev().removeClass('active');
	});
	$('.form-group-tel button').click(function(){
		var $_t = $(this);
		if($_t.hasClass('active')){
			var sec1 = 120;
			$.get("",{tel:$_t.prev().val()},function (data){
				if(data.msg == 'success'){
					var inter1 = window.setInterval(function(){
						if(sec1>0){
							$_t.text('重新发送'+sec1 + '(s)').removeClass('active');
							sec1 -= 1;

						}else{
							window.clearInterval(inter1);
							$_t.text('重新发送').addClass('active');
						}
					},1000);
				}else{
					$('.error-info').removeClass('none').find('span').text(data.msg);
				}
            });
		}
	});
	$('.form-group-tel').on('input','input',function(){
		if($(this).val().length>0){
			$(this).nextAll('i').show();
		}else{
			$(this).nextAll('i').hide();
		}
		if(/^1[345789]\d{9}$/.test($(this).val())){
			$(this).next().addClass('active');
		}else{
			$(this).next().removeClass('active');
		}
	});
	$('#regSub').click(function () {
		if(!(/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/.test($('#regPassword').val()))){
			$('.error-info').removeClass('none').find('span').text('密码必须6位以上，包含数字与字母！');
		}else if($('#regPassword').val()!=$('#regPassword2').val()){
			$('.error-info').removeClass('none').find('span').text('两次密码不相同，请重新输入');
		}else{
			enable = false;
			$.post("",$('#regForm').serialize(),function (data) {
				if(data.msg == 'success'){
					jump();
				}else{
					$('.error-info').removeClass('none').find('span').text(data.msg);
					enable = true;
				}
            });
		}
    });
	$('#telSub').click(function () {
		if(!(/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/.test($('#telPassword').val()))){
			$('.error-info').removeClass('none').find('span').text('密码必须6位以上，包含数字与字母！');
		}else if($('#telPassword').val()!=$('#telPassword2').val()){
			$('.error-info').removeClass('none').find('span').text('两次密码不相同，请重新输入');
		}else{
			enable = false;
			$.post("",$('#telForm').serialize(),function (data) {
				if(data.msg == 'success'){
					jump();
				}else{
					$('.error-info').removeClass('none').find('span').text(data.msg);
					enable = true;
				}
            });
		}
    });
	$('#loginSub').click(function () {
		var visitable_form = $('form:visible'),had_val = false;
		visitable_form.find('input').each(function () {
			had_val = !!($(this).val());
        });
		if(had_val){
			enable = false;
			$.post("",visitable_form.serialize(),function (data) {
				if(data.msg == 'success'){
					jump();
				}else{
					$('.error-info').removeClass('none').find('span').text(data.msg);
					enable = true;
				}
			});
		}else{
			$('.error-info').removeClass('none').find('span').text('输入框不能为空！');
		}

    });

	$('#findSecondSub').click(function () {
		var p1 = $('#findPassword').val();
		if(!(/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,10}$/.test(p1))){
			$('.error-info').removeClass('none').find('span').text('密码必须6位以上，包含数字与字母！');
		}else if(p1!=$('#findPassword2').val()){
			$('.error-info').removeClass('none').find('span').text('两次密码不相同，请重新输入');
		}else{
			enable = false;
			$.post("",$('#findPwd2Form').serialize(),function (data) {
				if(data.msg == 'success'){
					jump();
				}else{
					$('.error-info').removeClass('none').find('span').text(data.msg);
					enable = true;
				}
			});
		}

    });
	$(".captcha").click(function () {
		var $_t = $(this);
		enable = false;
		$.get("/captcha/refresh/?"+Math.random(), function(result){
			$_t.attr("src",result.image_url).next().attr("value",result.key);
			enable = true;
		});
    });
});
$(function(){
	$('.shadow').click(function(){
		$('.local-modal').animate({marginRight:'-80%'},500);
		setTimeout(function(){
			$('.shadow').hide();
		},490);
	});
	$('.form-group-locate').click(function(){
		$('.local-modal').animate({marginRight:'0%'},500);
		setTimeout(function(){
			$('.shadow').show();
		},490);
		
	});
	$('.local-modal-first').on('click','.modal-item',function(){
		var $_t = $(this);
		var $_s = $('.local-modal-second');
		$.get('',{p:$_t.data('id')},function (data) {
        	if(!$_t.hasClass('active')){
				$_t.append($('.local-modal-first .active').find('i')).addClass('active').siblings().removeClass('active');
			}
			c = JSON.parse(data.cities);
        	$_s.empty();
        	for(var i = 0;i<c.length;i++){
        		$_s.append('<div class="modal-item" data-id="'+c[i].pk+'">'+c[i].fields.name+'</div>');
			}
			$('.local-modal-first').hide();
			$_s.show();
		});
	});
	$('.local-modal-second').on('click','.modal-item',function(){
		var $_t = $(this);
		var $_th = $('.local-modal-third');
		$.get('',{c:$_t.data('id')},function (data) {
        	if(!$_t.hasClass('active')){
				$_t.append($('.local-modal-second .active').find('i')).addClass('active').siblings().removeClass('active');
			}
			a = JSON.parse(data.areas);
        	$_th.empty();
			for(var i = 0;i<a.length;i++){
        		$_th.append('<div class="modal-item" data-id="'+a[i].pk+'">'+a[i].fields.name+'</div>');
			}
			$('.local-modal-second').hide();
			$_th.show();
		});
	});
	$('.local-modal-third').on('click','.modal-item',function(){
		if(!$(this).hasClass('active')){
			$(this).append($('.local-modal-third .active').find('i')).addClass('active').siblings().removeClass('active');
		}
		$('.form-group-locate').find('span').each(function(){
			if($(this).index()==3){
				$(this).text($('.local-modal-first .modal-item.active').text());
			}else if($(this).index()==4){
				$(this).text($('.local-modal-second .modal-item.active').text());
			}else{
				$(this).text($('.local-modal-third .modal-item.active').text());
			}
		}).end().find('input').each(function () {
			if($(this).index()==0){
				$(this).val($('.local-modal-first .modal-item.active').data('id'));
			}else if($(this).index()==1){
				$(this).val($('.local-modal-second .modal-item.active').data('id'));
			}else{
				$(this).val($('.local-modal-third .modal-item.active').data('id'));
			}
        });
		$('.local-modal').animate({marginRight:'-80%'},500);
		setTimeout(function(){
			$('.shadow').hide();
		},490);
		$('.local-modal-third').hide();
		$('.local-modal-first').show();
		
	});
	$('.local-modal .title i').click(function(){
		if($('.local-modal-first').css('display')=='block'){
			$('.local-modal').animate({marginRight:'-80%'},500);
			setTimeout(function(){
				$('.shadow').hide();
			},490);
		}else if($('.local-modal-second').css('display')=='block'){
			$('.local-modal-second').hide();
			$('.local-modal-first').show();
		}else{
			$('.local-modal-third').hide();
			$('.local-modal-second').show();
		}
	});
	$('.nav-delete').click(function () {
		zeroModal.confirm({
			content:'您确定要删除该收货地址吗？',
			width:'80%',
			height:'260px',
			okFn:function(){
				$.get('',{delete:true},function (data) {
					if(data.msg=='success'){
						$('.jump-modal').removeClass('none');
						setTimeout(function () {
							location.replace('http://'+location.hostname+':'+location.port+'/delivery/');
						},1000);
					}else{
						zeroModal.alert({
							content:'收货地址删除失败!',
							width:'80%',
							height:'260px'
						});
					}
				});
			}
		});
    });
});
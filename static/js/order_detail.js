$(function(){

	var h = $('.item .order-item').length;
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
	$('.delete').click(function () {
		var $_t = $(this);
		zeroModal.confirm({
			content:'您确定要删除该订单吗？',
			width:'80%',
			height:'260px',
			okFn:function(){
				$.ajax({
					url:'',
					type:'GET',
					data:{delete_id:$_t.data('id')},
					success:function(data) {
						if(data.msg == 'success'){
							$('.jump-modal').removeClass('none');
							setTimeout(function () {
								location.replace('http://'+location.hostname+':'+location.port+'/order/0');
							},1000);
						}else{
							zeroModal.alert({
								content:'删除失败,请重试！',
								width:'80%',
								height:'260px'
							});
						}
					},error:function () {
						zeroModal.alert({
							content:'服务器错误,删除失败！',
							width:'80%',
							height:'260px'
						});
					}
				});
			}
		});
    });
	$('.cancel').click(function () {
		var $_t = $(this);
		zeroModal.confirm({
			content:'您确定要取消该订单吗？',
			width:'80%',
			height:'260px',
			okFn:function(){
				$.ajax({
					url:'',
					type:'GET',
					data:{cancel_id:$_t.data('id')},
					success:function(data) {
						if(data.msg == 'success'){
							$('.jump-modal').removeClass('none');
							setTimeout(function () {
								location.replace('http://'+location.hostname+':'+location.port+'/order/0');
							},1000);
						}else{
							zeroModal.alert({
								content:'删除失败,请重试！',
								width:'80%',
								height:'260px'
							});
						}
					},error:function () {
						zeroModal.alert({
							content:'服务器错误,删除失败！',
							width:'80%',
							height:'260px'
						});
					}
				});
			}
		});
    });
	$('.remind-delivery').click(function () {
		var $_t = $(this);
		$.get('',{'remind_id':$_t.data('id')},function (data) {
			if(data.msg == 'success'){
				zeroModal.success({
					content:'提醒发货成功!',
					width:'80%',
					height:'230px'
				});
			}
		});
	});
	$('.confirm-delivery').click(function () {
		var $_t = $(this);
		zeroModal.confirm({
			content:'您确定要确认收货吗？',
			width:'80%',
			height:'260px',
			okFn:function(){
				$.get('/order_detail/',{'confirm_id':$_t.data('id')},function (data) {
					if(data.msg == 'success'){
						zeroModal.success({
							content:'确认收货成功!',
							width:'80%',
							height:'230px',
							okFn:function () {
								location.replace('http://'+location.hostname+'/order/0');
							}
						});
					}
				});
			}
		});
	});
});

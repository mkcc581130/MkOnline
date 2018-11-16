$(function(){
	var $_click,cart_id='';
	(function(){
		var all= 0;
		var icon_active = $('.icon-outer.active');
		$('.cart-content').width($(window).width()<=640 ? $(window).width()-166 +'px':'474px');
		icon_active.nextAll('.cart-content').each(function(){
			var $_t =$(this);
			cart_id += $_t.data('id') +',';
			all += parseFloat($_t.find('.price').text().slice(1,-1))*parseInt($_t.find('.wan-spinner input').val());
		});
		$('.count-price span').text(all.toFixed(2));
		$('.contain-item').each(function(){
			if($(this).index()%2 == 0){
				$(this).addClass('contain-item-left');
			}
		});
		$('.pay span').text('('+ icon_active.length +')');
		$('.pay input').eq(1).val(cart_id.slice(0,-1));
	})()
	$(".wan-spinner").WanSpinner({
		maxValue: 999,
		minValue: 1,
		inputWidth: 24,
		valueChanged: function(element, val) {

			$.ajax({
				url:'',
				type:'GET',
				data:{id:$(element).data('id'),number:val},
				success:function () {
					var all= 0;
					if($(element).parents('.cart-content').prevAll('.icon-outer').hasClass('active')){
						$('.icon-outer.active').nextAll('.cart-content').each(function(){
							var $_t =$(this);
							all += parseFloat($_t.find('.price').text().slice(1,-1))*parseInt($_t.find('.wan-spinner input').val());
						});
						$('.count-price span').text(all.toFixed(2));
					}
                },error:function () {
					zeroModal.alert({
                        content:'服务器错误！',
                        width:'80%',
                        height:'260px'
                    });
                }
			});
	    }
	});
	$('.edit').click(function(){
		$(this).hide().next().show().parent().prevAll('.cart-content').find('.edit-style').show().prev('a').find('.title').hide().next().hide();
	});
	$('.complete').click(function(){
		$(this).parent().hide().prev().show().parents('.cart-bottom').prevAll('.cart-content').find('.edit-style').hide().prev('a').find('.title').show().next().show();
	});
	$('.delete').click(function(){
		var $_t = $(this);
		zeroModal.confirm({
			content:'您确定要删除该商品吗？',
			width:'80%',
			height:'260px',
			okFn:function(){
				$.ajax({
					url:'',
					type:'GET',
					data:{id:$_t.data('id'),del:true},
					success:function () {
						var $_i =$_t.parents('.cart-bottom').prevAll('.icon-outer');
						if($_i.hasClass('active')) $_i.click();
						$_t.parents('.cart-item').remove();
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
	$('.icon-outer').click(function(){
		var all= 0,cart_id ='';
		if(!$(this).hasClass('active')){
			$(this).addClass('active');
			if($('.icon-outer').length == $('.icon-outer.active').length) $('.icon-outer-all').addClass('active');
			$('.icon-outer.active').nextAll('.cart-content').each(function(){
				var $_t =$(this);
				all += parseFloat($_t.find('.price').text().slice(1,-1))*parseInt($_t.find('.wan-spinner input').val());
			});
			$('.count-price span').text(all.toFixed(2));
			
			$('.pay span').text('('+ $('.icon-outer.active').length +')');
		}else{
			$(this).removeClass('active');
			if($('.icon-outer-all').hasClass('active')) $('.icon-outer-all').removeClass('active');
			$('.icon-outer.active').nextAll('.cart-content').each(function(){
				var $_t =$(this);
				all += parseFloat($_t.find('.price').text().slice(1,-1))*parseInt($_t.find('.wan-spinner input').val());
			});
			if(all != 0){
				$('.count-price span').text(all.toFixed(2));
			}else{
				$('.count-price span').text('0.00');
			}
			
			$('.pay span').text('('+ $('.icon-outer.active').length +')');
		}
		$('.icon-outer.active').each(function () {
			cart_id += $(this).data('id') +',';
        });
		$('.pay input').eq(1).val(cart_id.slice(0,-1));
	});
	$('.icon-outer-all').click(function(){
		if(!$(this).hasClass('active')){
			var all= 0,cart_id = '';
			$(this).addClass('active');
			$('.icon-outer').each(function(){
				if(!$(this).hasClass('active')) $(this).addClass('active');
				cart_id += $(this).data('id') +',';
			});
			$('.pay input').eq(1).val(cart_id.slice(0,-1));
			$('.icon-outer').nextAll('.cart-content').each(function(){
				var $_t =$(this);
				all += parseFloat($_t.find('.price').text().slice(1,-1))*parseInt($_t.find('.wan-spinner input').val());
			});
			$('.count-price span').text(all.toFixed(2));
			$('.pay span').text('('+ $('.icon-outer.active').length +')');
		}else{
			$(this).removeClass('active');
			$('.pay input').eq(1).val('');
			$('.icon-outer').each(function(){
				if($(this).hasClass('active')) $(this).removeClass('active');
			});
			$('.count-all span').eq(0).text('0.00');
			$('.count-price span').text('0.00');
			$('.pay span').text('(0)');
		}
	});
	$('.edit-style').click(function(){
		var $_t = $(this),prop='',ogid=$_t.data('id'),formInput=$('#changeStyleForm input');
		$_t.find('span').each(function(){
			prop +=$(this).text()+'/';
		});
		var st = prop.slice(0,-1);
		$('.choice span').text(st);
		formInput.eq(0).val(ogid);
		$.ajax({
			url:'',
			type:'GET',
			data:{id:ogid,prop:true},
			success:function (data) {
				var $_s = $('.style-modal'),html = '';
				for(var i =0;i<data.props.length;i++){
					var pi = data.props[i];
					for(var j =0;j<pi.images.length;j++){
						html+='<img class="none" src="/media/'+pi.images[j].src+'" data-id="'+pi.images[j].id+'" width="100%" />';
                    }
                    $_s.find('.goods-img').empty().append(html);
					html = '';
                    for(var k =0;k<pi.detail_props.length;k++){
						var pik = pi.detail_props[k];
						if(pik == st){
							html+='<li class="active">'+pik+'</li>';
							var show_img = $_s.find('.goods-img img').eq(k);
							show_img.show();
							formInput.eq(1).val(show_img.data('id'));
						}else{
							html+='<li>'+pik+'</li>'
						}
                    }
                    $_s.find('.modal-contain>ul').empty().append('<li class="style"><div class="modal-title">'+pi.prop+'</div><div class="modal-right"><ul>'+html+'</ul></div><div class="clearfix"></div></li>');
					$('.style').on('click','li',function(){
						var $_t = $(this);
						if(!$_t.hasClass('active')){
							$_t.addClass('active').siblings().removeClass('active');
							var txt = '';
							$('.style .active').each(function(){
								txt+=($(this).text()+'/');
							});
							$('.choice span').text(txt.slice(0,-1));
							var show_img =$('.goods-img img').eq($_t.index());
							show_img.show().siblings().hide();
							formInput.eq(1).val(show_img.data('id'));
						}
					});
				}
			},error:function () {
				zeroModal.alert({
					content:'服务器错误！',
					width:'80%',
					height:'260px'
				});
			}
		});
		$('.style-modal').find('.price').text($_t.next().text()).end().show();
		$('.shadow').show();
	});

	$('.shadow,.close,.cancel').click(function(){
		$('.style-modal').hide();
		$('.shadow').hide();
		
	});
	$('.confirm').click(function(){
		$('.style-modal').hide();
		$('.shadow').hide();
		$_click.find('.color').text($('.style-color .active').text());
		$_click.find('.version').text($('.style-version .active').text());
		$_click.prev().find('.color').text($('.style-color .active').text());
		$_click.prev().find('.version').text($('.style-version .active').text());
		$_click.hide().prev().find('.title').show().next().show();
		$_click.parents('.cart-content').nextAll('.cart-bottom').find('.edit').show().next().hide();
		$_click.parents('.cart-content').prev().find('img').attr('src',$('.goods-img img').attr('src'));
	});
	$('#payBtn').click(function () {
		var $_v = $('.pay input').eq(1).val();
		if($_v != ''){
			$('#payForm').submit();
		}else{
			zeroModal.alert({
				content:'请选择至少一件商品！',
				width:'80%',
				height:'260px'
			});
		}
    });
});
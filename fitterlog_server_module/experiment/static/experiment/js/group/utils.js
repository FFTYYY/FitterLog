/*** utils ***/
function copy_expe(exp_id){ //创建新实验
	var copy_expe_url = `/experiment/${exp_id}/copy`

	layer_create_ask(config_files , copy_expe_url)
}

function process_state(){//根据状态划分不同的行颜色
	
	//先找到bad-exp，然后向上找到对应的tr，把中间一串元素的颜色全部改掉
	$(".bad-experiment").parentsUntil("tr").css("cssText" , "background-color: #9C0B56FC")
	$(".running-experiment").parentsUntil("tr").css("cssText" , "background-color: #3D3D3D")
}


function remove_panel_title(){ //去掉导出框的中title

	$(".layui-inline").click(function(){ //点击的时候消除弹出框中的所有元素的title
		let me = this
		setTimeout(function(){
			$(me).find(".layui-table-tool-panel *").attr("title" , "")
		} , 50) //停留一下
	})
}

function move_tools(){ //把header的位置移到toolbar里面
	$(".layui-table-tool").append($(".header"))
}

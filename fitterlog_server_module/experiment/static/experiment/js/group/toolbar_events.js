function save_config(table) {

	/* 可编辑的值 */
	var got = get_editable_values()
	var editable_id = got[0]
	var editable_val = got[1]
	for(var i = 0;i < editable_val.length;i++) {
		if(editable_val[i] == "")
			editable_val[i] = " "
	}

	var fixed_left = []
	var fixed_right = []
	/* 左右两侧的固定列 */
	$(".layui-table-fixed-l .layui-table-header th span:not(.layui-table-sort)").each(function(){
		fixed_left.push($(this).text()) //左侧固定
	})
	$(".layui-table-fixed-r .layui-table-header th span:not(.layui-table-sort)").each(function(){
		fixed_right.push($(this).text()) //右侧固定
	})

	var sep_token = "__FITTERLOG__SEP__"
	data = {
		hide_columns: get_hide_headers().join(sep_token) , 
		show_order  : get_show_headers().join(sep_token) , 
		hide_ids    : Array.from(deleted_ids).join(sep_token) , 
		intro       : $(".group-intro").val() , 
		editable_id : editable_id.join(sep_token) , 
		editable_val: editable_val.join(sep_token) , 
		fixed_left 	: fixed_left.join(sep_token) , 
		fixed_right : fixed_right.join(sep_token) , 
	}

	my_post(save_config_url , data)
}

/* 这里修改的全局变量deleted_ids定义在save_and_load.js中 */
/* 当点击delete按钮时，更新deleted_ids，并事实上隐藏他们 */
function hide_checked_rows(table) {
	var checked_data = table.checkStatus("the-table").data //当前那些行是选中的

	//把它们添加进集合
	for(var x of checked_data)
		deleted_ids.add( parseInt(x.id).toString())

	$("tr").each(function(){
		var my_id = $(this).find(".id-teller").attr("my-exp-id") //找到id列对应的exp id
		if(deleted_ids.has(my_id)) {
			$(this).hide() //隐藏之
			$(this).find(".id-teller").attr("hide-by-delete" , true)
		}
	})
}

function get_toolbar_event_func(table){
	return function(obj) {

		switch(obj.event){
			case "go-back": //返回按钮，跳转
				window.location.href = "/project/" + my_project_id
			break
			case "save": //保存按钮，保存设置
				save_config(table)
			break
			case "delete": //删除按钮，删除选中的行
				hide_checked_rows(table)
			break
		}
	}
}
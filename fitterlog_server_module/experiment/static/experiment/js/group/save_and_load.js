/*这个文件主要执行保存config以及从config中加载设置的操作*/
var deleted_ids = new Set()

/* 返回隐藏的列 */
function get_hide_headers() {
	var hide_list = []
	$(".layui-hide").filter("th").each(function(){
		hide_list.push($(this).text())
	})

	return hide_list
}

/* 返回显示的列的顺序 */
function get_show_headers() {
	var show_list = []
	$(".layui-table-header th").each(function(){
		show_list.push($(this).text())
	})

	return show_list
}

/* 返回可编辑单元的id和值（一一对应） */
function get_editable_values(){
	editable_ids = []
	editable_vals = []
	$("td[data-edit='text']").each(function(){
		var my_id = $(this).find(".id-teller").attr("my-id")
		var my_val = $(this).val()
		editable_ids.push(my_id)
		editable_vals.push(my_val)

	})
	return [editable_ids , editable_vals]
}
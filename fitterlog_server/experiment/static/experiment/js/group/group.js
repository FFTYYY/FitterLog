
function move_tools(){
	toolbar = document.getElementsByClassName("layui-table-tool")[0]
	headbar = document.getElementById("header")

	toolbar.appendChild(headbar)
}

function ontabledone(){
	move_tools()
}


layui.use("table", function(){
	table = layui.table
	 
	//转换静态表格
	table.init("main_table", {
		limits: [15,50,100,9999] , 
		page: true , 
		limit: 15 , 
		skin: "row" , 
		height: "full-0" , 
		
		defaultToolbar: [
			{title: "返回", layEvent: 'go-back',icon: 'layui-icon-return',} , 
			{title: "保存设置", layEvent: 'save',icon: 'layui-icon-upload-circle',} , 
			{title: "删除选中行", layEvent: 'delete',icon: 'layui-icon-close',} , 
			"filter", 
			{title: "导出", layEvent: 'LAYTABLE_EXPORT',icon: 'layui-icon-male',} , 
		] ,
		toolbar: true , 
		done: ontabledone , 
	})

	//在toolbar_event.html里定义
	table.on('toolbar', get_toolbar_event_func(table))
});


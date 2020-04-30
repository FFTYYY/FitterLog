
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
			{title: "返回",layEvent: 'go-back',icon: 'layui-icon-return',} , 
			{title: "保存",layEvent: 'save',icon: 'layui-icon-ok',} , 
			"filter", 
			"exports" , 
		] ,
		toolbar: true , 
		done: ontabledone , 
	})

	//在toolbar_event.html里定义
	table.on('toolbar', get_toolbar_event_func(table))
});


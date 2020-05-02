
function remove_panel_title()
{
	var tars = document.getElementsByClassName("layui-inline")

	for(var _t = 0;_t < tars.length;_t ++)
	{
		let tar = tars[_t]
		tar.onclick = function(){

			setTimeout(function(){
				var lls = tar.children

				for(var i = 0;i < lls.length;i++)
				{
					if(!lls[i].classList.contains("layui-table-tool-panel") )
						continue
					for(var j = 0;j < lls[i].children.length;j++)
					{
						lls[i].children[j].title = "" //把title删掉
					}
				}
			} , 50)
		}
	}


}

function move_tools(){
	toolbar = document.getElementsByClassName("layui-table-tool")[0]
	headbar = document.getElementById("header")

	toolbar.appendChild(headbar)
}

function ontabledone(){
	move_tools()
	remove_panel_title()
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


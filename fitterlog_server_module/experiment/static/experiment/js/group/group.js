
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

the_this = undefined
inpus = []
function ontabledone(){
	move_tools()
	remove_panel_title()
	setInterval( process_state , 200)
	
	layui.soulTable.render(this)
	the_this = this
}


layui.use(["table" , "soulTable"] , function(){
	table = layui.table
	 
	//转换静态表格
	table.init("main_table", {
		limits: [15,50,100,9999] , 
		page: true , 
		limit: 15 , 
		skin: "row" , 
		height: "full-0" , 
		done: ontabledone , 

		//工具栏
		toolbar: true , 
		defaultToolbar: [
			{title: "隐藏异常终止的实验", layEvent: "hide-bad",icon: "layui-icon-menu-fill"} , 
			{title: "返回", layEvent: "go-back",icon: "layui-icon-return",} , 
			{title: "保存设置", layEvent: "save",icon: "layui-icon-upload",} , 
			{title: "删除选中行", layEvent: "delete",icon: "layui-icon-close",} , 
			"filter", 
			{title: "导出", layEvent: "LAYTABLE_EXPORT",icon: "layui-icon-male",} , 
		] ,

		//右键菜单
		contextmenu: {
			//header: false , 
			body: [
				{
					name: "细节",
					icon: "layui-icon layui-icon-slider",

					mouseup: function(obj) {
						my_id = obj.elem.children()[0].children[0].getAttribute("my_id")
						new_url = "/variable/" + String(my_id)
						if(event.button == 1) // 中键
						{
							window.open(new_url , "_blank")
						}
						else if(event.button == 0) //左键
						{
							window.location.href = new_url
						}
					},
					children: []
				}

			],
		},
	})

	//在toolbar_event.html里定义
	table.on("toolbar", get_toolbar_event_func(table))

	table.on("sort", function() {
		layui.soulTable.render(the_this) //重新渲染soul-table，否则会失去右键菜单
	})
});


/*** 创建layui table ***/

the_table = undefined
function ontabledone(){
	move_tools()
	remove_panel_title()
	process_state()

	layui.soulTable.render(this)
	the_table = this
}


layui.use(["table" , "soulTable"] , function(){
	var table = layui.table
	
	var ret = get_table_data()
	var data = ret[0]
	var cols = ret[1]

	table.render({
		elem: '#the-table',
		height: 315,
		cols: cols,
		data: data,
		limits: [15,50,100,9999] , 
		page: true , 
		limit: 15 , 
		skin: "row" , 
		height: "full-0" , 
		done: ontabledone , 
		drag: {
			type: "simple" , 
			toolbar: true , 
		},

		//工具栏
		toolbar: true , 
		defaultToolbar: [
			{title: "返回", layEvent: "go-back",icon: "layui-icon-return",} , 
			{title: "保存设置", layEvent: "save",icon: "layui-icon-upload",} , 
			{title: "删除选中行", layEvent: "delete",icon: "layui-icon-close",} , 
			"filter", 
			{title: "导出", layEvent: "LAYTABLE_EXPORT",icon: "layui-icon-male",} , 
		] ,

		//右键菜单
		contextmenu: {
			head: [],
			body: [
				{
					name: "细节",
					icon: "layui-icon layui-icon-slider",

					mouseup: function(obj) {
						var my_id = obj.elem.find(".id-teller").attr("my-id")
						var new_url = "/variable/" + String(my_id)
						if(event.button == 1) // 中键，打开新页面
							window.open(new_url , "_blank")
						else if(event.button == 0) //左键，本页面跳转
							window.location.href = new_url
					},
					children: [],
				}

			],
		},
	})

	//在toolbar_event.html里定义
	table.on("toolbar", get_toolbar_event_func(table))

	table.on("sort", function() {
		layui.soulTable.render(the_table) //重新渲染soul-table，否则会失去右键菜单
		process_state() //重新修改行的颜色
	})
})


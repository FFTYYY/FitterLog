
/*** utils ***/
function copy_expe(exp_id){ //创建新实验
	var copy_expe_url = `/experiment/${exp_id}/copy`

	layer_create_ask(config_files , copy_expe_url)
}

function process_state(){//根据状态划分不同的行颜色
	
	//先找到bad-exp，然后向上找到对应的tr，把中间一串元素的颜色全部改掉
	$(".bad-experiment").parentsUntil("tr").css("cssText" , "background-color: #9C0B56FC !important")
	$(".running-experiment").parentsUntil("tr").css("cssText" , "background-color: #3D3D3D !important")
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

/*** 创建layui table ***/

the_table = undefined
function ontabledone(){
	move_tools()
	remove_panel_title()
	process_state()

	setInterval( process_state , 200) //反复变换颜色

	layui.soulTable.render(this)
	the_table = this
}


layui.use(["table" , "soulTable"] , function(){
	var table = layui.table
	 
	//转换静态表格
	table.init("main-table", {
		limits: [15,50,100,9999] , 
		page: true , 
		limit: 15 , 
		skin: "row" , 
		height: "full-0" , 
		done: ontabledone , 

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
	})
});


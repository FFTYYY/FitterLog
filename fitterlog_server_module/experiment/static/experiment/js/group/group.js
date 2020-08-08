/*** 创建layui table ***/

var the_table = undefined
var the_table_obj = undefined
function ontabledone(){
	move_tools()
	remove_panel_title()
	process_state()
	the_table = this

	layui.soulTable.render(this)
}


layui.use(["table" , "soulTable"] , function(){
	var table = layui.table
	
	// the_table_obj是table返回的对象，而全局变量the_table是实际的table对象，要注意
	the_table_obj = table.render({
		elem: '#the-table',
		
		/*异步数据接口*/
		cols 		: [[]], //获取数据之后再确定
		url 		: get_data_url,
		contentType : "application/json",
		parseData 	: function(ret){

			ret = get_table_data(ret)
			var data = ret[0]
			var cols = ret[1]
			var extr = ret[2]

			// extr中会包含本次request的page和limit，然后通过重载记录这些数据
			// 如果返回的跟上次的不一样，就说明翻了一页，需要重新加载列
			if( (extr.page != this._last_page) || (extr.limit != this._last_limit))
			{
				this.cols = cols //需要先赋为空值，不然reload会出错
				the_table_obj.reload({
					"cols": cols, //通过reload函数来重新加载列

					//记录上次加载的参数，用来确认两次加载是不是同一次
					"_last_page" : extr.page,
					"_last_limit": extr.limit,
				})
			}

			return {
				"code"	: 0,
				"msg"	: "",
				"count"	: extr.tot_num,
				"data"	: data,
			}
		},

		/*基础参数*/
		limits 	: [15,50,100,9999] , 
		page 	: true , 
		limit 	: 15 , 
		skin 	: "row" , 
		height 	: "full-0" , 

		/* 渲染完成的回调 */
		done 	: ontabledone , 

		/* 列拖动（soultable） */
		drag 	: {
			type 	: "simple" , 
			toolbar : true , 
		},

		/* 工具栏 */
		toolbar 	: true , 
		defaultToolbar: [
			{title: "返回", layEvent: "go-back",icon: "layui-icon-return",} , 
			{title: "保存设置", layEvent: "save",icon: "layui-icon-upload",} , 
			{title: "删除选中行", layEvent: "delete",icon: "layui-icon-close",} , 
			"filter", 
			{title: "导出", layEvent: "LAYTABLE_EXPORT",icon: "layui-icon-male",} , 
		] ,

		/* 右键菜单（soultable） */
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
	table.on("toolbar", function(obj){return toolbar_events(obj , table)})

	table.on("sort", function() {
		layui.soulTable.render(the_table) //重新渲染soul-table，否则会失去右键菜单
		process_state() //重新修改行的颜色
	})
})

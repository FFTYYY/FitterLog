/*project页面主程序*/

function start_search(){
	var search_file = $(".search-name-input").val()
	my_post(hyper_search_url , {"search-space" : search_file})
}

var app = new Vue({
	delimiters: ["[[", "]]"],
	el: "#main",

	data: function(){return {
		active_group_id: undefined, //当前哪个group是active的

		config_files: [],
		config_str: "",

		cmd_pref: "",
		cmd_comm: "",
		cmd_entr: "",
		cmd_suff: "",
	}},

	methods:{
		save_config: function() {
			/*保存全局设置*/
			var data = {}
			var sep_token = "__FITTERLOG__SEP__"

			$(".to-save").each(function(){ //添加所有静态待保存单元
				data[$(this).attr("name")] = $(this).val()
			})
			data["config-files"] = this.config_files.join(sep_token) //添加项目设置文件config
			data["cmd-pref"] = this.cmd_pref
			data["cmd-comm"] = this.cmd_comm
			data["cmd-entr"] = this.cmd_entr
			data["cmd-suff"] = this.cmd_suff
			my_post(save_config_url , data)
		},

		group_enter: function(group_id){
			/*鼠标移入了某个group*/
			this.active_group_id = group_id
		},

		/*** config设置的弹出层 ***/
		layer_update_cfgfiles: function(){
			/*添加项目的config文件。注意跟save_config没有关系。注意要保存后才有效
			在添加config文件的弹出层点击确定后调用。
			*/

			var the_str = $(".config-name-input").val()
			the_str = the_str.replace(/(^\s*)|(\s*$)/g, "")	//去掉前后空白符

			this.config_str   = the_str
			this.config_files = the_str.split("\n")
		},
		layer_add_cfgfile: function(){
			/*为项目添加一个config文件。注意跟save_config没有关系*/
			let me = this
			layui.use("layer", function(){
				var layer = layui.layer

				layer.open({
					title: "<p class='title-text'>管理设置文件</p>" , 
					content: `
						<textarea 
							type 			= "text" 
							class 			= "config-name-input" 
							placeholder 	= "config文件名"
							autocomplete 	= "off"

						>${me.config_str}</textarea>
						<a 
							class 	= "layui-icon layui-layer-close layui-layer-close1 my-close config-name-close" 
							onclick = "javascript:app.layer_update_cfgfiles()" title = "关闭窗口"
						>&#xe605;</a>
					` , 
					skin: "my-skin config-layer",
					resize: false,
					closeBtn: 0,
					shade: 0,
					btn: [],
					id: "layer-config",

					area: ["300px" , "150px"],
					//success : on_layer_done,
				})
			})
		},
		/*** 新建实验的弹出层 ***/
		layer_create_expe: function(){
			return layer_create_ask(this.config_files , create_expe_url) //在utils里面定义的新建实验功能
		},
		/*** 超参数搜索的弹出层 ***/
		layer_search: function(){
			layui.use("layer", function(){
				var layer = layui.layer

				layer.open({
					title: "<p class='title-text'>输入搜索空间文件</p>" , 
					content: `
						<input 
							type 			= "text" 
							class 			= "search-name-input Y-color-dark" 
							placeholder 	= "空间定义文件名"
							autocomplete 	= "off"
						/>
						<a 
							class = "layui-icon search-button" title = "开始"
							href = "javascript:void(0)" onclick = "javascript:start_search()"
						>&#xe624;</a>	

						<a 
							class = "layui-icon layui-layer-close layui-layer-close1 my-close" 
							title = "关闭窗口"
						>&#x1006;</a>
					` , 
					skin: "my-skin search-layer",
					resize: false,
					closeBtn: 0,
					shade: 0,
					btn: [],
					id: "layer-search",

					area: ["300px" , "100px"],
					//success : on_layer_done,
				})
			})
		},
		/*** 设置默认命令的弹出层 ***/
		layer_update_cmd: function(){
			this.cmd_pref = $(".pref-input").val()
			this.cmd_comm = $(".comm-input").val()
			this.cmd_entr = $(".entr-input").val()
			this.cmd_suff = $(".suff-input").val()
			console.log(this.cmd_pref)
		},

		layer_set_cmd: function(){
			let me = this
			layui.use("layer", function(){
				var layer = layui.layer

				layer.open({
					title: "<p class='title-text'>设置默认命令</p>" , 
					content: `
						<input class = "set-cmd-input Y-color-dark pref-input"  type = "text" autocomplete = "off"
							  placeholder = "前缀" value = "${me.cmd_pref}"
						/>
						<input class = "set-cmd-input Y-color-dark comm-input"  type = "text" autocomplete = "off"
							  placeholder = "命令" value = "${me.cmd_comm}"
						/>
						<input class = "set-cmd-input Y-color-dark entr-input"  type = "text" autocomplete = "off"
							  placeholder = "入口" value = "${me.cmd_entr}"
						/>
						<input class = "set-cmd-input Y-color-dark suff-input"  type = "text" autocomplete = "off"
							  placeholder = "后缀" value = "${me.cmd_suff}"
						/>

						<a 
							class = "layui-icon layui-layer-close layui-layer-close1 my-close" 
							onclick = "javascript:app.layer_update_cmd()" title = "关闭窗口"
						>&#x1006;</a>
					` , 
					skin: "my-skin set-cmd-layer",
					resize: false,
					closeBtn: 0,
					shade: 0,
					btn: [],
					id: "layer-set-cmd",

					area: ["300px" , "130px"],
					//success : on_layer_done,
				})
			})

		},

	},
})

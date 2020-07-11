/*project页面主程序*/

var app = new Vue({
	delimiters: ["[[", "]]"],
	el: "#main",

	data: function(){return {
		active_group_id: undefined, //当前哪个group是active的

		config_files: [],
		config_str: "",
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
			data["csrfmiddlewaretoken"] = csrf_token //获得密钥

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
					skin: "my-skin config-create-layer",
					resize: false,
					closeBtn: 0,
					shade: 0,
					btn: [],
					id: "layer-config",

					area: ['250px' , '150px'],
					//success : on_layer_done,
				})
			});
		},

		/*** 新建实验的弹出层 ***/
		layer_submit_create: function (){
			/*生成一次实验*/
			var data = {}
			var sep_token = "__FITTERLOG__SEP__"

			data["chosen-config"] = $(".config-manu option:selected").val() //添加项目设置文件config
			data["csrfmiddlewaretoken"] = csrf_token //获得密钥

			my_post(create_expe_url , data)
		},

		layer_get_config_manu: function(){
			//从configs列表，生成下拉菜单
			var s = ""
			for(let f of this.config_files)
				s += `<option value = "${f}">${f}</option>`

			return `<div class = "layui-input-block config-manu"><select>${s}</select></div>`
		},

		layer_create_ask: function(){
			let me = this
			layui.use("layer", function(){
				var layer = layui.layer;

				layer.open({
					title: "<p class='title-text'>新建实验</p>" , 
					content: `
						${me.layer_get_config_manu()}
						<a 
							class = "layui-icon create-button" title = "创建"
							href = "javascript:void(0)" onclick = "javascript:app.layer_submit_create()"
						>&#xe624;</a>	

						<a 
							class = "layui-icon layui-layer-close layui-layer-close1 my-close" 
							title = "关闭窗口"
						>&#x1006;</a>
					` , 
					skin: "my-skin",
					btn: [],
					resize: false,
					closeBtn: 0,
					shade: 0,
					id: "layer-create",
					area: ["200px" , "100px"],
					minWidth: 0,

					//success : on_layer_done,
				});
			});

		},
	},
})

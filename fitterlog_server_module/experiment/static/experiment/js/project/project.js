
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
			var sep_token = "__FITTERLOG__SEP__"
			var for_saving = document.getElementById("for-saving")

			var intros = document.getElementsByClassName("to-save")
			for (var i = 0;i < intros.length;i++)
				this.add_save(for_saving , intros[i].name , intros[i].value)

			add_save(for_saving , "config-files" , this.config_files.join(sep_token))

			for_saving.submit()
		},

		
		add_save: function(for_saving , name , value)
		{
			var opt = document.createElement("textarea");
			opt.name = name;
			opt.value = value;
			for_saving.appendChild(opt)
		},


		header_button: function(idx){
			if (idx == 0){
				location.href = "/"
			}
			else if (idx == 1){
				
			}
			else if (idx == 2){
				console.log(2)
			}
			else if (idx == 3){
				console.log(3)
			}
		},
		group_enter: function(group_id){
			this.active_group_id = group_id
		},

		update_configs: function(){
			var the_ar = document.getElementById("config_name_input")
			config_str = the_ar.value.replace(/(^\s*)|(\s*$)/g, "")//去掉前后空白符
			config_input_w = the_ar.offsetWidth
			config_input_h = the_ar.offsetHeight

			configs = config_str.split("\n") 
		}
		layer_add_config: function(){
			let me = this

			layui.use("layer", function(){
				var layer = layui.layer

				layer.open({
					title: "<p class='title-text'>管理设置文件</p>" , 
					content: `
					<textarea 
						type 			= "text" 
						class 			= "config-name-input" 
						placeholder 	= "config文件名">
					` + me.config_str + `</textarea>
					<a 
						class 	= "layui-icon layui-layer-close layui-layer-close1 my-close" 
						onclick = "javascript:app.update_configs()" title = "关闭窗口">
						&#xe605;
					</a>
					` , 
					skin: "my-skin config-create-layer",
					btn: [],
					resize: false,
					closeBtn: 0,
					shade: 0,

					//success : on_layer_done,
				})
			});
		},
	},
})

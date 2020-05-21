var config_input_w = 150
var config_input_h = 50
function update_configs()
{
	var the_ar = document.getElementById("config_name_input")
	config_str = the_ar.value.replace(/(^\s*)|(\s*$)/g, "")//去掉前后空白符
	config_input_w = the_ar.offsetWidth
	config_input_h = the_ar.offsetHeight

	configs = config_str.split("\n") 
}

function add_config_ask()
{
	layui.use("layer", function(){
		var layer = layui.layer;

		layer.open({
			title: "<p class='title-text'>管理设置文件</p>" , 
			content: '																				\
			<textarea type = "text" id = "config_name_input" autocomplete = "off" placeholder = "config文件名"' + 
			'style = "height:' + config_input_h + 'px;width:' + config_input_w + 'px;">'
			 + config_str + '</textarea>	\
			<a class = "layui-icon layui-layer-close layui-layer-close1 my-close" onclick= "javascript:update_configs()" title = "关闭窗口">&#xe605;</a>\
			' , 
			skin: "my-skin config_create_layer",
			btn: [],
			resize: false,
			closeBtn: 0,
			shade: 0,

			//success : on_layer_done,
		});
	});

}

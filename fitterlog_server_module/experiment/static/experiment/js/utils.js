function my_post(url , data){ //jqury居然只能ajax提交，气死我了
	data["csrfmiddlewaretoken"] = csrf_token //获得密钥

	var form = $(`<form method = 'post' action = '${url}'></form>`)

	for(let x in data){
		let input = $(`<input type = 'hidden' name = '${x}' />`)
		input.val(data[x])
		form.append(input)
	} 

	$(document.body).append(form)
	form.submit()
}


function get_length(text){ //获取一段文本的长度（中文算两个字符）
	var len = 0
	for (var x in text){
		var code = text.charCodeAt(x)
		if (0 <= code && code <= 128) //ascii
			len += 1
		else len += 2
	}
	return len
}

/*** 新建实验的弹出层 ***/
function layer_submit_create (create_url){
	/*生成一次实验*/

	my_post(create_url , {
		"chosen-config": $(".config-manu option:selected").val() //选中的设置文件
	})
}

function layer_get_config_manu(config_files){
	/*从configs列表，生成下拉菜单
	condig_files: config文件名（字符串）的列表
	*/
	var s = ""
	for(let f of config_files)
		s += `<option value = "${f}">${f}</option>`

	return `<div class = "layui-input-block config-manu"><select>${s}</select></div>`
}

function layer_create_ask(config_files , create_url){
	layui.use("layer", function(){
		var layer = layui.layer;

		layer.open({
			title: "<p class='title-text'>新建实验</p>" , 
			content: `
				${layer_get_config_manu(config_files)}
				<a 
					class = "layui-icon create-button" title = "创建"
					href = "javascript:void(0)" onclick = "javascript:layer_submit_create('${create_url}')"
				>&#xe624;</a>	

				<a 
					class = "layui-icon layui-layer-close layui-layer-close1 my-close" 
					title = "关闭窗口"
				>&#x1006;</a>
			` , 
			skin: "my-skin create-layer",
			btn: [],
			resize: false,
			closeBtn: 0,
			shade: 0,
			id: "layer-create",
			area: ["300px" , "100px"],
			minWidth: 0,

			//success : on_layer_done,
		});
	});

}

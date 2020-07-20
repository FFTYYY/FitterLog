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
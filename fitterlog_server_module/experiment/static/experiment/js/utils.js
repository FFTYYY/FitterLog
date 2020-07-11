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

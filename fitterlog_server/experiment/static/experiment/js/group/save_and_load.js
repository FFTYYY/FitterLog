function get_hide_headers() {
	var a_hide_list = document.getElementsByClassName("layui-hide")
	var hide_list = []
	for(var i = 0;i < a_hide_list.length;i++)
	{
		if(a_hide_list[i].tagName == "TH") //表头
		{
			hide_list.push(a_hide_list[i].innerText)
		}
	}
	return hide_list
}

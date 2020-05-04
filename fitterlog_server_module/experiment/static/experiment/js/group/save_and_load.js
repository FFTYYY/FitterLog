
deleted_ids = new Set()

/*更新deleted_ids，并事实上隐藏他们*/
function hide_checked_rows() {
	var checkStatus = table.checkStatus('the_table');
	var checkData = checkStatus.data

	for(var i = 0;i < checkData.length;i++)
	{
		deleted_ids.add(checkData[i].id)
	}


	var the_root = document.getElementsByClassName("layui-table-main")[0]
	var rowlist = the_root.firstElementChild.firstElementChild.children
	var del_idxs = []
	for(var i = 0;i < rowlist.length;i++)
	{
		var r = rowlist[i]
		var flag = false
		for(var j = 0;j < r.children.length;j++)
		{
			if(r.children[j].getAttribute("data-field") == "id")
			{
				if(deleted_ids.has(r.children[j].innerText)) //是一个需要删除的行
				{
					flag = true
					break
				}
			}
		}

		if(flag)
		{
			del_idxs.push(r.getAttribute("data-index"))
		}
	}
	

	var trs = document.getElementsByTagName("tr")
	for(var i = 0;i < trs.length;i++)
	{
		if(del_idxs.indexOf(trs[i].getAttribute("data-index")) >= 0)
			trs[i].hidden = true
	}

	//console.log("ids" , deleted_ids)
	//console.log("idxs" , del_idxs)
}

/*返回隐藏的列*/
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

/*返回显示的列的顺序*/
function get_show_headers() {
	var headers = document.getElementsByClassName("layui-table-header")[0]
	headers = headers.children[0].children[0].children[0].children

	var show_list = []
	for(var i = 0;i < headers.length;i++)
	{
		if(headers[i].tagName == "TH") //表头
		{
			show_list.push(headers[i].innerText)
		}
	}
	return show_list
}

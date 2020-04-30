config = {
	hide_columns: [] , 
	hide_ids: [] , 
}

deleted_ids = new Set()

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


	console.log("ids" , deleted_ids)
	console.log("idxs" , del_idxs)

}

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

function save_config() {
	hide_headers = get_hide_headers()

	config.hide_columns = hide_headers
	config.hide_ids = deleted_ids

}


function change_color(){
	var icons = document.getElementsByClassName("layui-table-tool-self")[0]
	icons = icons.children

	var tar = undefined

	for(var i = 0;i < icons.length;i++)
	{
		if(icons[i].getAttribute("lay-event") != "hide-bad")
			continue
		tar = icons[i] //隐藏坏实验的那个按钮		
	}

	if(hide_bad_exp)
		tar.classList.add("inverse-color")
	else
		tar.classList.remove("inverse-color")
}

function change_hide_bad(){
	hide_bad_exp = !hide_bad_exp
	change_color()

	bad_idx = new Set()

	var bad_exp_inside = document.getElementsByClassName("bad_experiment")
	for(var i = 0;i < bad_exp_inside.length;i++)
	{
		var pa = bad_exp_inside[i].parentElement.parentElement.parentElement

		if(pa.getAttribute("data-index") != null)
			bad_idx.add(pa.getAttribute("data-index"))
	}

	var trs = document.getElementsByTagName("tr")

	for(var i = 0;i < trs.length;i++)
	{
		var pa = trs[i];

		if(pa["hide_by_delete"])
			continue

		if(bad_idx.has( pa.getAttribute("data-index") ))
			pa.hidden = hide_bad_exp
	}
}

function process_state(){
	//根据状态划分不同的行颜色
	change_hide_bad()
	change_hide_bad()

	var bad_exp_inside = document.getElementsByClassName("bad_experiment")
	for(var i = 0;i < bad_exp_inside.length;i++)
	{
		var pa = bad_exp_inside[i].parentElement.parentElement
		pa.style.backgroundColor = "#9C0B56FC"
	}

	var running_exp_inside = document.getElementsByClassName("running_experiment")
	for(var i = 0;i < running_exp_inside.length;i++)
	{
		pa = running_exp_inside[i].parentElement.parentElement
		pa.style.backgroundColor = "#3D3D3D"
	}
}

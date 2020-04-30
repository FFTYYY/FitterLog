function when_unhovor()
{
	//获得动画
	this.classList.add("panel_hover_anime")
	
	//因为动画的执行时间是0.5s，在0.5s后移除动画
	setTimeout(
		function (){
			this.classList.remove("panel_hover_anime")
		}.bind(this),
		500
	)
}


function add_hover_and_unhover_action()
{
	var tars = document.getElementsByClassName("layui-inline")
	tar = undefined
	for(var i = 0;i < tars.length;i++)
	{
		if(tars[i].getAttribute("lay-event") == "LAYTABLE_EXPORT")
			tar = tars[i]
	}

	tar.onclick = function(){

		setTimeout(function(){
			var lls = tar.children

			for(var i = 0;i < lls.length;i++)
			{
				if(!lls[i].classList.contains("layui-table-tool-panel") )
					continue
				for(var j = 0;j < lls[i].children.length;j++)
				{
					lls[i].children[j].onmouseout = when_unhovor
					lls[i].children[j].title = "" //顺便把title删掉
				}
			}
		} , 50)
	}


}

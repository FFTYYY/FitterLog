now_active = undefined

function when_unhivor()
{
	//获得动画
	this.classList.add("group_list_unhover_anime")
	
	//因为动画的执行时间是0.5s，在0.5s后移除动画
	setTimeout(
		function (){
			this.classList.remove("group_list_unhover_anime")
		}.bind(this),
		500
	)
}

function when_hover()
{
	fuck = this
	group_id = this.getAttribute("group_id")

	if (now_active != undefined)
		now_active.classList.add("hidden")

	the_right = document.getElementById("right_content_" + String(group_id))
	the_right.classList.remove("hidden")

	now_active = the_right

}

function add_hover_and_unhover_action()
{
	lls = document.getElementsByClassName("group_list")
	for(var i = 0;i < lls.length;i++)
	{
		lls[i].onmouseenter = when_hover	
		lls[i].onmouseout = when_unhivor	
	}

}


add_hover_and_unhover_action()

now_active = document.getElementsByClassName("default_right")[0]
active_left = document.getElementsByClassName("active_left")[0]

function when_hover()
{
	var group_id = this.getAttribute("group_id")

	if (now_active != undefined)
		now_active.classList.add("hidden")
	var the_right = document.getElementById("right_content_" + String(group_id))
	the_right.classList.remove("hidden")
	now_active = the_right

	if(active_left != undefined)
		active_left.classList.remove("active_left")
	var the_left = document.getElementById("left_content_" + String(group_id))
	the_left.classList.add("active_left")
	active_left = the_left
}

function add_hover_and_unhover_action()
{
	var lls = document.getElementsByClassName("group_list")

	for(var i = 0;i < lls.length;i++)
	{
		lls[i].onmouseenter = when_hover	
	}

}

add_hover_and_unhover_action()

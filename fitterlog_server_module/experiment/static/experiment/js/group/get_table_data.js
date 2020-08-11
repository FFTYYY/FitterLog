/* 根据传回的data生成表头和数据 */

function inner_temp(d , head_name , extr){ //中间格子的模板
	/*
		d: data元素
		head_name: 这一列的列名
		extr: 额外元素，如可编辑列列表
	*/

	/* 额外的类 */
	ex_class = ""
	if (d.state == 3)
		ex_class += " bad-experiment "
	else if(d.state == 0)
		ex_class += " running-experiment "

	if (extr.editable[head_name]) //可编辑
		ex_class += " editable "

	/* 根据可编辑与否决定格子的内容 */
	var content = ""
	if (extr.editable[head_name]) //可编辑格子，放一个input上去
		content = `<input class = "Y-font-short editable-input" value = "${ d.val[head_name] }"/>`
	else //普通格子
		content = `<span>${ d.val[head_name] }</span>`


	return `
		${ content }
		<div 
			my-exp-id = ${d.exp_id} 
			my-id = ${d.vid[head_name]} 
			class = "
				id-teller
				hidden 
				${ex_class}
			"
		></div>
	`
}

function right_temp(d){ //右侧工具栏的模板
	ex_class = ""
	if (d.state == 3)
		ex_class += " bad-experiment "
	else if(d.state == 0)
		ex_class += " running-experiment "

	return `
		<a class = "content-a layui-icon" href = "/experiment/${d.exp_id}/logs">&#xe621;</a>
		<a class = "content-a layui-icon" href = "/experiment//${d.exp_id}/figures">&#xe64a;</a>
		<a class = "content-a layui-icon" href = "javascript:void(0)" 
						onclick = "javascript:copy_expe('/${d.exp_id}')">&#xe656;</a>
		<div 
			my-exp-id = ${d.exp_id}
			class = "
				id-teller
				hidden 

				${ex_class}
			"
		></div>
	`
}

function get_table_data(ret){
	// var ret = JSON.parse( my_get(get_data_url) )
	var data = ret["data"]
	var cols = ret["cols"]
	var extr = ret["extr"]

	/* 给每一列添加template */
	for(let x of cols){
		x.templet = function(d){return inner_temp(d , x.title , extr)}
	}

	var special_style = "background-color: #363636; color: #AAAAAAFF;" //固定格子的特殊style
	cols[0].style = special_style //id列特殊对待

	cols = [{//复选框列
		filed 	: "_checkbox" , 
		type 	: "checkbox" , 
		width 	: 50 ,
		fixed 	: "left" ,
		style: special_style , 
	}].concat(cols)

	cols.push({///右侧工具栏
		field 	: "_right", 
		fixed 	: "right", 
		width 	: 100, 
		align 	: "center" , 
		style 	: special_style , 
		templet : right_temp ,
	})


	return [ data , [cols] , extr]
}
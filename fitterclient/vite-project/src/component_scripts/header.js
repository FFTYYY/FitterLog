import {isnull_list} from "../scripts/utils.js"

export function search_son (nodes , name) {
	/*从nodes中寻找node，返回[所在的list，所在list的index]*/
	for(let i = 0; i < nodes.length; i++) {
		let [ now_name , sons ] = nodes[i]
		if(now_name == name)
			return i
	}
	return -1 //没有找到
}

export function node2titlelist(node){
	// 将node转成titlelist
	let child_list = []
	if(!isnull_list(node.children)){ 
		for(let c of node.children){
			child_list.push(node2titlelist(c))
		}
	}
	return [node.label , child_list]
}


export function get_opr_options(){
	return [
		{
			value: "fitter-opt:exists",
			label: "存在",
		},
		{
			value: "fitter-opt:interval",
			label: "范围",
		},
		{
			value: "fitter-opt:regular",
			label: "正则",
		},

	]
}
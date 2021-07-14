import { h, defineComponent, ref } from 'vue'
import { NText , NButton , NSwitch} from 'naive-ui'
import { make_selector_title } from "../scripts/title_list_process.js"
import { isnull_list } from "../scripts/utils.js"

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


export function on_drop(drag_node , tar_node , drop_pos , full_list){
	// 寻找拿起来的点的container
	let drag_container = full_list
	for(let father of drag_node.fatherlist){
		let idx = search_son(drag_container , father)
		drag_container = drag_container[idx][1]
	}
	let drag_idx = search_son(drag_container , drag_node.label) //拿起来的点是container的第几个
	drag_container.splice(drag_idx, 1) //从drag_container中取出

	// 寻找要放下的点的container
	let tar_container = full_list
	for(let father of tar_node.fatherlist){
		let idx = search_son(drag_container , father)
		tar_container = tar_container[idx][1]
	}
	let tar_idx = search_son(tar_container , tar_node.label) //放下去的点是container的第几个

	if (drop_pos == "inside") {
		tar_container = tar_container[tar_idx][1] //转到tar_node本身
		tar_container.push(node2titlelist(drag_node))
	}
	else {
		if (drop_pos == "before") 
			tar_container.splice(tar_idx    , 0, node2titlelist(drag_node))
		if (drop_pos == "after")
			tar_container.splice(tar_idx + 1, 0, node2titlelist(drag_node))
	}
}

function _get_title_label(vm , titlename , fatherlist){
	let this_title = make_selector_title(titlename , fatherlist)
	let disabled_set = vm.disabled
	let ret = h(
		"span", {}, 
		[
			h(NButton , {
				onClick: ()=> {
					if(disabled_set.has(this_title))
						disabled_set.delete(this_title)
					else
						disabled_set.add(this_title)
				} , 
				text: true , 
			} , {
				default: () => {
					if(disabled_set.has(this_title))
						return "×"
					else
						return "√"
				} 
			}
			) , 
			h(NText , {} , {
				default: () => " " + titlename
			}) , 
		]
	)
	console.log(ret)
	return ret
}

export function get_title_label(vm){
	return (titlename , fatherlist) => {return _get_title_label(vm , titlename , fatherlist)}
}

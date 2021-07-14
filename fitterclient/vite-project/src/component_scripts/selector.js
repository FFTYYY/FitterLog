import { h, defineComponent, ref } from "vue"
import { NText , NButton , NSwitch} from "naive-ui"
import { make_selector_key } from "../scripts/predlist_process.js"
import { isnull_list } from "../scripts/utils.js"

export function get_son_idx (nodes , name) {
	/*从nodes中寻找node，返回[所在的list，所在list的index]*/
	for(let i = 0; i < nodes.length; i++) {
		let [ now_name , sons ] = nodes[i]
		if(now_name == name)
			return i
	}
	return -1 //没有找到
}

export function node2predlist(vm , node){
	// 将node转成predlist
	let child_list = []
	if(!isnull_list(node.children)){ 
		for(let c of node.children){
			child_list.push(node2predlist(vm , c))
		}
	}
	return [
		node.predname , 
		child_list
	]
}

function search_son(container, node){
	// 找到node所在的列表和位置
	for(let father of node.fatherlist){
		let idx = get_son_idx(container , father)
		container = container[idx][1]
	}
	let drag_idx = get_son_idx(container , node.predname) //拿起来的点是container的第几个
	return [container , drag_idx]
}

export function allow_drop(vm , drag_node , tar_node , drop_pos , full_list){
	if(drop_pos == "inside") //不准inside
		return false
	let [ drag_container , drag_idx] = search_son(full_list , drag_node)
	let [ tar_container  , tar_idx ] = search_son(full_list , tar_node)

	return drag_container === tar_container //只能在一个container内拖动
}

export function on_drop(vm , drag_node , tar_node , drop_pos , full_list){
	
	let [ drag_container , drag_idx] = search_son(full_list , drag_node) // 寻找拿起来的点的container
	drag_container.splice(drag_idx, 1)  //从drag_container中取出。必须先取，不然后面的idx就不对了

	let [ tar_container , tar_idx] = search_son(full_list , tar_node)// 寻找要放下的点的container

	// 放进去
	let to_add = node2predlist(vm , drag_node) 

	if (drop_pos == "inside") {
		tar_container = tar_container[tar_idx][1] //转到tar_node本身
		tar_container.push(to_add)
	}
	else {
		if (drop_pos == "before") 
			tar_container.splice(tar_idx    , 0, to_add)
		if (drop_pos == "after")
			tar_container.splice(tar_idx + 1, 0, to_add)
	}
}

function _make_selector_text(vm , predname , fatherlist){
	let this_key = make_selector_key(predname , fatherlist) // 生成这个谓词对应的key
	let disabled_set = vm.disabled
	let ret = h(
		"span", {}, 
		[
			h(NButton , {
				onClick: ()=> {
					if(disabled_set.has(this_key))
						disabled_set.delete(this_key)
					else
						disabled_set.add(this_key)
				} , 
				text: true , 
			} , {
				default: () => { //TODO：更换图标
					if(disabled_set.has(this_key))
						return "×"
					else
						return "√"
				} 
			}
			) , 
			h(NText , {} , {
				default: () => " " + predname
			}) , 
		]
	)
	return ret
}

export function make_selector_text(vm){
	return (predname , fatherlist) => {return _make_selector_text(vm , predname , fatherlist)}
}

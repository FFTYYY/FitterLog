import { h, defineComponent, ref } from "vue"
import { NText , NButton , NSwitch} from "naive-ui"
import { get_real_name } from "../scripts/predlist_process.js"
import { isnull_list } from "../scripts/utils.js"


function search_son(container, node){
	// 找到node所在的列表和位置

	var get_son_idx = function(nodes , name) {
		// 从nodes中寻找node，返回[所在的list，所在list的index]
		for(let i = 0; i < nodes.length; i++) {
			let [ now_name , sons ] = nodes[i]
			if(now_name == name)
				return i
		}
		return -1 //没有找到
	}

	for(let father of node.fatherlist){
		let idx = get_son_idx(container , father)
		container = container[idx][1]
	}
	let drag_idx = get_son_idx(container , node.predname) //拿起来的点是container的第几个
	return [container , drag_idx]
}

function node2predlist(node){
	// 将tree node转成predlist
	let child_list = []
	if(!isnull_list(node.children)){ 
		for(let c of node.children){
			child_list.push(node2predlist(c))
		}
	}
	return [
		node.predname , 
		child_list
	]
}

export function allow_drop(drag_node , tar_node , drop_pos , full_list){
	/* 是否允许拖到此处 
	参数：
		drag_node：正在拖动的树节点 
		tar_node ：将要拖到的树节点
		drop_pos ：放下的位置和将要拖到的树节点的关系（before / after / inside）
		full_list：完整的predlist
	返回值：
		boolean
	*/
	if(drop_pos == "inside") //不准inside
		return false
	let [ drag_container , drag_idx] = search_son(full_list , drag_node)
	let [ tar_container  , tar_idx ] = search_son(full_list , tar_node)

	return drag_container === tar_container //只能在一个container内拖动
}

export function on_drop(drag_node , tar_node , drop_pos , full_list){
	/* 拖动结束，放下元素。这个函数会更新predlist
	参数：
		drag_node：正在拖动的树节点 
		tar_node ：将要拖到的树节点
		drop_pos ：放下的位置和将要拖到的树节点的关系（before / after / inside）
		full_list：完整的predlist
	*/

	let [ drag_container , drag_idx] = search_son(full_list , drag_node) // 寻找拿起来的点的container
	drag_container.splice(drag_idx, 1)  //从drag_container中取出。必须先取，不然后面的idx就不对了

	let [ tar_container  , tar_idx ] = search_son(full_list , tar_node)// 寻找要放下的点的container

	let to_add = node2predlist(drag_node) // 将要放进去的位置

	// 注意虽然 drop_pos 有 inside 这个取值，但是 allow_drop() 中已经拒斥了这种取值。
	if (drop_pos == "before") 
		tar_container.splice(tar_idx    , 0, to_add)
	if (drop_pos == "after")
		tar_container.splice(tar_idx + 1, 0, to_add)
}

function _make_selector_text(vm , predname , fatherlist){
	/* 生成 selector 的每一项的显示的文本。这个函数会调用vue.h()来创建组件。
	参数：
		vm        ：selector的vue组件对象。
		predname  ：这一项的pred名。
		fatherlist：这一项的父组件列表。
	*/
	let this_key = get_real_name(predname , fatherlist) // 生成这个谓词对应的key
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
	/* partial(_make_selector_text , vm = vm) 为了适应predlist_process的格式。*/
	return (predname , fatherlist) => {return _make_selector_text(vm , predname , fatherlist)}
}

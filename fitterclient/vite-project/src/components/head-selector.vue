<!-- 这个模块接受完整的title_list，并允许用户筛选列，返回筛选后的selected_title_list -->

<template>
	<n-button type="primary" @click=open_main>选择器</n-button>

	<n-modal v-model:show="show_main">
	<n-card style="width: 80%;" title="筛选谓词" :bordered="false" size="huge">
		<template #header-extra> 
			<n-button @click=sub_apply>应用</n-button>
			<n-button @click=sub_close>关闭</n-button>
		</template>

		<n-tree
			block-line
			:data="tree_data"
			selectable
			draggable
			:checked-keys="checkedKeys"
			:expanded-keys="expandedKeys"
			@drop="handleDrop"
			@update:checked-keys="handleCheckedKeysChange"
			@update:expanded-keys="handleExpandedKeysChange"

		/>

	</n-card>
	</n-modal>
</template>

<script>
import {make_selector_title , title_process} from "../scripts/title_list_process.js"
import {search_son , node2titlelist} from "../component_scripts/header.js"

export default {
	data(){return {
		draged_title_list: [], // 拖动之后的title_list

		show_main: false,
		expandedKeys: [],
		checkedKeys: [],
		disabled: [],
	}},
	computed: {
		tree_data(){
			return title_process(this.draged_title_list , [] , {
				label: (titlename , fatherlist) => titlename,
				key: make_selector_title ,
				isLeaf: (titlename , fatherlist) => false ,
				fatherlist: (titlename , fatherlist) => fatherlist, 
			} , "children" , {
				isLeaf: (titlename , fatherlist) => true , //覆盖之前生成的属性
			})
		}
	},
	methods: {
		open_main () { //点击按钮时，弹出主界面
			if(!this.show_main){
				this.show_main = true
				this.draged_title_list = JSON.parse(JSON.stringify(this.title_list))
 														//弹出按钮时更新titlelist
														//TODO：应该是merge，暂时随便用一个deepcopy
			}
		},
		sub_apply (){ //点击提交按钮
			//this.$emit("filter-update" , this.filter_items)
			this.show_main = false
		},
		sub_close(){ // 点击关闭按钮
			this.show_main = false
		},

		handleExpandedKeysChange (expandedKeys) {
		  this.expandedKeys = expandedKeys
		},
		handleCheckedKeysChange (checkedKeys) {
		  this.checkedKeys = checkedKeys
		},
		handleDrop (e) {
			let full_list = this.draged_title_list

			let drag_node = e.dragNode
			let tar_node  = e.node
			let drop_pos  = e.dropPosition

			// 寻找拿起来的点的container
			let drag_container = full_list
			for(let father of drag_node.fatherlist){
				let idx = search_son(drag_container , father)
				drag_container = drag_container[idx][1]
			}
			let drag_idx = search_son(drag_container , drag_node.label) //拿起来的点是container的第几个
			drag_container.splice(drag_idx, 1) //从drag_container中取出
			console.log(drag_container , drag_idx)

			// 寻找要放下的点的container
			let tar_container = full_list
			for(let father of tar_node.fatherlist){
				let idx = search_son(drag_container , father)
				tar_container = tar_container[idx][1]
			}
			let tar_idx = search_son(tar_container , tar_node.label) //放下去的点是container的第几个

			if (drop_pos == "inside") {
				tar_container = tar_container[1][tar_idx] //转到tar_node本身
				tar_container.push(node2titlelist(drag_node))
			}
			else {
				if (drop_pos == "before") 
					tar_container.splice(tar_idx    , 0, node2titlelist(drag_node))
				if (drop_pos == "after")
					tar_container.splice(tar_idx + 1, 0, node2titlelist(drag_node))
			}
		}
	},
	setup(){

	},
	props:[
		"title_list" , 
	],
}
</script>
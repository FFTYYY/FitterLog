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
			:selectable="false"
			:allow-drop="allow_drop"
			:on-dragstart="on_dragstart"

			draggable
			default-expand-all
			@drop="ondrop"
		/>

	</n-card>
	</n-modal>
</template>

<script>
import { make_selector_title , title_process } from "../scripts/title_list_process.js"
import { get_title_label , on_drop , allow_drop } from "../component_scripts/selector.js"

export default {
	data(){return {
		show_main: false,      // 主界面是否出现
		dragging_node: undefined , //维护一个当前正在拖动的节点。

		draged_title_list: [], // 拖动之后的title_list
		disabled: new Set(),   // 哪些title不要显示
	}},
	computed: {
		tree_data(){
			let me = this
			let data = title_process(this.draged_title_list , [] , {
				label: get_title_label(me),
				key  : make_selector_title ,
				isLeaf    : (titlename , fatherlist) => false ,
				titlename : (titlename , fatherlist) => titlename,
				fatherlist: (titlename , fatherlist) => fatherlist, 
			} , "children" , {
				isLeaf: (titlename , fatherlist) => true , //覆盖之前生成的属性
			})
			return data
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
			this.$emit("selector-update" , {
				"after-drag": this.draged_title_list ,
				disabled: this.disabled
			})
			this.show_main = false
		},
		sub_close(){ // 点击关闭按钮
			this.show_main = false
		},
		ondrop (e) {
			on_drop(this , e.dragNode , e.node , e.dropPosition , this.draged_title_list)
		},
		allow_drop(info) {
			
			return allow_drop(this , this.dragging_node , info.node , info.dropPosition , this.draged_title_list)
		},
		on_dragstart(info){
			this.dragging_node = info.node
		},
	},
	setup(){

	},
	props:[
		"title_list" , 
	],
	emits:[
		"selector-update" , 
	]
}
</script>
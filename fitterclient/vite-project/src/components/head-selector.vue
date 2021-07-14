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
			draggable
			default-expand-all
			@drop="ondrop"
		/>

	</n-card>
	</n-modal>
</template>

<script>
import { make_selector_title , title_process } from "../scripts/title_list_process.js"
import { search_son , node2titlelist , on_drop } from "../component_scripts/selector.js"
import { get_title_label } from "../component_scripts/selector.js"

export default {
	data(){return {
		draged_title_list: [], // 拖动之后的title_list
		show_main: false,
		disabled: new Set(),
	}},
	computed: {
		tree_data(){
			let me = this
			let data = title_process(this.draged_title_list , [] , {
				label: get_title_label(me),
				key: make_selector_title ,
				isLeaf: (titlename , fatherlist) => false ,
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
			//this.$emit("filter-update" , this.filter_items)
			this.show_main = false
		},
		sub_close(){ // 点击关闭按钮
			this.show_main = false
		},
		ondrop (e) {
			on_drpo(e.dragNode , e.node , e.dropPosition , this.draged_title_list)
		}
	},
	setup(){

	},
	props:[
		"title_list" , 
	],
}
</script>
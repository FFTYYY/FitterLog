<template>
	<n-button type="primary" @click=onclick>选择器</n-button>

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
		/>

	</n-card>
	</n-modal>

</template>

<script>
import {make_selector_title , title_process} from "../scripts/title_list_process.js"

export default {
	data(){return {
		show_main: false,
	}},
	computed: {
		tree_data(){
			return title_process(this.title_list , [] , {
				label: (titlename , fatherlist) => titlename,
				key: make_selector_title ,
				isLeaf: (titlename , fatherlist) => false ,
			} , "children" , {
				isLeaf: (titlename , fatherlist) => true , //覆盖之前生成的属性
			})
		}
	},
	methods: {
		onclick () { //点击按钮时，弹出主界面
			this.show_main = true
		},
		sub_apply (){ //点击提交按钮
			//this.$emit("filter-update" , this.filter_items)
			this.show_main = false
		},
		sub_close(){ // 点击关闭千牛
			this.show_main = false
		}

	},
	setup(){

	},
	props:[
		"title_list" , 
	],
}
</script>
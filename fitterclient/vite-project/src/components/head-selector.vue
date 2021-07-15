<!-- 这个模块接受完整的predlist，并允许用户筛选列，返回筛选后的selected_predlist -->

<template>
<n-button type="primary" @click=visib_click>选择器</n-button>
<n-modal v-model:show="visib_display">

	<n-card style="width: 80%;" title="筛选谓词" :bordered="false" size="huge">
		<template #header-extra> 
			<n-button @click=visib_apply>应用</n-button>
			<n-button @click=visib_close>关闭</n-button>
		</template>

		<n-tree
			block-line
			:data			= tree_data
			:selectable		= false
			default-expand-all

			draggable
			:allow-drop		= dragger_allow_drop
			:on-dragstart	= dragger_on_dragstart
			@drop 			= dragger_ondrop
		/>

	</n-card>
</n-modal>
</template>

<script>
import { get_real_name      , predlist_process } from "../scripts/predlist_process.js"
import { make_selector_text , on_drop , allow_drop } from "../component_scripts/selector.js"

export default {
	data(){return {
		visib_display: false,      // 主界面是否出现
		dragging_node: undefined , //维护一个当前正在拖动的节点。

		draged_predlist: [], // 拖动之后的predlist
		disabled: new Set(),   // 哪些pref不要显示
	}},
	computed: {
		tree_data(){
			let me = this
			let data = predlist_process(this.draged_predlist , [] , {
				label     : make_selector_text (me),
				key       : get_real_name          ,
				isLeaf    : (predname , fatherlist) => false      ,
				predname  : (predname , fatherlist) => predname   ,
				fatherlist: (predname , fatherlist) => fatherlist , 
			} , "children" , {
				isLeaf: (predname , fatherlist) => true , //覆盖之前生成的属性
			})
			return data
		}
	},
	props:[
		"predlist" , 
	],
	methods: {

		// ----- 以下几个 visib 开头的函数是处理弹出框的。 -----

		visib_click () { //点击按钮时，弹出主界面
			if(!this.visib_display){
				this.visib_display = true
			}
		},
		visib_apply (){ //点击提交按钮
			this.$emit("selector-update" , {
				"after-drag": this.draged_predlist ,
				disabled: this.disabled
			})
			this.visib_display = false
		},
		visib_close(){ // 点击关闭按钮
			this.visib_display = false
		},

		// ----- 以下几个 dragger 开头的函数是处理拖动的。 -----
		dragger_ondrop (e) {       // 当放下的时候更新 this.draged_predlist
			on_drop(e.dragNode , e.node , e.dropPosition , this.draged_predlist)
		},
		dragger_allow_drop(info) { // 是否允许放下
			return allow_drop(this.dragging_node , info.node , info.dropPosition , this.draged_predlist)
		},
		dragger_on_dragstart(info){ // 维护目前正在拖动的节点
			this.dragging_node = info.node
		},

	},
	watch: {
		predlist(new_val , old_val){
			this.draged_predlist = JSON.parse(JSON.stringify(this.predlist)) //弹出按钮时更新predlist
		}
	},
	setup(){

	},
	emits:[
		"selector-update" , 
	]
}
</script>
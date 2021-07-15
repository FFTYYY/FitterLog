<!-- 全局组件，控制数据等全局内容

组件结构如下：
main
	table
	header
		filter
		selecter....
 -->

<template>
		<div class = "the_header" ><fitter-header 
			:predlist     = predlist_orig

			@filter-update   = update_filter
			@selector-update = update_selector

		/></div>
		<div class = "the_table" ><fitter-table  
			:predlist   = predlist_proc
			ref 		= "the_table"
		/></div>
</template>

<script>
import { dataloader , make_filter , predlist_process} from "../component_scripts/main.js"
import mytable  from "./table.vue"
import myheader from "./header.vue"

export default {
	data: function(){
		return {
			predlist_orig     : [], // 读到的pred列表
			predlist_proc     : [], // 读到的pred列表
		}
	},
	components: {
		"fitter-table" : mytable,
		"fitter-header": myheader,
	},	
	created() {

		// 开启读取后台数据的循环。
		let me = this
		dataloader.run(
			(predlist) => {me.predlist_orig = predlist}, 
			(data_dict , start , num) => { 
				this.$refs.the_table.push_data(data_dict , start , num) //调用子组件方法
			}
		)

		// 一开始用一个空filter先跑一次，即获得全部数据
		dataloader.update_data({})
	},
	methods: {
		update_filter(filter_items) {
			let filter = make_filter(filter_items)
			dataloader.update_data(filter)
		},
		update_selector(e){
			let after_drag = e["after-drag"]
			let disabled   = e["disabled"]

			this.predlist_proc = predlist_process(after_drag , disabled)
		},
	}

}
</script>

<style>
	.the_header{
		height: 20%;
	}

	.the_table{
		height: 80%;
	}
		
</style>
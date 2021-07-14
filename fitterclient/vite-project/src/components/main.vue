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
			:title_list = title_list_read
			
			@filter-update = update_filter
			@selector-update = update_selector

		/></div>
		<div class = "the_table" ><fitter-table  
			:title_list = title_list_selected
			ref 		= "the_table"
		/></div>
</template>

<script>
import { dataloader , make_filter } from "../component_scripts/main.js"
import mytable  from "./table.vue"
import myheader from "./header.vue"

export default {
	data: function(){
		return {
			title_list_read : [], // 读到的title列表
			title_list_selected : [], // 读到的title列表
		}
	},
	components: {
		"fitter-table" : mytable,
		"fitter-header": myheader,
	},	
	created() {
		let me = this
		dataloader.run(
			(title_list) => {me.title_list_read = title_list}, 
			(data_dict , start , num) => { 
				this.$refs.the_table.push_data(data_dict , start , num) //调用子组件方法
			}
		)
		dataloader.update_data({}) //一开始用一个空filter先跑一次，即获得全部数据
	},
	methods: {
		update_filter(filter_items) {
			let filter = make_filter(filter_items)
			dataloader.update_data(filter)
		},
		update_selector(e){
			let after_drag = e["after-drag"]
			let disabled   = e["disabled"]

			console.log(after_drag , disabled)
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
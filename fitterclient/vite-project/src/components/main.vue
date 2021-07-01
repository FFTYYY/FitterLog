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
			:title_list = title_list

			@filter-update = update_filter
		/></div>
		<div class = "the_table"  ><fitter-table  
			:title_list = title_list
			:data_box   = data_box
		/></div>
</template>

<script>
import { dataloader , make_filter } from "../scripts/main.js"
import mytable  from "./table.vue"
import myheader from "./header.vue"

export default {
	data: function(){
		return {
			title_list : undefined, // 读到的title列表
			data_box   : undefined, // 向table组件传递data_dict所用的prop
		}
	},
	components: {
		"fitter-table" : mytable,
		"fitter-header": myheader,
	},	
	created() {
		let me = this
		dataloader.run(
			(title_list) => {me.title_list = title_list}, 
			(data_dict , start , num) => { me.data_box = [data_dict , start , num]}
		)
		dataloader.update_data({}) //一开始用一个空filter先跑一次，即获得全部数据
	},
	methods: {
		update_filter(filter_items) {
			console.log(filter_items)
			let filter = make_filter(filter_items)
			dataloader.update_data(filter)
		}
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
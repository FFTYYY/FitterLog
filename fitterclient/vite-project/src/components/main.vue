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
			:data_dict  = data_dict
		/></div>
</template>

<script>
import { get_data , make_filter } from "../scripts/main.js"
import mytable  from "./table.vue"
import myheader from "./header.vue"

export default {
	data: function(){
		return {
			title_list: undefined, //读到的title列表
			data_dict : undefined, //读到的名词列表
		}
	},
	components: {
		"fitter-table" : mytable,
		"fitter-header": myheader,
	},	
	created() {
		get_data(this) //填充数据
	},
	methods: {
		update_filter(filter_items) {
			console.log(filter_items)
			console.log(make_filter(filter_items))
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
<!-- 负责根据数据，渲染表格 -->
<template>
	<n-data-table :columns="columns" :data="datas" :pagination="pagination" />
</template>

<script>
import {make_columns , make_datas} from "../scripts/table.js"

export default {
	data: function(){
		return {
			pagination: { // 分页配置。提供给layui。
				page: 1,
				pageSize: 20,
				showSizePicker: true,
				pageSizes: [20, 50, 70],
				onChange: (page) => {
					this.pagination.page = page
				},
				onPageSizeChange: (pageSize) => {
					this.pagination.pageSize = pageSize
					this.pagination.page = 1
				},
			},

			datas: [], // 表格数据。提供给template。每次由data_dict_box()更新
		}
	},
	watch: {
		data_box(new_val , old_val){
			// 一个val是一个data_dict
			let [data_dict , start , num] = new_val //加载了[start,start+num]这个区间的数据

			let data_made = make_datas(data_dict)
			for(let i = start;i < start + num;i++)
				this.datas[i] = data_made[i]
			// TODO: 清空后面的data
		},
	},
	computed: {
		columns() { // 表格头。提供给template。
			return make_columns(this.title_list)
		},
	},
	props: [
		"title_list" , 
		"data_box"  , 
	],
}
</script>

<!-- 负责根据数据，渲染表格 -->
<template>
	<n-data-table :columns="columns" :data="datas" :pagination="pagination" />
</template>

<script>
import {make_columns , make_datas} from "../component_scripts/table.js"

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

			datas: [], // 表格数据。提供给template。每次由push_data更新
		}
	},
	methods: {
		push_data(data_dict , start , num){
			/*这个方法由父组件main调用，用于在接收到data后传递给table。因为接收数据的逻辑是在main中实现的。
			*/
			let data_made = make_datas(data_dict)
			for(let i = start;i < start + num;i++)
				this.datas[i] = data_made[i-start]
			if(this.datas.length > start + num)
				this.datas = this.datas.slice(0,start + num)
			// TODO: 用更帅气的方式清空后面的data
		},
	},
	computed: {
		columns() { // 表格头。提供给template。
			return make_columns(this.title_list)
		},
	},
	props: [
		"title_list" , 
	],
}
</script>

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
		}
	},
	computed: {
		columns: function(){ // 表格头。提供给template。
			return (this.title_list == undefined) ? [] : make_columns(this.title_list[1])
		},
		datas  : function(){ // 表格数据。提供给template。
			return (this.data_dict == undefined) ? [] : make_datas  (this.data_dict )
		},
	},
	props: [
		"title_list" , 
		"data_dict"  , 
	]
}
</script>

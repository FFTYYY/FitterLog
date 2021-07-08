<!-- 负责渲染表头 -->

<template>
	<div>
		<fitter-filter   :title_list=title_list @filter-update=pass_filter_update> </fitter-filter>
		<fitter-selector :title_list=title_list> </fitter-selector>
	</div>
</template>


<script>

import filter   from "./head-filter.vue"
import selector from "./head-selector.vue"

export default {
	components:{
		"fitter-filter"  : filter,  
		"fitter-selector": selector,  
	},
	methods:{
		pass_filter_update(x){ //向上传递filter-update事件
			this.$emit("filter-update" , x)
		}
	},
	props: [
		"title_list", //从远端读到的title列表。由main提供
	],
	emits: [
		"filter-update" , 
	],

}
</script>
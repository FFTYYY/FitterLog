<!-- 负责渲染表头 -->

<template>
	<fitter-filter :title_list=title_list> </fitter-filter>
	<fitter-selector :title_list=title_list> </fitter-selector>
</template>


<script>

import filter   from "./head-filter.vue"
import selector from "./head-selector.vue"

export default {
	components:{
		"fitter-filter"  : filter,  
		"fitter-selector": selector,  
	},
	props: [
		"title_list", //从远端读到的title列表。由main提供
	],
	emits: [
		"filter-update", // 更新过滤器事件。传递给main。
	]

}
</script>
<!-- 负责渲染表头 -->

<template>
	<div>
		<fitter-filter   
			:predlist        = predlist 
			@filter-update   = pass_filter_update
		> </fitter-filter>
		<fitter-selector 
			:predlist        = predlist
			@selector-update = pass_selector_update
		> </fitter-selector>
	</div>
</template>


<script>

import filter   from "./head-filter.vue"
import selector from "./head-selector.vue"

export default {
	components:{
		"fitter-filter"  : filter  ,  
		"fitter-selector": selector,  
	},
	methods:{
		pass_filter_update(x){   //向上传递filter-update事件
			this.$emit("filter-update"   , x)
		},
		pass_selector_update(x){ //向上传递selector-update事件
			this.$emit("selector-update" , x)
		},
	},
	props: [
		"predlist", //从远端读到的pred列表。由main提供
	],
	emits: [
		"filter-update" , 
		"selector-update" , 
	],

}
</script>
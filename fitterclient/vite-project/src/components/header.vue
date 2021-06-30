<!-- 负责渲染表头 -->

<template>
	<fitter-filter :title_list=title_list> </fitter-filter>
</template>


<script>

import filter from "./filter.vue"

export default {
	data: function(){
		return {
			value: null,
		}
	},
	components:{
		"fitter-filter": filter,  
	},
	props: [
		"title_list", //从远端读到的title列表。由main提供
	]
}
</script>
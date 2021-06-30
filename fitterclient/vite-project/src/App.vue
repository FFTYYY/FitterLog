<!-- 顶层组件，控制主题 -->

<template>
	<n-config-provider :theme="darkTheme">

		<div class=main>
			<fitter-main />
		</div>
		<n-global-style />
	</n-config-provider>
</template>

<script>
import { darkTheme } from "naive-ui"
import fittermain  from "./components/main.vue"

export default {
	data: function(){
		return {
			darkTheme: darkTheme,
		}
	},
	components:{
		"fitter-main": fittermain,
	},
}
</script>

<style>

.main{
	height: 500px;
}	
</style>
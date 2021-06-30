<!-- 过滤器 -->

<template>
	<n-button type="primary" @click=onclick>选择器</n-button>

	<n-modal v-model:show="show_main">
		<n-card style="width: 80%;" title="筛选名词" :bordered="false" size="huge">
			<n-dynamic-input
				v-model:value = "filter_item"
				:on-create    = "new_filter_line"
				# = "{ value }"
			>    
				<div style="width: 100%;">
				<div style="display: flex; align-items: center;">
					<n-select v-model:value="value.pred" :options="pred_options" />
					<n-select v-model:value="value.opr"  :options="opr_options" />

					<!-- 输入正则表达式 -->
					<n-input  v-model:value="value.content1" type="input" v-show="show_input(value)" />

					
					<!-- 输入左右区间 -->
					<n-input 
						v-model:value="value.content1" 
						:validator="number_validator"
						v-show="show_number_input(value)"
					/>
					<n-input 
						v-model:value="value.content2" 
						:validator="number_validator"
						v-show="show_number_input(value)"
					/>

				</div>
				</div>
			</n-dynamic-input>

		</n-card>
	</n-modal>

</template>


<script>

import {titlelist2options , get_opr_options} from "../scripts/header.js"

export default {
	data: function(){
		return {
			show_main: false, // 主界面是否出现。提供给template。
			filter_item: [	  // 储存动态录入的值。提供给template。
				{
					pred: "",
					opr: "fitter-opt:exists",
					content1: null, //如果是正则表达式，则这个就是内容
					content2: null, //如果是范围，则这个是右范围
				},
			],
			opr_options: get_opr_options(), //对于每个谓词可以执行哪些操作。提供给template。
		}
	},
	computed: {
		pred_options: function(){ // 选项列表。提供给template。
			if(this.title_list == undefined) return []
			return titlelist2options(this.title_list[1]) 
		}
	},
	methods: {
		onclick () { //点击按钮时，弹出主界面
			this.show_main = true
		},
		new_filter_line () { // 添加一行时的模板
			return {
				pred: "",
				opr: "fitter-opt:exists",
				content1: null, //如果是正则表达式，则这个就是内容
				content2: null, //如果是范围，则这个是右范围
			}
		},

		show_input(value) { //是否显示input框
			return value.opr == "fitter-opt:regular"
		},
		show_number_input(value) { //是否显示input框
			return value.opr == "fitter-opt:interval"
		},

		number_validator(x) { //验证是否为数字
			return ! isNaN( Number(x) )
		},

	},
	props: ["title_list",],
}
</script>
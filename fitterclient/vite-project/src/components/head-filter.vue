<!-- 过滤器 -->

<template>
	<n-button type="primary" @click=open_main>筛选器</n-button>

	<n-modal v-model:show="show_main">
		<n-card style="width: 80%;" title="筛选名词" :bordered="false" size="huge">
			<template #header-extra> 
				<n-button @click=sub_apply>应用</n-button>
				<n-button @click=sub_close>关闭</n-button>
			</template>

			<n-dynamic-input
				v-model:value = "filter_items"
				:on-create    = "new_filter_line"
				# = "{ value }"
			> 
				<div style="width: 100%;">
				<div style="display: flex; align-items: center;">
					<n-select v-model:value="value.pred" :options="pred_options" placeholder="选择谓词"/>
					<n-select v-model:value="value.opr"  :options="opr_options" />

					<!-- 输入正则表达式 -->
					<n-input  
						v-model:value="value.content1" 
						type="input" 
						v-show="show_input(value)" 
						placeholder=正则表达式
					>
						<template #prefix>/</template>
						<template #suffix>/</template>
					</n-input>

					
					<!-- 输入左右区间 -->
					<n-input 
						v-model:value="value.content1" 
						type="input" 
						v-show="show_number_input(value)"
						placeholder=左
					/>
					<n-input 
						v-model:value="value.content2" 
						type="input" 
						v-show="show_number_input(value)"
						placeholder=右
					/>

				</div>
				</div>
			</n-dynamic-input>

		</n-card>
	</n-modal>
</template>


<script>

import {get_opr_options} from "../component_scripts/header.js"
import {make_filter_title , title_process} from "../scripts/title_list_process.js"

export default {
	data: function(){
		return {
			show_main: false, // 主界面是否出现。提供给template。
			noun_left: 0,
			noun_right: -1,
			filter_items: [	  // 储存动态录入的值。提供给template。
				{
					pred: null,
					opr: "fitter-opt:exists",
					content1: null, //如果是正则表达式，则这个就是内容
					content2: null, //如果是范围，则这个是右范围
				},
			],
			opr_options: get_opr_options(), //对于每个谓词可以执行哪些操作。提供给template。
		}
	},
	computed: {
		pred_options(){ // 选项列表
			return title_process(this.title_list , [] , {
				label: (title_name , father_list) => father_list.concat(title_name).join("-"), 
				value: make_filter_title , 
			} , undefined)
		}
	},
	methods: {
		open_main () { //点击按钮时，弹出主界面
			this.show_main = true
		},
		new_filter_line () { // 添加一行时的模板
			return {
				pred: null,
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

		// number_validator(x) { //验证是否为数字
		// 	return ! isNaN( x )
		// },

		sub_apply (){ //点击提交按钮
			this.$emit("filter-update" , this.filter_items)
			this.show_main = false
		},
		sub_close(){ // 点击关闭按钮
			this.show_main = false
		}

	},
	props: [
		"title_list", // title列表。由main传递。
	],
	emits: [
		"filter-update", // 更新过滤器事件。传递给main。
	]
}
</script>
<!-- 过滤器 -->

<template>
	<n-button type="primary" @click=visib_click>筛选器</n-button>

	<n-modal v-model:show="visib_display">
		<n-card style="width: 80%;" title="筛选名词" :bordered="false" size="huge">
			<template #header-extra> 
				<n-button @click=visib_apply>应用</n-button>
				<n-button @click=visib_close>关闭</n-button>
			</template>

			<n-dynamic-input
				v-model:value = "filter_items"
				:on-create    = "new_filter_line"
				# = "{ value }"
			> 
				<div style="width: 100%;">
				<div style="display: flex; align-items: center;">
					<n-select v-model:value="value.pred" :options="pred_options" placeholder="选择谓词"/>
					<n-select v-model:value="value.opr"  :options= "opr_options" />

					<!-- 输入正则表达式 -->
					<n-input  
						v-model:value = "value.content1" 
						v-show        = "show_input(value)" 
						type          = "input" 
						placeholder   = 正则表达式
					>
						<template #prefix>/</template>
						<template #suffix>/</template>
					</n-input>

					
					<!-- 输入左右区间 -->
					<n-input 
						v-model:value = value.content1
						v-show        = show_number_input(value)
						type          = input 
						placeholder   = 左
					/>
					<n-input 
						v-model:value = value.content2
						v-show        = show_number_input(value)
						type          = input
						placeholder   = 右
					/>

				</div>
				</div>
			</n-dynamic-input>

		</n-card>
	</n-modal>
</template>


<script>

import { get_opr_options } from "../component_scripts/header.js"
import { get_real_name , predlist_process } from "../scripts/predlist_process.js"

export default {
	data: function(){
		return {
			visib_display: false, // 主界面是否出现。提供给template。
			filter_items: [	      // 储存动态录入的值。提供给template。
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
			return predlist_process(this.predlist , [] , {
				label: (predname , fatherlist) => fatherlist.concat(predname).join("-"), // 生成给用户看到的文本
				value: get_real_name , // 用realname作为给vue的key
			} , undefined)
		}
	},
	props: [
		"predlist", // pred列表。由main传递。
	],
	methods: {

		// ----- 以下几个 visib 开头的函数是处理弹出框的。 -----

		visib_click () { //点击按钮时，弹出主界面
			this.visib_display = true
		},
		visib_apply (){ //点击提交按钮
			this.$emit("filter-update" , this.filter_items)
			this.visib_display = false
		},
		visib_close(){ // 点击关闭按钮
			this.visib_display = false
		},

		// ----- ----- 
		new_filter_line () { // 添加一行时的模板
			return {
				pred: null,
				opr: "fitter-opt:exists",
				content1: null, //如果是正则表达式，则这个就是内容
				content2: null, //如果是范围，则这个是右范围
			}
		},

		// ----- 以下几个show开头的函数是控制每一行的输入框类型的 -----

		show_input(value) { //是否显示input框
			return value.opr == "fitter-opt:regular"
		},
		show_number_input(value) { //是否显示input框
			return value.opr == "fitter-opt:interval"
		},


	},
	emits: [
		"filter-update", // 更新过滤器事件。传递给main。
	],
}
</script>
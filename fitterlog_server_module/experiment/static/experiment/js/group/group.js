Vue.component("fitter-container", {
	delimiters: ["[[", "]]"],

	template: `
		<div class = "content">
		<slot></slot>
		</div>`
	,
})

Vue.component("fitter-line-x", {
	delimiters: ["[[", "]]"],

	props: ["width" , "top"] , 

	template: `
		<div 
			:style = "{
				position: 'absolute',
				top: top + 'px',
				left: '0',
				height: '1px',
				width: width + 'px',
				border: '0',
				'background-color': '#B2B2B2FF',
			}"
		>
		</div>`
	,
})

Vue.component("fitter-line-y", {
	delimiters: ["[[", "]]"],

	props: {
		height:{} , 
		left:{default: 0} , 
	} , 

	template: `
		<div 
			:style = "{
				position: 'absolute',
				top: '0',
				width: '1px',
				border: '0',
				height: height + 'px',
				left: left + 'px',
				'background-color': '#B2B2B2FF',
			}"
		>
		</div>`
	,
})


Vue.component("fitter-head", {
	delimiters: ["[[", "]]"],

	props: ["text" , "idx"] , 

	data: function(){return {
		height: 50,
		width: 0,
		tot_height: 50,

		cell_cps: [] , //本列的全体cell，按从上到下排列
	}},

	created: function(){
		this.$emit("head-created" , this)
		this.width = get_length(this.text) * 10 + 20
	},

	computed: {
		left_cp:function(){ //自己左边的那个元素。相当于一个链表
			if(this.idx == 0)
				return undefined
			return this.$parent.h_idx2cp(this.idx - 1)
		},

		x: function(){ //真实的横坐标
			if(this.left_cp == undefined) //自己就是最左边元素
				return 0
			return this.left_cp.x + this.left_cp.width
		}
	},

	methods: {
		add_cell: function(c){ //添加一个本列的cell
			this.$set(this.cell_cps , c.idx , c)
		},
		c_idx2cp: function(idx){ //询问这一列第idx个元素是谁
			return this.cell_cps[idx]
		},

	},

	template: `
		<div 
			:style = "{
				width : width + 'px' ,
				height: height + 'px' ,
				'flex-shrink': '0',

			}"
		>
			<p 
				class = "Y-text-center" 
				:style = "{
					height: '100%',
					width: '100%',
				}"
			>[[text]]</p>
		</div>`
	,
})


Vue.component("fitter-cell", {
	delimiters: ["[[", "]]"],

	props: [
		"my_id" 		, // 这个格子的id
		"text" 			, // 这个格子的内容
		"head_text" 	, // 这个格子的头部的i内容
		"tot_head_cps" 	, // 全体头部元素
		"idx" 			, // 这个格子的行号
	] , 

	data: function(){return {
		height: 50,
		head_cp: this.tot_head_cps[this.head_text], //自己头部的那个元素
	}},

	computed: {
		width: function(){ //本格子的宽度
			return this.head_cp.width
		},
		up_cp: function(){ //自己上方的元素，的id列
			if(this.idx == 0) //自己就是最上面的
				return undefined
			return this.head_cp.c_idx2cp(this.idx - 1)
		},
		x: function(){ //x坐标
			return this.head_cp.x
		},
		y: function(){ //真实的y坐标（top）
			if(this.up_cp == undefined) //自己就是最上边的元素
				return this.head_cp.height
			return this.up_cp.y + this.up_cp.height
		},

	},

	created: function(){
		this.$emit("cell-created" , this)

		this.head_cp.width = Math.max(this.head_cp.width , get_length(this.text)*10+20) //更新头部宽度
		this.head_cp.tot_height += this.height
	},

	methods: {
		cl: function(){
			console.log(this.head_cp)
		},
	},

	template: `
		<div 
			:style = "{
				width : width + 'px' ,
				height: height + 'px' ,
				'flex-shrink': '0',

			}"	
			@click = "cl()"

		>
			<p 
				class = "Y-text-center" 
				:style = "{
					height: '100%',
					width: '100%',
				}"
			>[[text]]</p>
		</div>`
	,
})


function start_vue(){
	var app = new Vue({
		delimiters: ["[[", "]]"],
		el: "#main" ,

		data: function(){return {
			heads: [],
			lines: [[]],

			head_cps: {},
			cell_cps: {},
		}},

		computed: {
			tot_width: function(){ //整个表格的长度
				var w = 0
				for(var x in this.head_cps){ //对所有头部的宽度求和
					w += this.head_cps[x].width
				}
				return w
			},
			tot_height: function(){ //整个表格的高度
				if(this.head_cps.id == undefined)
					return 0 //还没初始化好
				return this.head_cps.id.tot_height //用id列的高度作为总高度，因为道理上他们的高度应该是一样的
			},
		},

		methods:{
			h_idx2x: function(idx){ //询问第idx个head的左侧横坐标
				return this.h_idx2cp(idx) == undefined ? 0 : this.h_idx2cp(idx).x
			},
			h_idx2cp: function(idx){ //询问第idx个head的元素是谁
				return this.head_cps[this.heads[idx]]
			},
			c_idx2y: function(idx){ //询问第idx行的top
				let h = this.head_cps.id
				let x = h == undefined ? undefined : h.c_idx2cp(idx)
				return x == undefined ? 0 : x.y
			},


			add_head: function(h){ //一个head创建成功了
				this.$set(this.head_cps , h.text , h)
			},
			add_cell: function(c){ //一个格子创建成功了
				this.$set(this.cell_cps , c.id , c)
				c.head_cp.add_cell(c) //告知对应头部
			},
			cl: function(e){
				console.log(this.$el.scrollLeft)
			},

		},
	})

	return app
}
Vue.component("fitter-line-x", {
	delimiters: ["[[", "]]"],

	props: ["width"] , 

	data: function(){return {
	}},

	template: `
		<div 
			:style = "{
				position: 'absolute',
				left: '0',
				height: '1px',
				width: width + 'px',
				'background-color': 'white',
			}"
		>
		</div>`
	,
})

Vue.component("fitter-head-cell", {
	delimiters: ["[[", "]]"],

	props: ["text"] , 

	data: function(){return {
		height: 50,
		width: 0,
	}},

	created: function(){
		this.$emit("head-created" , this)

		this.width = get_length(this.text) * 10 + 20
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

	props: ["my_id" , "text" , "head_text" , "tot_head_cps"] , 

	data: function(){return {
		height: 50,
		head_cp: this.tot_head_cps[this.head_text],
	}},

	computed: {
		width: function(){
			return this.head_cp.width
		},
	},

	created: function(){
		this.$emit("cell-created" , this)

		this.head_cp.width = Math.max(this.head_cp.width , get_length(this.text)*10+20) //更新头部宽度
	},

	methods: {
		cl: function(){
			console.log(this.head_cp)
		}
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
			tot_width: function(){
				var w = 0
				for(var x in this.head_cps){
					w += this.head_cps[x].width
				}
				return w
			},
		},

		methods:{	
			add_head: function(h){
				this.head_cps[h.text] = h
			},
			add_cell: function(c){
				this.cell_cps[c.id] = c
			},
		},
	})

	return app
}
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

		cell_cps: [] , //���е�ȫ��cell�������ϵ�������
	}},

	created: function(){
		this.$emit("head-created" , this)
		this.width = get_length(this.text) * 10 + 20
	},

	computed: {
		left_cp:function(){ //�Լ���ߵ��Ǹ�Ԫ�ء��൱��һ������
			if(this.idx == 0)
				return undefined
			return this.$parent.h_idx2cp(this.idx - 1)
		},

		x: function(){ //��ʵ�ĺ�����
			if(this.left_cp == undefined) //�Լ����������Ԫ��
				return 0
			return this.left_cp.x + this.left_cp.width
		}
	},

	methods: {
		add_cell: function(c){ //���һ�����е�cell
			this.$set(this.cell_cps , c.idx , c)
		},
		c_idx2cp: function(idx){ //ѯ����һ�е�idx��Ԫ����˭
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
		"my_id" 		, // ������ӵ�id
		"text" 			, // ������ӵ�����
		"head_text" 	, // ������ӵ�ͷ����i����
		"tot_head_cps" 	, // ȫ��ͷ��Ԫ��
		"idx" 			, // ������ӵ��к�
	] , 

	data: function(){return {
		height: 50,
		head_cp: this.tot_head_cps[this.head_text], //�Լ�ͷ�����Ǹ�Ԫ��
	}},

	computed: {
		width: function(){ //�����ӵĿ��
			return this.head_cp.width
		},
		up_cp: function(){ //�Լ��Ϸ���Ԫ�أ���id��
			if(this.idx == 0) //�Լ������������
				return undefined
			return this.head_cp.c_idx2cp(this.idx - 1)
		},
		x: function(){ //x����
			return this.head_cp.x
		},
		y: function(){ //��ʵ��y���꣨top��
			if(this.up_cp == undefined) //�Լ��������ϱߵ�Ԫ��
				return this.head_cp.height
			return this.up_cp.y + this.up_cp.height
		},

	},

	created: function(){
		this.$emit("cell-created" , this)

		this.head_cp.width = Math.max(this.head_cp.width , get_length(this.text)*10+20) //����ͷ�����
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
			tot_width: function(){ //�������ĳ���
				var w = 0
				for(var x in this.head_cps){ //������ͷ���Ŀ�����
					w += this.head_cps[x].width
				}
				return w
			},
			tot_height: function(){ //�������ĸ߶�
				if(this.head_cps.id == undefined)
					return 0 //��û��ʼ����
				return this.head_cps.id.tot_height //��id�еĸ߶���Ϊ�ܸ߶ȣ���Ϊ���������ǵĸ߶�Ӧ����һ����
			},
		},

		methods:{
			h_idx2x: function(idx){ //ѯ�ʵ�idx��head����������
				return this.h_idx2cp(idx) == undefined ? 0 : this.h_idx2cp(idx).x
			},
			h_idx2cp: function(idx){ //ѯ�ʵ�idx��head��Ԫ����˭
				return this.head_cps[this.heads[idx]]
			},
			c_idx2y: function(idx){ //ѯ�ʵ�idx�е�top
				let h = this.head_cps.id
				let x = h == undefined ? undefined : h.c_idx2cp(idx)
				return x == undefined ? 0 : x.y
			},


			add_head: function(h){ //һ��head�����ɹ���
				this.$set(this.head_cps , h.text , h)
			},
			add_cell: function(c){ //һ�����Ӵ����ɹ���
				this.$set(this.cell_cps , c.id , c)
				c.head_cp.add_cell(c) //��֪��Ӧͷ��
			},
			cl: function(e){
				console.log(this.$el.scrollLeft)
			},

		},
	})

	return app
}
var YUI_mixins_components = {
	activable: { //鼠标放上去时进入active状态，也可以通过props设置一直active
		props: ["always_active"] , //always_active：是否保持active状态
		mixins: [YUI_mixins.sense_mouse] , 

		computed:{
			active: function(){
				return this.mouse_in || this.always_active
			},
		},
	}
}

function YUI_components_init(){

	//按钮
	Vue.component("y-button", {
		delimiters: ['[[', ']]'],

		mixins: [YUI_mixins_components.activable] , 

		computed:  {
			//用这种方式来实现hover效果
			classes: function(){ return {
				'Y-text-center' 		: true , 
				'Y-font-short' 			: true , 
				"Y-color-text-light"	: ! this.active, 
				"Y-color-highdark"		: ! this.active,
				"Y-color-text-dark"		: this.active, 
				"Y-color-light"			: this.active,
			}},
		},

		template: `
			<div 
				:class = classes
				@mouseenter.self = mouseenter($event)
				@mouseleave.self = mouseleave($event)
				@click.self = "$emit('y-button-click' , this)"

				:style = "{
					border: '0',
					outline: '0',
				}"
			>
				<slot></slot>
			</div> 
		`, 
	})

	//选项
	Vue.component("y-option", {
		delimiters: ['[[', ']]'],

		mixins: [YUI_mixins_components.activable] , 

		created: function(){
			this.$emit("y-created" , this)
		},

		computed:  {
			//用这种方式来实现hover效果
			classes: function(){ return {
				'Y-text-vertical-center': true , 
				'Y-font-short' 			: true , 
				"Y-color-text-light"	: !this.active, 
				"Y-color-transparent"	: !this.active, 
				"Y-color-text-dark"		: this.active, 
				"Y-color-light"			: this.active,
			}},
		},

		template: `
			<a 
				:class = classes
				@mouseenter.self = mouseenter($event)
				@mouseleave.self = mouseleave($event)

				:style = "{
					'border' 			: '0',
					'outline' 			: '0',
					'text-decoration'	: 'none',
					'transition' 		: '0.5s ease-in',
				}"
			>
				<slot></slot>
			</a> 
		`, 
	})

	//text input
	Vue.component("y-text-input", {
		delimiters: ['[[', ']]'],

		data: function (){return {
			classes: ["Y-color-text-light" , "Y-color-lightdark" , "Y-font-short"] , 
		}} , 

		template: `
			<input
				:class = classes
				type = "text"
			/>
		`, 
	})
	//text area
	Vue.component("y-text-area", {
		delimiters: ['[[', ']]'],

		data: function (){return {
			classes: ["Y-color-text-light" , "Y-color-lightdark" , "Y-font-short"] , 
		}} , 

		template: `
			<textarea
				:class = classes
				type = "text"

				:style = "{
					'resize': 'none',
				}"
			><slot></slot></textarea>
		`, 
	})

}

YUI_components_init()

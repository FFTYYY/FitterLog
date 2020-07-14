/*新建实验页面主程序*/

var app = new Vue({
	delimiters: ["[[", "]]"],
	el: "#main",

	data: function(){return {

	}},

	mounted: function(){
		let me = this
		$(".inner-default").each(function(){
			let init_value = $(this).val()
			let init_bgcolor = $(this).css("background-color")

			$(this).change(function(){
				if($(this).val() == init_value)
					$(this).css("background-color" , init_bgcolor)
				else
					$(this).css("background-color" , "#3D3D3DFF")
			})
		})
	},


	methods:{
		finish_create: function(){
			data = {}
			$(".to-save").each(function(){ //添加所有变量
				data[$(this).attr("name")] = $(this).val()
			})

			data["__FITTERLOG__CONFIG__"] = config_name
			data["__last_page_path"] 	  = last_page_path //如果不以双下划线开头就会被以为是变量


			my_post(finish_create_url , data)
		}

	},
})

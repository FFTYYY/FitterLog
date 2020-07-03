var YUI_style_functions = {
	"Y-text-vertical-center": function(x){
		x.css("line-height" , x.height() + "px")
	},
	"Y-text-center": function(x){
		YUI_style_functions["Y-text-vertical-center"](x)
	},
}


$(document).ready(function(){
	for(let x in YUI_style_functions)
		YUI_style_functions[x]( $("."+x) )
})
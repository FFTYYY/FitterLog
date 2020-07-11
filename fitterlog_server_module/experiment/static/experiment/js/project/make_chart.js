/*使用highcharts.js生成project页面的图表*/
var _charts = []

function add_chart(container_id , tot_num , state_num){
	/*
		container_id: 要把chart放到哪一个容器中（容器id）
		tot_num: 实验总数
		state_num: 4元组。各种状态的实验数量
	*/

	let new_chart = Highcharts.chart(container_id, {
		chart: {
			spacing: [0,0,0,0] , 
			margin: [0,0,0,0] , 
		},
		credits: false , 
		title: {
			floating: true,
			text: `实验数：${tot_num}` , 
			style: { 
				"color": "#E0E0E0", 
				"fontSize": 15,
			} , 
		},
		plotOptions: {
			pie: {
				borderWidth: 0 , 
				allowPointSelect: true,
				cursor: "pointer",
				dataLabels: {
					enabled: true,
					format: "<b>{point.name}</b>: {point.y}",
					color: "#E0E0E0" , 
					style: {
						"textOutline": "0px 0px contrast"
					}
				},
				point: {
					events: {
						mouseOver: function(e) {
							var new_text = e.target.name + "："+ (parseInt(e.target.percentage*100)/100) + " %"
							new_chart.setTitle({
								text: new_text , 
							})
						} , 
						mouseOut: function(e) {
							new_chart.setTitle({
								text: `实验数：${tot_num}` , 
							})
						} , 
					} , 
				},
			}
		},
		series: [{
			type: "pie",
			innerSize: "80%",
			name: "数量",
			data: [
				["已完成"	,	state_num[1] + state_num[2] ],
				["异常终止"	,	state_num[3] ],
				["未完成"	,	state_num[0] ],
			]
		}]
	}, function(c) {
		// 环形图圆心
		var center_y = c.series[0].center[1]
		var title_height = parseInt(c.title.styles.fontSize)

		// 动态设置标题位置
		c.setTitle({
			y: center_y + title_height/2 , 
		})
	});

	_charts.push(new_chart)
}

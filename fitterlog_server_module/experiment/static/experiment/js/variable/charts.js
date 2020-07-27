var charts = []
function make_all_cont(var_name , series){
	var chart = Highcharts.chart("all-container", {
		title: {
			text: `All Tracks of Variable 【${var_name}】`,
		},
		credits: false , 
		yAxis: {
			title: {
				text: "Value",
			}
		},
		legend: {
			layout: "vertical",
			align: "right",
			verticalAlign: "middle",
		},
		plotOptions: {
			series: {
				label: {
					connectorAllowed: false,
				},
			}
		},
		series: series,

		responsive: {
			rules: [{
				condition: {
					maxWidth: 500,
				},
				chartOptions: {
					legend: {
						layout: "horizontal",
						align: "center" ,
						verticalAlign: "bottom",
					}
				}
			}]
		}
	})
	charts.push(chart)
}

function make_chart(tra_id , tra_name , var_name , data){
	var chart = Highcharts.chart(`container-${tra_id}`, {
		title: {
			text: `Tracks 【${tra_name}】 of Variable 【${var_name}】`
		},
		credits: false , 
		yAxis: {
			title: {
				text: "Value",
			}
		},
		xAxis: {
			title: {
				text: "Time",
			}
		},
		legend: {
			layout: "vertical",
			align: "right",
			verticalAlign: "middle",
		},
		plotOptions: {
			series: {
				label: {
					connectorAllowed: false,
				},
			}
		},
		series: [
			{
				name: tra_name,
				data: data,
			} , 
		],

		responsive: {
			rules: [{
				condition: {
					maxWidth: 500,
				},
				chartOptions: {
					legend: {
						layout: "horizontal",
						align: "center",
						verticalAlign: "bottom",
					}
				}
			}]
		}
	})

	charts.push(chart)
}

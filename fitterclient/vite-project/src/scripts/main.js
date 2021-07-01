import axios from "axios"

function isnull(o){
	return o == null || o == undefined || o == ""
}

export function make_filter(filter_items){
	/* 将filter类输出的filter_items转成通知后端用的格式
	参数：
		filter_items: 形如[
			{
				pred: "n",
				type: "exists",
			},
			{
				pred: "m",
				type: "regular",
				cond: "\d*"
			},
			{// bad filter
				pred: null,
			}
		]

	返回值：形如{
		"n":{
			type: exists,
		},
		"m":{
			type: regular,
			cond: "\d*"
		}
	}
	*/
	let filter = {}
	for(let item of filter_items){
		if(item.pred == null) continue

		if(item.opr == "fitter-opt:exists")
		{
			filter[item.pred] = {
				"type" : "exists",
			}
		}
		if(item.opr == "fitter-opt:regular")
		{
			filter[item.pred] = {
				"type" : "regular",
				"cond" : isnull(item.content1) ? "" : item.content1, // null转成匹配全部
			}
		}
		if(item.opr == "fitter-opt:interval")
		{
			filter[item.pred] = {
				"type" : "interval",
				"cond" : [
					isnull(item.content1) ? "-inf" : item.content1, // null转成inf
					isnull(item.content2) ? "inf"  : item.content2,
				], 
			}
		}
	}
	return filter
}

/* ----- 以下是关于数据传输的模块 ----- */

function mergetitle(title_list_1 , title_list_2){
	/*	合并两个title_list

	titlelist：形如 [  ["loss" , [ ["train" , []] , ["test" , []] ]]  , ["acc" , []] ]
	*/

	// given pred and sons, return a list item 
	let make_list = (pred,sons) => ( sons.length == 0 ? [pred] : [pred , sons] )

	let has = {} // has[pred] = [1] / [2] / [1,2]

	for(let pred_info of title_list_1){
		let pred = pred_info[0]
		let sons = pred_info[1]
		has[pred_name] = {
			1: sons
		}
	}
	for(let pred_info of title_list_2){
		let pred = pred_info[0]
		let sons = pred_info[1]
		if (has[pred] == undefined)
			has[pred] = {}

		has[pred][2] = sons
	}


	let ret = []
	for(let pred in has){
		if(has[pred][2] == undefined){ // only 1
			ret.push([pred , has[pred][1]])
		}
		else if(has[pred][1] == undefined){ // only 2
			ret.push([pred , has[pred][2]])
		}
		else{ //1 and 2
			sons = mergetitle(has[pred][1] , has[pred][2])
			ret.push( [pred , sons] )
		}
	}

	return ret

}

async function get_data(ip , filter , start , trans_size , searc_size){
	/* 从 start开始，找num个符合filter的名词传过来
	返回值： 
		title_list
		data_dict
		num_loaded: 成功传输了多少个
		pos: 目前搜索到的位置，-1表示到头了
	*/

	// 请求数据
	let resp = await axios.post(`http://${ip}/ask_datas` , {filter , start , trans_size , searc_size})

	let title_list = resp.data["title_list"]
	let data_dict  = resp.data["data_dict" ]
	let num_loaded = resp.data["num_loaded"]
	let pos    = resp.data["pos"   ]

	return [title_list , data_dict , num_loaded , pos ]


	// v.$data.title_list = title_resp.data
	// v.$data.data_dict  = data_resp .data
}


// 一个线程对象，每次接受数据获取请求，然后去下载远端数据并更新数据。
// 同步的方法是，这个线程本身会永远运行，但是一旦数据更新完成就进入等待，并设置一个_cur_resolve对象，有
// 新数据时通过调用这个函数来触发线程。
// 因此获取数据的行为始终是同步的，只是异步更新筛选条件。
// 必须保证，每次要重新筛选条件时，都去调用了this._cur_resolve()
export let dataloader = {
	trans_size: 50,   //每次最多传输多少个名词，这个限制是为了让网络不要花太长时间
	searc_size: 2000, //每次最多搜索多少个名词。这个限制是为了让后端不要累着
	ip: "127.0.0.1:7899",

	cur_title: [],
	cur_pos   : -1, // 目前已经加载的元素的最大编号。-1表示已经到头了
	cur_loaded: 0 , // 目前已经加载的元素的个数

	filter: null, // 筛选条件。由update()负责维护。

	_cur_resolve: null, // _wait_new_data()的resolve函数。

	run: async function(push_title , push_data){
		while(true){

			while(this.cur_pos < 0)
				await this._wait_new_data()

			let [title_list , data_dict , num_loaded , pos] = await get_data(
				this.ip , this.filter , this.cur_pos ,  this.trans_size , this.searc_size
			)
			// 直接返回的title_list类似于["root" , [ ... ] ] ， 所以要先取[1]
			this.cur_title = mergetitle(this.cur_title , title_list[1]) 

			push_title(this.cur_title) // 通知父函数最新的title_list
			push_data(data_dict , this.cur_loaded , num_loaded) // 通知父函数新获得的data

			this.cur_pos    = pos //pos需要保证：-1的话表示到头了
			this.cur_loaded = this.cur_loaded + num_loaded
		}

	},
	async update_data(filter) { // 只有这个函数会触发数据更新

		// 据说js是单线程的，所以这个函数一定会原子的执行到结束，不用担心异步问题。

		this.filter     = filter
		this.cur_title  = []
		this.cur_loaded = 0
		this.cur_pos    = 0 //设为1表示开始加载了

		// 唤醒 run() 函数
		if(this._cur_resolve != null){
			this._cur_resolve()
			this._cur_resolve = null
		}
	},

	_wait_new_data(){ // 一个promise函数，等待新数据
		let me = this
		return new Promise((resolve) => {
			me._cur_resolve = resolve
		})
	}

}


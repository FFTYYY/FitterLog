
/*** utils ***/
function copy_expe(exp_id){ //������ʵ��
	var copy_expe_url = `/experiment/${exp_id}/copy`

	layer_create_ask(config_files , copy_expe_url)
}

function process_state(){//����״̬���ֲ�ͬ������ɫ
	
	//���ҵ�bad-exp��Ȼ�������ҵ���Ӧ��tr�����м�һ��Ԫ�ص���ɫȫ���ĵ�
	$(".bad-experiment").parentsUntil("tr").css("cssText" , "background-color: #9C0B56FC")
	$(".running-experiment").parentsUntil("tr").css("cssText" , "background-color: #3D3D3D")
}


function remove_panel_title(){ //ȥ�����������title

	$(".layui-inline").click(function(){ //�����ʱ�������������е�����Ԫ�ص�title
		let me = this
		setTimeout(function(){
			$(me).find(".layui-table-tool-panel *").attr("title" , "")
		} , 50) //ͣ��һ��
	})
}

function move_tools(){ //��header��λ���Ƶ�toolbar����
	$(".layui-table-tool").append($(".header"))
}

/*** ����layui table ***/

the_table = undefined
function ontabledone(){
	move_tools()
	remove_panel_title()
	process_state()

	layui.soulTable.render(this)
	the_table = this
}


layui.use(["table"] , function(){
	var table = layui.table
	 
	table.render({
		elem: '#the-table',
		height: 315,
		url: get_data_url,
		cols: table_cols,
		contentType: "application/json",
		parseData: function(res){ //res ��Ϊԭʼ���ص�����
			console.log(res.data)
			return {
			  "code" 	: res.code,
			  "msg" 	: res.msg,
			  "count" 	: res.count,
			  "data" 	: res.data
			}
		},

		limits: [15,50,100,9999] , 
		page: true , 
		limit: 15 , 
		skin: "row" , 
		height: "full-0" , 
		done: ontabledone , 
		drag: {
			type: "simple" , 
			toolbar: true , 
		},

		//������
		toolbar: true , 
		defaultToolbar: [
			{title: "����", layEvent: "go-back",icon: "layui-icon-return",} , 
			{title: "��������", layEvent: "save",icon: "layui-icon-upload",} , 
			{title: "ɾ��ѡ����", layEvent: "delete",icon: "layui-icon-close",} , 
			"filter", 
			{title: "����", layEvent: "LAYTABLE_EXPORT",icon: "layui-icon-male",} , 
		] ,

		//�Ҽ��˵�
		contextmenu: {
			head: [],
			body: [
				{
					name: "ϸ��",
					icon: "layui-icon layui-icon-slider",

					mouseup: function(obj) {
						var my_id = obj.elem.find(".id-teller").attr("my-id")
						var new_url = "/variable/" + String(my_id)
						if(event.button == 1) // �м�������ҳ��
							window.open(new_url , "_blank")
						else if(event.button == 0) //�������ҳ����ת
							window.location.href = new_url
					},
					children: [],
				}

			],
		},
	})

	//��toolbar_event.html�ﶨ��
	table.on("toolbar", get_toolbar_event_func(table))

	table.on("sort", function() {
		layui.soulTable.render(the_table) //������Ⱦsoul-table�������ʧȥ�Ҽ��˵�
		process_state() //�����޸��е���ɫ
	})
})


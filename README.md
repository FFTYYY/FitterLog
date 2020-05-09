伪·魔改版fitlog

总得来说使用逻辑跟[fitlog](https://github.com/fastnlp/fitlog)差不多

## 安装和启动服务

`pip install fitterlog`

## 在代码中使用

首先创建一个实验
```
from fitterlog.interface import new_or_load_experiment

expe = new_or_load_experiment(project_name = "<project_name>" , group_name = "<group_name>")
```
其中 project_name 是你的项目的名称，group_name 是这个实验所属的实验组的名称。后者默认为default。<br/>
而`expe`代表本次实验。

在创建实验之后，再次调用`new_or_load_experiment`可以得到之前创建的那个实验（这个时候不需要传参数）。

#### 记录超参数
使用`ArgProxy`来代替`argparse`：

```
from fitterlog.arg_proxy import ArgProxy

prox = ArgProxy()                                    #等价于 pars = ArgumentParser()

prox.add_argument("n" , type = int , default = 0)    #等价于 pars.add_argument("--n" , type = int , default = 0)
prox.add_store_true("use_cuda")                      #等价于 pars.add_argument("--use_cuda" , action = "store_true")

config = prox.assign_from_cmd()                      #等价于 config = pars.parse_args()
```

可以将`prox`赋给`expe`来记录超参数：
```
expe.use_argument_proxy(prox)
```

#### 记录变量

为一个实验创建变量：
```
expe.new_variable("<variable_name>" , type = <variable_type> , default = <default_value>)
```
其中 variable_name 是变量的名称，variable_type 是变量的类型，default_value 是变量的默认（初始）值。

##### 访问变量
```
print( expe["<variable_name>"].value )
```

##### 更新变量
```
expe["<variable_name>"].update(<new_value> , time_stamp = <time_stamp>)
```
new_value 是新的变量值。time_stamp 是本次更新的时间戳。<br/>
time_stamp 默认为上次的时间戳+1（初始默认为0）


## 访问前端
使用命令`fitterlog-start-server -p <port>`启动服务。port 默认为8000。

使用url `<服务器地址>:<port>`即可访问前端。（前端的具体操作<ruby>自己摸索吧<rt>懒得写了</rt></ruby>）

## 高级功能

* 使用`add_argument(editable = True)`可以让某个变量可以在前端修改，类似于fitlog中的memo，不过更灵活。

* 一个变量可以同时记录多组值。示例：<br/>
```
    expe["loss"].new_track("dev")
    expe["loss"].new_track("test")
    expe["loss"]["dev"].update(balabala)
    expe["loss"]["test"].update(balabala)
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;使用的时候不`new_track`也可以，他会自动创建track。

* 使用`expe.add_line`可以向前端写文字版log，相当于fitlog的`fitlog.add_to_line`（没错我刚刚才发现名字打错了，本来是想跟fitlog一致的）

* 还有很多功能<ruby>自己摸索吧<rt>懒得写了</rt></ruby>

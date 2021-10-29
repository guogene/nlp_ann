# nlp标注平台
> 一个简易文本标记平台,支持用户权限,标签管理,标注数据存储功能

![](https://img.shields.io/badge/python-3.6-blue)
![](https://img.shields.io/badge/apache-cgi-red)
![](https://img.shields.io/badge/vue-build-green)

1.apache做web服务器

2.python编写cgi提供接口. 

3.前端采用vue框架搭建



## 安装
DOCKER 一键启动
```
在项目根目录
docker build -t poplar:v1 .

docker run -itd --name poplar -v $(pwd)/ann_data:/home/ann_data -p8012:80 poplar:v1

启动成功后,打开浏览器 访问 http://localhost:8012/poplar  即可。

数据:
	ann_data 通过挂载的方式, 可直接修改本地文件夹, 容器会读取本地文件的变更。
	user_info.json 用于配置账号信息

```

OS X & Linux:

```sh
前端:
	npm install 
	npm build
后端:
	将cgi-bin中的接口文件移至 apache的 /var/www/cgi-bin 目录下,并提供可执行权限(chmod)
	将打包好的前端 dist中的文件放置 /var/www/html/poplar 目录下, 无poplar文件夹自行创建
数据:
	ann_data文件夹存放到适合的目录,并修改 cgi-bin/base_cgi.py 中的配置路径, 并提供可读写权限(chmod)
	user_info.json 用于配置账号信息

```

Windows:

```sh
前端:
	npm install 
	npm build
后端:
	将cgi-bin中的接口文件移至 apache的 apache/www/cgi-bin 目录下,并提供可执行权限(chmod)
	将打包好的前端 dist中的文件放置 apache/www/html/poplar 目录下, 无poplar文件夹自行创建
数据:
	ann_data -> 文件夹存放到适合的目录,并修改 cgi-bin/base_cgi.py 中的配置路径, 并提供可读写权限(chmod)
	user_info.json -> 用于配置账号信息
	label_data.json -> 完成后的标注信息存储
	label_templete.json -> 标签模板的储存
```

## 使用

```sh
部署完成后, 访问 http://remote_ip/poplar
需要标注的文本文件,放置ann_data/task_data 文件夹下, 注意文件名不能重复!! 且历史名称也不要重复,采用文件名做唯一标识

```

## 图例
[![yEZi6A.png](https://s3.ax1x.com/2021/01/31/yEZi6A.png)](https://imgchr.com/i/yEZi6A)
[![yEZAmt.png](https://s3.ax1x.com/2021/01/31/yEZAmt.png)](https://imgchr.com/i/yEZAmt)
[![yEZFOI.png](https://s3.ax1x.com/2021/01/31/yEZFOI.png)](https://imgchr.com/i/yEZFOI)
[![yEZE0P.png](https://s3.ax1x.com/2021/01/31/yEZE0P.png)](https://imgchr.com/i/yEZE0P)


## 其他

guogene – guoxinjiede@gmail.com

[![yEZW1H.png](https://s3.ax1x.com/2021/01/31/yEZW1H.png)](https://imgchr.com/i/yEZW1H)


## 感谢

前端核心标注组件采用 synyi.ai 下的[poplar](https://github.com/synyi/poplar)二次开发


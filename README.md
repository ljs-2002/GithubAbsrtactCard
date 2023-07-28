# Github Card

- 创建关于Github仓库的摘要卡片
- 目前只支持生成`svg`格式

## Table of Contents

[Example](#example)

[Install](#install)

- [Python 脚本](#python脚本安装)
- [TamperMonkey插件](#TamperMonkey插件安装)

[Usage](#usage)

- [Python脚本使用](#python脚本使用)
- [TamperMonkey插件使用](#TamperMonkey插件使用)

[TODO](#todo)

[Reference](#reference)

[License](#license)

## Example

- 生成的卡片如下所示，包含
  - 仓库名；
  - 作者名和头像；
  - 仓库简介；
  - 仓库的信息，包括使用的语言、Star数等。
- 点击仓库名可直接跳转到仓库，点击作者头像和名字可以直接跳转到作者主页，点击Star数等位置可直接跳转到相应的详情页。

![Example](assets/ljs-2002_GithubCard.svg)

## Install

- 提供了Python脚本和TamperMonkey插件，其中油猴插件在`./script`下。

### Python脚本安装

- 程序依赖在`requirements.txt`下，在命令行中使用下列命令安装依赖：

  ```shell
  python -m pip install -r requirements.txt
  ```

  

### TamperMonkey插件安装

1. 通过浏览器的应用商店安装TamperMonkey扩展；
2. 将代码克隆到本地；
   - 也可在[Releases](https://github.com/ljs-2002/GithubCard/releases)中下载并解压插件；
3. 在TamperMonkey扩展中选择**管理面板**→**实用工具**→**导入**，将源码目录下`./script`中的`GithubCard.js`文件/在Releases中下载的插件导入；
   - 也可在TamperMonkey扩展中选择**添加新脚本**，复制`./script/GithubCard.js`中的所有内容并粘贴到编辑器内；

**:heavy_exclamation_mark:插件已经发布到[Greasy Fork](https://greasyfork.org/zh-CN/)，搜索`GithubCard`即可找到本插件并直接安装；**

## Usage

### Python脚本使用

- 使用Python脚本时，可在命令行下运行`cli.py`文件来生成图片。

- 运行下列命令查看命令行参数帮助：

  ```shell
  > python cli.py -h
  ```

- 参数说明

  | 参数                      | 说明                                                         |
  | ------------------------- | ------------------------------------------------------------ |
  | -h/--help                 | 显示help信息                                                 |
  | -r/--repo [REPO_NAME]     | 指定目标仓库，REPO_NAME的格式为`onwer/repo`                  |
  | -o/--output [OUTPUT_NAME] | （可选）指定输出的文件名，若不指定则默认储存为`./img/[owner]_[repo].svg`，`./img`文件夹若不存在会自动创建 |



### TamperMonkey插件使用

- 安装并启用插件后，当访问`Github`仓库时，会在屏幕左侧中间显示一个绿色按钮，鼠标移动到按钮上时按钮会弹出并显示**Get Card**字样。点击该按钮即可生成并下载当前仓库的摘要卡片。
- :bulb: 注意：在点击按钮后需要稍等几秒钟才会弹出下载提示，若一直没有下载提示请打开网页控制台查看报错。



## TODO

- [ ] 增加支持导出的格式
- [ ] 增加显示仓库的Topics信息
- [ ] 增加个人主页的摘要卡片生成



## Reference

- 本项目参考了[nwtgck/gh-card:  GitHub Repository Card for Any Web Site](https://github.com/nwtgck/gh-card)



## License

- 遵循 [Apache License 2.0](https://github.com/ljs-2002/GithubCard/blob/main/LICENSE)
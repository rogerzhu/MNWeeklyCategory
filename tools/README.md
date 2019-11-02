# 代码全解析

## 代码依赖
本repo主要是用python编写，在无脑跑起整个项目之前，需要安装以下依赖：
```
pip3 install selenium
pip3 install requests
pip3 install BeautifulSoup4
pip3 install click
```

前三个都是爬虫和解析所要用的工具，第四个是强大的python命令行构建工具

除了这些，还需要安装一个webdriver，而这个是根据你对浏览器的喜好和系统选择的，具体的可以参照下面：
* [Chrome](http://chromedriver.storage.googleapis.com/index.html)
* [Firefox](https://github.com/mozilla/geckodriver/releases/)
* [IE](http://www.nuget.org/packages/Selenium.WebDriver.IEDriver/)

弄完这些，就可以准备心情开始无脑运行的步骤了。

## 我要做什么
对于这个repo，我想做的主要其实就是以下两点：
* 获取码农周刊第一期到当前最新一期的所有内容，做一个分类展示
* 可以处理以后的每一期的更新，人工干预的越少越好

大饼已经画好了，考虑到我是一个程序员，秉承着能让机器帮我干事就就不应该自己费力气的原则，对于这么一个算不上特别有难度的事情，我开始了折腾之路。

## 我是怎么想的
我是这样想的，好歹也写了不少代码，不谈一谈我的心路历程，难以铺平我的技术人生。所以，这一部分是写我从一开始要做这个repo到写成所有代码的心路历程，和运行代码没有半点关系，但是我觉得对于代码注释还是有很大的帮助的。

### 万事开头难
其实这个东西，如果考虑的是从0开始，其思路还是很直观的，我相信在啥也不想，靠意识流的情况下基本就是思路一的节奏。但是随着思考的深入，动手的介入，脑子的进入，明显思路二才是最优的选择。

| 思路一 | 思路二 |
| ------ | ------ |
| 利用爬虫获取每一期码农周刊的内容，一条一条的标题和链接|利用爬虫获取每一期码农周刊的内容，一次性将所有的标题和链接存入文本文件|
| 筛选每一条链接，主要去除无效链接| 读取上述文本文件，根据配置文件中的分类关键词分类|
| 对于每条链接，从配置文件中按照规则寻找关键字分类| 一次性分类好，形成所有分好类的md文件 |
| 按照分类写入相应的md文件| 处理所有的md文件，去除失效的链接，形成最终的md文件|

为什么要采用思路二，主要有以下几点：
* 思路二中每个步骤都是相对独立的文件，每个部分完成一个简单的小功能，keep it simple，stupid
* 在这个过程中，最费时的就是探查链接是否有效，如果按照思路一的方式，基本要全部运行完才能获得最终可以git push的文件，而思路二，完全可以实现一边执行，一边获取部分完整可以git push上去的文件

### 然后后面更加难
我一直秉承着实用主义的原则，软件只是实现思想的工具，关键不是炫技而是要满足需求。那么，我已经可以从0开始获取到所有的markdown文件，那么下一个问题是怎样更新？首先，得明确在每次将要更新的时候自己有什么。
* 已经分类好的若干md文件
* 一个readme.md文件用来进行说明这玩意儿干什么

我的主要任务是当新一期出来之后更新若干md文件，这个更新当然是需要有效的，格式化好的md文本，并且用最少的力气。所以，我的思路是这样的:
* 获取最新一期的内容
* 重复上一节的过程。
* 和按照文件名和现有的md文件合并。

### 说一说所谓分类关键词文件吧
这个repo有一个核心文件，这个在下一大节会具体说明，但是一开始我面临过的问题是，怎么分类，找哪些关键词？于是我想到了分词，但是这玩意儿其实没想象的那么好用，也不能说不好用，仅仅做一个参考吧。于是我就利用了分类后的结果，最主要的是得加上我这真“人工智能”，human intelligence，大体搞出了几类的关键词。而且这个东西基本只需要执行一次，因为分分类标准并不会剧烈变化，除非我们的语言变了。所以tools里面并没有这个相关的代码，但是放心，分类配置的json文件是有的。

另外，在分类分分的过程中，我发现我分出了感情。于是，我就开始自我展(chui)望(niu)一下，我也在开始用用人工智能，这次是AI，从这将近2w个样本中高出一个合理而又高效的计算机分类。不为别的，每当我在网上买计算机书籍的时候，我发现分类并不那么的合理，也许有一天，我能做出一套“行业”标准呢？

## 我是怎么做的
具体到实现上，按照我的初步想法，我写了这么几个文件：
* GetAllTitles.py -> 这个是用来爬取码农周刊内容的，正式一点的话就叫爬虫部分吧
* ExtractMD.py -> 这个是把爬虫保存下来的内容格式化好，并且根据分类配置文件，组织形成markdown文件，也就是呈现的主要内容
* Erase404.py -> 名字起的不是特别恰当，其实我就留下了相应码是200的文件，顾名思义，剔除掉那些也许是年久失修，也许是已经被挪走的内容
* MergeFile.py -> 这个是专门为更新写的，功能简单，就是把最新一期形成的markdown文件汇总到已经分类好的大的markdown文件之中
* category.json -> 这个是传说中的汇聚了自动分词加上human intelligence结果的分类配置文件

所有文件都完成独立的，简单的，弱智的的功能，互相有依赖但是功能上完全不会影响。对于我个人，我是很喜欢这种设计哲学的，以不要把事情搞复杂了为原则。 因为代码中没有注释，所以，接下来，我来稍微具体扯一扯这些文件是怎么用的。

### GetAllTitles.py 
由于命令行神器click的加入，所以无论编写还是使用都变得更加简单。使用`python3 GetAllTitles.py --help`可以看到该脚本有三个子命令：
* new -> 获取从第一期到最新一期的所有码农周刊的内容
* update -> 指定起始期数和结束期数，获取指定期数的内容，如果起始期数未指定，则从第一期开始，如果结束期数未指定，则一直获取到最新的一期
* latest -> 获取最新一期的内容

在爬虫部分，我试过比较多的方法，为什么选用selenium这个偏向测试而不是爬虫的库？原因是我用了requests，但是码农周刊这个域名的签名有问题，使用requests的话会报错。我试了几个方法，都在解决和不能解决这问题之前徘徊，所以，索性我换了另一种框架。

其实后面解释的内容使用子命令的--help都能看到，比如`python3 GetAllTitles.py new --help`会显示如下结果：
```
Usage: GetAllTitles.py new [OPTIONS]
Options:
   --fname TEXT  The output file name for all content, default file name is allLists.txt.
   --help        Show this message and exit.
```

简单点，如果你执行python3 GetAllTitles.py new会怎样呢？理论上如果你无人值守的话，过一会你会发现在你的代码目录下有个一直在更新的allLists.txt文件，里面的内容都是这样的格式的：
> 期数：标题$url

为什么用$作为分隔符，一，这是一个对于美好事物的向往，二，更重要的是，最开始我是选用最常见的逗号，但是在实践的过程中发现，很多标题里面本身就带有逗号。导致后面的步骤分类格式化成为markdown文件出问题，所以，改成了一个很不常用的$富豪，哦不，符号。

其他两个子命令主要功能都一样，就不再赘述了。

### ExtractMD.py
这个文件流程相当清晰：
* 从爬取保存下来的文件中读取内容，找到标题
* 从category.json中读取filter和rejecter，为什么有这两个玩意儿，下一节就可以说明
* 按照类别格式化好字符串，存储成为markdown文件
* 记录下未被分到任何一类的内容，自动保存在一个名叫uncategorized1.md的文件中，人工筛选其中的文章，并且根据筛选的结果，更新category.json文件，以求在一次次的洗礼中获得更加准确，合理的分类配置文件

使用`python3 ./ExtractMD.py --help`可以看到如下帮助信息：
```
Usage: ExtractMD.py [OPTIONS]
Options:
  --fname TEXT    The raw file name for crawling file，default is allList.txt.
  --filters TEXT  Input the filers that you need, seperate by ',', if no keywords, means use all filters by default.
  --help          Show this message and exit.
```

其中的filters是你想分类的文件的关键词，比如说“c++，java，大数据”等等，这些类名可以在下一节提到的category.json中查询。如果不传这个参数，标示按照category.json文件里面的类别尽量分类。

### category.json
这个应该算这个repo的核心部件了，程序根据这个json文件里的标示来进行分类，特意节选一部分方便说明：
``` json
{
    "root":[
        {
            "keywords":"C++",
            "filters":["c++","c 语言"],
            "rejecters":[],
            "fileName":"CppLinks.md"
        },
        {
            "keywords":"Java",
            "filters":["java","jar","jvm","jdk"],
            "rejecters":["招聘","bjarne","javascript"],
            "fileName":"JavaLinks.md"
        }
    ]
}
```
主要的元素有四个，作用分别如下：
* keywords:这一个类别的名字，暂时在代码中没有直接使用，主要是给人做一个标示
* filters:只有包含这些个关键词的标题才能归为这一类
* rejecters:如果标题中包含了这类关键词，一定不归属于这一类
* fileName:最终形成的markdown文件的名字

这里面有值得解释的就是rejecters，有这个东西也是没有办法。以java举例，jar关键词是属于Java这一类的，但是偏偏大名鼎鼎的c++之父名字里面也有jar这个关键词，我又觉得精确匹配的话没那个必要，所以就使用了rejecter这么个玩意儿。

这里着重的提一句，这里的分类带有浓烈的个人喜好和自我经验的限制，非常欢迎各位对于这个分类提出补充。

对于这个json文件，我还有一些扩展的想法，统一在最后一节扯扯。

### Erase404.py
这个就是去除不可达的url的内容，因为码农周刊从第一期开始算的话，已经有6年了，那是一个二维码支付都还刚刚开始普及的年代，很多估计是年久失修了或者作者心血来潮清除了自己的黑历史。

方法很简单，就是利用requests的库去获得每一条url的response code。但是正如我在该部分第一小节说过的一样，码农周刊的域名和requests库会发生证书报错的问题。怎么办？我选取了最简单的办法，如果url里面含有码农周刊的域名，也就是toutiao.io，我就默认这个是一个可以访问的网站。使用`python3 ./Erase404.py --help`可以看到如下内容：
```
Usage: Erase404.py [OPTIONS]
Options:
   --folder TEXT  The folder that contains markdown files to be processed, default is current folder.
   --help         Show this message and exit.
```

只需要一个参数，就是含有需要处理的markdown文件的folder名称，默认就是当前文件。处理好的文件会放在当前文件夹下的新建的一个叫做filtered的文件夹下。因为这个算IO密集型的操作，所以使用多线程大大提高了其速度。

### MergeFiles.py
这个文件就及其简单了，合并两个文件夹下文件名相同的文件。使用`python3 ./MergeFiles.py --help`可以看到如下内容：
```
Usage: MergeFiles.py [OPTIONS]
Options:
  --src TEXT  Sorce folder that contains markdown files to be merged.
  --dst TEXT  Destination folder that contains existing,categorized markdown files.
  --help      Show this message and exit.
```

## 如何把他们链接起来
这里我又要做一次树莓派的强力推广人员，上面的4个文件明显是可以自动化，只有最后的git push需要更多一点的关照。而这种默默采集数据加一些处理的工作利用树莓派再合适不过了，只需要利用脚本在上linux的cron程序，可以实现这些程序定时的跑起来，省时又省电。

## 我接下来想要做什么
对于目前已经做的，我还有一些想补充的，毕竟边做边吹做起来比较有动力，包括但不仅限于：
* 为所有的python文件加上log
* 利用人工智能形成更好的json分类配置文件
* 添加重复值检测，有时候会出现重复的内容，需要提出
* 修改代码，使其能够更加自动化
* 给json文件添加一个类别项，这样可以自动生成最外层的readme.md文件
* 将GetAllTitles.py new改成多线程的，为什么现在是一个直接撸的，原因很简单，因为这个是一次性的,后面的更新用latest就行了。而且，全撸一遍只要一晚上就可以了
* 修改任何bug以及反直觉使用的地方


## 如果你想无脑跑程序，直接看这里
上面的长篇累述大部分都是我的一厢情愿，如果你想简单暴力，直接运行，只要看这里就行了。

### 从零开始的
* `python3 GetAllTitles.py new` 然后等待程序结束，在当前文件夹下，可以看到一个叫做allLists.txt的文件
* `python3 ExtractMD.py` 等待程序结束，抱歉没有表示进度的输出，在当前文件夹下，可以看到很多md文件
* `python3 Erase404.py` 等待程序结束，在一阵输出之后，会在当前文件夹下出现一个filtered的文件夹，里面就是过滤过失效连接的md文件

### 更新markdown文件
* `python3 GetAllTitles.py latest --fname somefile.txt` 然后等待程序结束，在当前文件夹下，可以看到一个叫做somefile.txt的文件
* `python3 ExtractMD.py` 等待程序结束，抱歉没有表示进度的输出，在当前文件夹下，可以看到很多md文件
* `python3 Erase404.py` 等待程序结束，在一阵输出之后，会在当前文件夹下出现一个filtered的文件夹，里面就是过滤过失效连接的md文件
* `python3 MergeFiles.py --src . --dst <MNWeeklyCategory>/docs` <MNWeeklyCategory>是已经存在的并且分类好的md文件，等待程序结束，获得更新后的结果

我是mac和linux上跑的这个程序，如果在windows上可能需要改一下GetAllTitles.py 中one_list_with_url后面的换行符。

### 结尾
如果看到这里，说明你真是对我写的这些多少还有点兴趣，如果你对我的展(chui)望(niu)也是饶有兴趣的话，我是不反对接受直接打款这种暴力形式的支持的。
![$$$](https://i.loli.net/2019/11/02/hXiOwdKT5eSFqgs.jpg)


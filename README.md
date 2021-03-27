# NBTedit
Editing NBT files in minecraft with Python

出于一些原因，我想用python来编辑minecraft的存档，用编辑nbt的方法再用mcedit导入是个很可行的方法，所以我就简单的写了一个py脚本来生成nbt文件。

文章项目地址：https://www.12skoko.com/archives/178

该文件需要NBT库的支持：https://github.com/twoolie/NBT

```pip
pip install nbt
```

直接py文件下载放在项目同目录就行，使用的时候直接import
```python
import NBTeidtpy
```

这个脚本非常简单，里面只有一个类
```python
class NBTedit:
	def __init__(self, sizes):
	def printNBT(self):
	def saveNBT(self, path):
	def addblockskind(self, block):
	def setblock(self, coor, block):
	def removeblock(self, coor):
	def setcommandblock(self, coor, command, type, name='@'):
```
###创建NBT文件
刚开始创建NBT文件的时候，需要规定好文件的大小，初始化的时候就已经把所有的方块全部填上了air方块

```python
mynbt=NBTeditpy.NBTedit([50,10,10])
```
###方块字典
接下来就是要添加我们需要的方块了
注意nbt格式添加方块是先需要添加方块种类的
也就是说nbt格式储存方块是根据坐标和的方块种类，而不是直接方块的名字

不是这样的：

| 坐标 | x=0 | x=1 | x=2 |
|:---:| :---: | :---: | :--: |
| z=0 | 草方块 | 草方块 | 圆石 |
| z=1 | 草方块 | 草方块 | 圆石 |
| z=2 | 草方块 | 空气 | 圆石 |


而是这样的：

| 坐标 | x=0 | x=1 | x=2 |        | 方块字典 |  |
|:---:| :---: | :---: | :--: |   |:---:| :---: |
| z=0 | 方块2 | 方块2 | 方块3 |    | 方块1 | 空气 |
| z=1 | 方块2 | 方块2 | 方块3 |    | 方块2 | 草方块 |
| z=2 | 方块2 | 方块1 | 方块3 |    | 方块3 | 圆石 |

所以我们要先在方块字典里面添加方块
```python
def addblockskind(block):
```

我们先来看一看方块字典里的方块需要哪些东西

这是air方块：
```nbt
TAG_Compound: {1 Entries}
{
	TAG_String('Name'): minecraft:air
}
```
这是command_block方块：
```nbt
TAG_Compound: {2 Entries}
{
	TAG_String('Name'): minecraft:command_block
	TAG_Compound('Properties'): {2 Entries}
	{
		TAG_String('conditional'): false
		TAG_String('facing'): up
	}
}
```

我们可以看出来有一个固定的tag是'name'，后面跟着方块的名字，然后有一个可选的'properties'是方块的属性

在NBTeditpy中，addblockskind函数中的block的类型为字典

```python
block_new = {'Name': 'minecraft:stone', 'tag': 'stone'}
```
如果是有'properties'属性的方块则为
```python
block_new = {'Name': 'minecraft:command_block', 'tag': 'cb',
			'Properties': {'conditional': 'flase', 'facing': 'north'}}
```
这里的tag是随便取的标识名字，为了是以后能方便的添加方块，只要自己认识随便写什么都是可以的。

注意这里面所有的变量属性都应该是字符串，'condition'的后面是'false'而不是false

把我们写好的字典传入就可以添加进nbt文件中的方块字典了

```python
mynbt.addblockskind(block_new)
```
air方块在创建对象时已经添加，tag是'air'

###添加方块

现在就可以在nbt中正式的添加方块了

```python
def setblock(coor, block)
```
coor是一个列表，用来确定这个方块放置的具体坐标，注意不要超过一开始初始化时设置的坐标大小限制
```python
coor=[2,3,5]
```
block是一个字典，只有一个必须的键值对
```python
block_set={'tag':'stone'}
```
这里的tag就是在加入方块字典里是自己取的名字

方块的nbt格式也是储存在这里的，所以有一个可选的nbt键值对
```python
cb = {'tag': 'cb', 'nbt': {'Command': 'time set 1000',
                           'Command_type': 'String',
                           'auto': 0,
                           'auto_type': 'Byte',
                           'id': 'minecraft:command_block',
                           'id_type': 'String',
                           'CustomName': '@',
                           'CustomName_type': 'String',
                           'powered': 0,
                           'powered_type': 'Byte',
                           'UpdateLastExecution': 1,
                           'UpdateLastExecution_type': 'Byte',
                           'conditionMet': 1,
                           'conditionMet_type': 'Byte',
                           'TrackOutput': 1,
                           'TrackOutput_type': 'Byte',
                           'SuccessCount': 1, 
                           'SuccessCount_type': 'Int',
                           'LastExecution': 0,
                           'LastExecution_type': 'Long'
                           }}
```
这里nbt字典里面的键值对根据需要自行添加。但需要注意的是，需要在添加的键中再添加一个'type'的键，值来表示nbt的格式

例如添加{'Command': 'time set 1000'}需要同时再加一个{'Command_type': 'String'}

目前支持的nbt格式有['String','Byte','Int','Long','Float','Double','Short']（注意大小写）

套娃的Compound格式并不支持。~~别问，问就是懒，有需求再加~~

然后就能用setblock函数添加方块了
```python
setblock(coor, cb)
```

###删除方块

这个没什么好说的，传入坐标数组就能把坐标的方块替换成air方块

```python
def removeblock(coor)
```

###保存

```python
def saveNBT(path)
```

path为保存路径名字

```python
saveNBT('mynbt.nbt')
```

###命令方块

噔噔噔，我写这个主要是因为要放置命令方块，所以写了一个函数来专门放置命令方块

```python
def setcommandblock(coor, command, type, name='@')
```

coor是坐标，command是命令，格式是string，name是命令方块的别名，是个可选参数

接下来就是type的格式了，type是一个由四个数组成的列表

众所周知命令方块有好几种（脉冲，连锁，循环），又有制约朝向啥的，所以我把它统一放在type列表里了

|  | 方块类型| |   | 制约     |  |  | 朝向|       |  |自动|
|:---:| :---: |  | :---: | :---: || :---: |:---: | | :---: | :---: |
| 0 | 脉冲 |  | 0 |  不受制约 |  | 0 | east x+|  |  0  | 红石控制 |
| 1 | 连锁 |  | 1 |  条件制约 |  | 1 | south z+| |  1  | 始终开启 |
| 2 | 循环 |  |   |          |  | 2 | west x-|  |     | |
|   |      |  |   |          |  | 3 | north z-| |     | |
|   |      |  |   |          |  | 4 | up y+|    |     | |
|   |      |  |   |          |  | 5 | down y-|  |     | |

比如我要一个始终开启不受制约朝上的连锁命令方块，则type=[1,0,4,1]

```python
setcommandblock([1,2,3], 'time set day', [1,0,4,1])
````

注意，使用setcommandblock函数时是不需要添加方块字典的，这个函数会自动把不在方块字典里的命令方块加入方块字典

###demo

```python

import NBTeditpy

stone = {'Name': 'minecraft:stone', 'tag': 'stone', 'Properties':{'variant':'stone'}}
dirt = {'Name': 'minecraft:dirt', 'tag': 'dirt'}
grass = {'Name': 'minecraft:grass', 'tag': 'grass'}
cobblestone = {'Name': 'minecraft:cobblestone', 'tag': 'cobblestone'}

nn = NBTeditpy.NBTedit([2, 2, 2])

nn.addblockskind(stone)
nn.addblockskind(dirt)
nn.addblockskind(grass)
nn.addblockskind(cobblestone)

nn.setblock([0, 0, 0], {'tag': 'stone'})
nn.setblock([0, 0, 1], {'tag': 'dirt'})
nn.setblock([0, 1, 1], {'tag': 'grass'})
nn.setblock([1, 0, 1], {'tag': 'cobblestone'})
nn.setcommandblock([1, 1, 0], 'helloworld', [0, 0, 0, 0])

nn.printNBT()

nn.saveNBT('demo.nbt')

```

















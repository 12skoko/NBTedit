from nbt import *


class NBTedit:
    def __init__(self, sizes, author='12skoko'):
        self.nnn = nbt.NBTFile()
        self.create(sizes, author)
        self.size = [sizes[0], sizes[1], sizes[2]]
        self.blocktags = {'air': 0}

        self.cbtype = [{0: 'command_block', 1: 'chain_command_block', 2: 'repeating_command_block'},
                       {0: 'false', 1: 'true'},
                       {0: 'east', 1: 'south', 2: 'west', 3: 'north', 4: 'up', 5: 'down', }
                       ]

    def create(self, sizes, author):
        self.nnn.tags.append(nbt.TAG_String(name="author", value=author))
        self.nnn.tags.append(nbt.TAG_Int(name="DataVersion", value=1))
        entities = nbt.TAG_List(name='entities', type=nbt.TAG_Byte)
        self.nnn.tags.append(entities)
        size = nbt.TAG_List(name='size', type=nbt.TAG_Int)
        size.tags.append(nbt.TAG_Int(sizes[0]))
        size.tags.append(nbt.TAG_Int(sizes[1]))
        size.tags.append(nbt.TAG_Int(sizes[2]))
        self.nnn.tags.append(size)
        palette = nbt.TAG_List(name='palette', type=nbt.TAG_Compound)
        self.nnn.tags.append(palette)
        blocks = nbt.TAG_List(name='blocks', type=nbt.TAG_Compound)
        self.nnn.tags.append(blocks)
        self.addblockskind({'Name': 'minecraft:air', 'tag': 'air'}, 1)
        for i in range(0, sizes[2]):
            for j in range(0, sizes[0]):
                for k in range(0, sizes[1]):
                    air = nbt.TAG_Compound()
                    pos = nbt.TAG_List(name='pos', type=nbt.TAG_Int)
                    pos.tags.extend([nbt.TAG_Int(j), nbt.TAG_Int(k), nbt.TAG_Int(i)])
                    air.tags.append(nbt.TAG_Int(name="state", value=0))
                    air.tags.append(pos)
                    self.nnn['blocks'].tags.append(air)

    def printNBT(self):
        print(self.nnn.pretty_tree())

    def saveNBT(self, path):
        self.nnn.write_file(path)

    def addblockskind(self, block, init=0):

        blockkind = nbt.TAG_Compound()
        blockkind.tags.append(nbt.TAG_String(name='Name', value=block['Name']))
        if 'Properties' in block:
            Properties = nbt.TAG_Compound(name='Properties')
            Properties.name = 'Properties'
            for i in block['Properties']:
                Properties.tags.append(nbt.TAG_String(name=i, value=block['Properties'][i]))
            blockkind.tags.append(Properties)
        self.nnn['palette'].tags.append(blockkind)

        if init == 0:
            self.blocktags[block['tag']] = len(self.blocktags)

    def Calcoor(self, coor):
        if coor[0] < 0 or coor[1] < 0 or coor[2] < 0 or coor[0] > self.size[0] or coor[1] > self.size[1] or coor[2] > \
                self.size[2]:
            return 0
        return coor[2] * self.size[0] * self.size[1] + coor[0] * self.size[1] + coor[1]

    def setblock(self, coor, block):
        num = self.Calcoor(coor)
        self.nnn['blocks'][num]['state'].value = self.blocktags[block['tag']]
        try:
            self.nnn['blocks'][num].tags.remove(self.nnn['blocks'][num]['nbt'])
        except:
            pass

        if 'nbt' in block:
            nbtt = nbt.TAG_Compound()
            nbtt.name = 'nbt'

            for i in block['nbt']:
                if '_type' not in i:
                    tagtype = block['nbt'][str(i) + '_type']
                    if tagtype == 'String':
                        nbtt.tags.append(nbt.TAG_String(name=i, value=block['nbt'][i]))
                    elif tagtype == 'Byte':
                        nbtt.tags.append(nbt.TAG_Byte(name=i, value=block['nbt'][i]))
                    elif tagtype == 'Int':
                        nbtt.tags.append(nbt.TAG_Int(name=i, value=block['nbt'][i]))
                    elif tagtype == 'Long':
                        nbtt.tags.append(nbt.TAG_Long(name=i, value=block['nbt'][i]))
                    elif tagtype == 'Float':
                        nbtt.tags.append(nbt.TAG_Float(name=i, value=block['nbt'][i]))
                    elif tagtype == 'Double':
                        nbtt.tags.append(nbt.TAG_Double(name=i, value=block['nbt'][i]))
                    else:
                        print(i)
                        exit(66666)

            self.nnn['blocks'][num].tags.append(nbtt)

    def removeblock(self, coor):
        num = self.Calcoor(coor)
        self.nnn['blocks'][num]['state'].value = 0
        try:
            self.nnn['blocks'][num].tags.remove(self.nnn['blocks'][num]['nbt'])
        except:
            pass

    def setcommandblock(self, coor, command, type, name='@'):
        typestr = 'cb' + str(type[0]) + str(type[1]) + str(type[2]) + str(type[3])
        if typestr not in self.blocktags:
            cbnew = {'Name': self.cbtype[0][type[0]], 'tag': typestr,
                     'Properties': {'conditional': self.cbtype[1][type[1]], 'facing': self.cbtype[2][type[2]]}}
            self.addblockskind(cbnew)
        cb = {'tag': typestr, 'nbt': {'Command': command,
                                      'Command_type': 'String',
                                      'auto': type[3],
                                      'auto_type': 'Byte',
                                      'id': 'minecraft:command_block',
                                      'id_type': 'String',
                                      'CustomName': name,
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
        self.setblock(coor, cb)

#!/usr/bin/env python3

import re
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter

INDICES = {
    1 : 'class',
    2 : 'subclass',
    3 : 'tech level',
    6 : 'prob. to appear in shop',
    7 : 'min cost',
    8 : 'max cost',
    9 : 'damage',
    10 : 'em damage',
    11 : 'recharge, ms',
    12 : 'distance',
    13 : 'speed',
    14 : 'explosion radius',
    15 : 'weapon steer, Liberator only',
    16 : '1/0 auto/manual turret',
    17 : 'turret speed',
    18 : 'shield capacity',
    19 : 'shield recharge',
    20 : 'armor durability',
    22 : 'payload shrinking effect',
    23 : '1/0 auto/manual tractor beam',
    24 : 'tractor beam lock time',
    25 : 'afterburner effect',
    26 : 'afterburner recharge',
    27 : 'afterburner duration',
    28 : 'maneuvering thruster effect',
    29 : 'scanner lock time',
    30 : '1/0 a-class asteroid detection yes/no',
    31 : '1/0 cargo scan yes/no',
    32 : 'mining laser handling',
    33 : 'mining laser yield',
    34 : 'passenger cabin capacity',
    35 : 'cloak duration',
    36 : 'cloak spin-up time',
    37 : 'hyperdrive spin-up time',
    38 : 'battery consumption',
    39 : 'weapon modifier recharge param',
    40 : 'weapon modifier damage param',
    41 : 'emergency system duration',
    42 : 'rhoda vortex duration',
    43 : 'rhoda vortex recharge',
    49 : 'plasma collector speed',
    50 : 'plasma collector radius',
    51 : 'plasma collector distance',
    52 : 'gamma-shielding effect',
    53 : 'emitter/reciever beam radius',
    54 : 'emitter/reciever beam effect',
    55 : 'emitter/reciever beam max targets',
    56 : 'ionizing rocket effect',
    57 : '1/0 gas clouds indicator yes/no',
    58 : '1/0 gas clouds on radar yes/no',
    59 : 'shields plasma consumption',
    60 : '1/0 sold by vossk only yes/no',
    61 : 'manufactured by'
    }

class Item:
    def __init__(self, values):
        self.values = {}
        self.values['preamble'] = None
        for key, value in values.items():
            self.values[key] = value

    def __str__(self):
        s = ''
        for key, value in self.values.items():
            s+= str(key)
            if key in INDICES.keys():
                s+= ' (' + str(INDICES[key]) + ')'
            s+= ' : ' + str(value) + '\n'
        return s

    def __getitem__(self, key):
        if not isinstance(key, slice) and key in self.values.keys():
            return self.values[key]
        return None

    def __setitem__(self, key, value):
        if not isinstance(key, slice):
            self.values[key] = value

    def keys(self):
        return self.values.keys()

    def to_binary(self):
        output = self.values['preamble']
        for key, value in self.values.items():
            if isinstance(key, int):
                output += int.to_bytes(key, 4, 'big') + int.to_bytes(value, 4, 'big') 
        return output
        

def parse_args():
    parser = ArgumentParser(description = 'items.bin browser and editor.\n\ncommands:\n  list - list all items\n  sel [num] - select item by ID\n  edit [num1] [num2] - change index num1 value to num2\n  output - write file\n  exit - exit', formatter_class=RawTextHelpFormatter)
    parser.add_argument('in_file', metavar='in_file_path', type=str, help = 'source items.bin file path')
    parser.add_argument('out_file', metavar='out_file_path', type=str, help = 'output items.bin file path')

    return parser.parse_args()

def parse_file(filename):
    with open(filename, 'rb') as file:
        items = []
        while True:
            offset = file.tell()
            preamble = file.read(4) #total item structure is: preamble -> repeating index (4b) + value (4b) structure

            if not preamble:
                return items

            if int.from_bytes(preamble, 'big') == 0: #preamble may be fixed-length (12b) or variable length in case of a blueprint item
                preamble += file.read(8)
            else:
                to_read = int.from_bytes(preamble, 'big')*8+8 #blueprint item preamble first number is a number of ingridients (x), total preamble length is 8*x+12 bytes
                preamble += file.read(to_read)
            id_index = file.read(4)
            id_value = file.read(4)

            id_index = int.from_bytes(id_index, 'big')
            id_value = int.from_bytes(id_value, 'big')
            
            indices = {}
            indices['offset'] = offset
            indices['preamble'] = preamble
            indices[id_index] = id_value

            max_index = -1
            
            while True:
                index = file.read(4)

                if not index: #empty byte sequence == eof
                    break
                
                if len(index) != 4 or int.from_bytes(index, 'big') <= max_index: #self-repeated index == new item
                    file.seek(file.tell() - 4)
                    break
                value = file.read(4)
                
                index = int.from_bytes(index, 'big')
                value = int.from_bytes(value, 'big')
                if index > max_index:
                    max_index = index
                indices[index] = value
            items.append(Item(indices))
            
        #return items

def output(path, item_list):
    with open(path, 'wb') as file:
        [file.write(item.to_binary()) for item in item_list]

args = parse_args()
items = parse_file(args.in_file)
#items = parse_file('/home/vladislav/Downloads/hd/items.bin')
print('Parsed', len(items), 'items')

selected_item = None

while True:
    print('\033[94m' + 'Selected item:', selected_item, '\033[0m')
    if selected_item and 0 <= selected_item < len(items):
        print('\n' + str(items[selected_item]))
    print('What to do:\n')
    command = input().lower().strip()
    sel = re.compile(r'sel (\d+)')
    edit = re.compile(r'edit (\d+) (\d+)')

    if command == 'list':
        [print(item) for item in items]
    elif sel.findall(command):
        index = int(sel.findall(command)[0])
        if 0 <= index < len(items):
            selected_item = index
            #print(str(items[selected_item]))
        else:
            print('\033[91m' + 'no such item' + '\033[0m')
            
    elif edit.findall(command):
        if not selected_item:
            print('\033[91m' + 'no item selected' + '\033[0m')
        else:
            index, value = edit.findall(command)[0]
            index, value = int(index), int(value)
            if isinstance(index, int) and index in items[selected_item].keys():
                prev_value = items[selected_item][index]
                items[selected_item][index] = value
                print('\033[92m' + 'set index', str(index), 'value from', str(prev_value), 'to', str(items[selected_item][index])+ '\033[0m')
            else:
                print('\033[91m' + 'cannot add a new index' + '\033[0m')
    elif command == 'exit':
        break
    elif command == 'output':
        print('\033[94m' + 'writing...' + '\033[0m')
        output(args.out_file, items)
    else:
        print('\033[91m' + 'cannot recognize' + '\033[0m')
    

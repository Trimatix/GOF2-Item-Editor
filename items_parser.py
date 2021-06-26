"""Galaxy on Fire 2 Items.bin browser and editor. Requires python 3.

Written by SkaterFromHell, August 2019.
https://4pda.to/forum/index.php?s=&showtopic=483666&view=findpost&p=88289467

Some item attributes identified by Wobatt, October 2017
https://steamcommunity.com/app/212010/discussions/0/882964117926225628/#c1480982338953713020

Compiled into exe with basic tkinter UI by Trimatix, June 2021.
Join the Kaamo Club discord server. Link can be found on the wiki: https://galaxyonfire.fandom.com/wiki/Galaxy_on_Fire_Wiki
Once you've joined, you can jump to the discussion thread here: https://discord.com/channels/226528541368385536/582862358888579072/858307198648188958


1) Run the script and select your existing items.bin when prompted.

2) The script now shows a command prompt. Type in your commands, with any arguments, and press enter.
     Type `list` to list all items in the items.bin and their attributes. Each item's `0` attribute is its ID.

3) To edit an item, select it with `sel [ID]`. E.g to select the item in the above screenshot, I would `sel 195`
     This command is also useful for finding the attributes of a specific item.

4) To change an attribute of your selected item, use `edit [attribute number] [new value]`. E.g to edit the tech level of item 195 in the above screenshot,
      I would use `edit 3 10`

5) To save your modified items.bin, type `output`, and enter your desired output file path. You can now `exit`, and drop your newly edited items.bin into your game's bin folder.

To see all available commands, use the `help` command.
"""

#!/usr/bin/env python3

import re
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog

USE_GUI = True
HELP_STR = 'items.bin browser and editor.\n\ncommands:\n  help - show this message\n  list - list all items\n  sel [num] - select item by ID\n  findid [item name] - find the item ID of the named item. Case insensitive, but beware of symbols\n  edit [num1] [num2] - change index num1 value to num2\n  output - write file\n  exit - exit'


if USE_GUI:
    root= tk.Tk()

    canvas1 = tk.Canvas(root, width=200, height=200)
    canvas1.pack()

    log_box_1 = ScrolledText(root)
    log_box_1.pack()
    
    command_input_box = tk.Entry(root)
    command_input_box.pack()
    submit_button = tk.Button(root, text="Send command")
    submit_button.pack()

def log(*args, **kwargs):
    txt = " ".join(str(i) for i in args)
    if kwargs:
        log(f"WARN: LOG() GIVEN KWARGS: {', '.join(kwargs)}\nBUT LOG() TAKES NO KWARGS")
    if USE_GUI:
        log_box_1.config(state=tk.NORMAL)
        log_box_1.insert(tk.END, "\n" + txt)
        log_box_1.see("end")
        log_box_1.config(state=tk.DISABLED)
    else:
        print(txt)



INDICES = {
    0 : 'item ID',
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
    16 : 'auto/manual turret',
    17 : 'turret speed',
    18 : 'shield capacity',
    19 : 'shield recharge',
    20 : 'armor durability',
    22 : 'payload shrinking effect',
    23 : 'auto/manual tractor beam',
    24 : 'tractor beam lock time',
    25 : 'afterburner effect',
    26 : 'afterburner recharge',
    27 : 'afterburner duration',
    28 : 'maneuvering thruster effect',
    29 : 'scanner lock time',
    30 : 'a-class asteroid detection',
    31 : 'cargo scan',
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
    44 : 'sell in Vossk systems only',
    49 : 'plasma collector speed',
    50 : 'plasma collector radius',
    51 : 'plasma collector distance',
    52 : 'gamma-shielding effect',
    53 : 'emitter/reciever beam radius',
    54 : 'emitter/reciever beam effect',
    55 : 'emitter/reciever beam max targets',
    56 : 'ionizing rocket effect',
    57 : 'gas clouds indicator',
    58 : 'gas clouds on radar',
    59 : 'shields plasma consumption',
    60 : 'sold by vossk only',
    61 : 'manufactured by'
    }


NAMED_INDEX_VALUES = {
    0 : {
        0x00 : "Nirai Impulse EX 1",
        0x01 : "Nirai Impulse EX 2",
        0x02 : "Nirai Charged Pulse",
        0x03 : "V'skorr",
        0x04 : "Sh'koom",
        0x05 : "Berger Focus I",
        0x06 : "Berger Focus II A1",
        0x07 : "Berger Retribution",
        0x08 : "Berger Converge IV",
        0x09 : "M6 A1 \"Wolf\"",
        0x0A : "M6 A2 \"Cougar\"",
        0x0B : "M6 A3 \"Wolverine\"",
        0x0C : "N'saan",
        0x0D : "K'booskk",
        0x0E : "Sh'gaal",
        0x0F : "H'nookk",
        0x10 : "Luna EMP Mk I",
        0x11 : "Sol EMP Mk II",
        0x12 : "Dia EMP Mk III",
        0x13 : "Gram Blaster",
        0x14 : "Ridil Blaster",
        0x15 : "Tyrfing Blaster",
        0x16 : "Micro Gun MK I",
        0x17 : "Micro Gun MKII",
        0x18 : "64MJ Railgun",
        0x19 : "128MJ Railgun",
        0x1A : "Scram Cannon",
        0x1B : "Mass Driver MD 10",
        0x1C : "Thermic o5",
        0x1D : "ReHeat o10",
        0x1E : "MaxHeat o20",
        0x1F : "G'liissk",
        0x20 : "Jet Rocket",
        0x21 : "Amour Rocket",
        0x22 : "EMP Rocket Mk I",
        0x23 : "EMP Rocket Mk II",
        0x24 : "Edo",
        0x25 : "Intelli Jet",
        0x26 : "S'koonn",
        0x27 : "Mamba EMP",
        0x28 : "Dephase EMP",
        0x29 : "EMP GL I",
        0x2A : "EMP GL II",
        0x2B : "EMP GL DX",
        0x2C : "AMR Tormentor",
        0x2D : "AMR Oppressor",
        0x2E : "AMR Extinctor",
        0x2F : "Hammerhead D1",
        0x30 : "Hammerhead D2A2",
        0x31 : "L'ksaar",
        0x32 : "Targe Shield",
        0x33 : "Riot Shield",
        0x34 : "H'Belam",
        0x35 : "Beamshield II",
        0x36 : "Fluxed Matter Shield",
        0x37 : "E2 Exoclad",
        0x38 : "E4 Ultra Lamina",
        0x39 : "E6 D-X Plating",
        0x3A : "D'iol",
        0x3B : "T'yol",
        0x3C : "AMR Saber",
        0x3D : "Neétha EMP",
        0x3E : "Ksann'k",
        0x3F : "ZMI Optistore",
        0x40 : "Autopacker 2",
        0x41 : "Ultracompact",
        0x42 : "Shrinker BT",
        0x43 : "Rhoda Blackhole",
        0x44 : "AB-1 \"Retractor\"",
        0x45 : "AB-2 \"Glue Gun\"",
        0x46 : "AB-3 \"Kingfisher\"",
        0x47 : "Linear Boost",
        0x48 : "Cyclotron Boost",
        0x49 : "Synchrotron Boost",
        0x4A : "Me'al",
        0x4B : "Ketar Repair Bot",
        0x4C : "Static Thrust",
        0x4D : "Pendular Thrust",
        0x4E : "D'ozzt Thrust",
        0x4F : "Mp'zzzm Thrust",
        0x50 : "Pulsed Plasma Thrust",
        0x51 : "Telta Quickscan",
        0x52 : "Telta Ecoscan",
        0x53 : "Hiroto Proscan",
        0x54 : "Hiroto Ultrascan",
        0x55 : "Khador Drive",
        0x56 : "IMT Extract 1.3",
        0x57 : "IMT Extract 2.7",
        0x58 : "K'yuul",
        0x59 : "IMT Extract 4.0X",
        0x5A : "Gunant's Drill",
        0x5B : "Small Cabin",
        0x5C : "Medium Cabin",
        0x5D : "Large Cabin",
        0x5E : "Sight Suppressor II",
        0x5F : "U'tool",
        0x60 : "Yin Co. Shadow Ninja",
        0x61 : "Drinking Water",
        0x62 : "Medical Supplies",
        0x63 : "Space Waste",
        0x64 : "Artifacts",
        0x65 : "Rare Animals",
        0x66 : "Rare Plants",
        0x67 : "Drugs",
        0x68 : "Luxury",
        0x69 : "Premium Food",
        0x6A : "Basic Food",
        0x6B : "Organs",
        0x6C : "Vossk Organs",
        0x6D : "Buskat",
        0x6E : "Collectible Figure",
        0x6F : "Digital Watch",
        0x70 : "Towels",
        0x71 : "Implants",
        0x72 : "Explosives",
        0x73 : "Documents",
        0x74 : "Secure Cabin/Container",
        0x75 : "Secure Cabin/Container",
        0x76 : "Electronics",
        0x77 : "Chemicals",
        0x78 : "Plastics",
        0x79 : "Nanotech",
        0x7A : "Energy Cells",
        0x7B : "Biowaste",
        0x7C : "Radioactive Goods",
        0x7D : "Mechanical Supplies",
        0x7E : "Noble Gas",
        0x7F : "Microchips",
        0x80 : "Com. Devices",
        0x81 : "Optics",
        0x82 : "Hydraulics",
        0x83 : "Alien Remains",
        0x84 : "Suteo Liqueur",
        0x85 : "Pan Whiskey",
        0x86 : "Behén Wine",
        0x87 : "V'ikka Moonshine",
        0x88 : "Eanya Tonic",
        0x89 : "S'kolptorr Rum",
        0x8A : "Wolf-Reiser Brandy",
        0x8B : "Aquila Cocktail",
        0x8C : "Buntta Apéritif",
        0x8D : "Weymire Punch",
        0x8E : "Y'mirr Schnapps",
        0x8F : "Union Draught",
        0x90 : "Oom'bak Gin",
        0x91 : "Vulpes Soup",
        0x92 : "Magnetar Juice",
        0x93 : "Mido Distillate",
        0x94 : "Prospero Flip",
        0x95 : "Nesla Brandy",
        0x96 : "Pescal Inartu Brew",
        0x97 : "Augmenta Fizz",
        0x98 : "K'ontrr Dishwater",
        0x99 : "Ni'mrrod Muck",
        0x9A : "Gold",
        0x9B : "Titanium",
        0x9C : "Iron",
        0x9D : "Orichalzine",
        0x9E : "Pyresium",
        0x9F : "Sodil",
        0xA0 : "Doxtrite",
        0xA1 : "Cesogen",
        0xA2 : "Perrius",
        0xA3 : "Hypanium",
        0xA4 : "Void Crystals",
        0xA5 : "Golden Core",
        0xA6 : "Titanium Core",
        0xA7 : "Iron Core",
        0xA8 : "Orichalzine Core",
        0xA9 : "Pyresium Core",
        0xAA : "Sodil Core",
        0xAB : "Doxtrite Core",
        0xAC : "Cesogen Core",
        0xAD : "Perrius Core",
        0xAE : "Hypanium Core",
        0xAF : "Void Essence",
        0xB0 : "Nirai .50AS",
        0xB1 : "Berger FlaK 9-9",
        0xB2 : "Icarus Heavy AS",
        0xB3 : "Liberator",
        0xB4 : "Berger AGT 20mm ",
        0xB5 : "Skuld AT XR",
        0xB6 : "HH-AT \"Archimedes\"",
        0xB7 : "Disruptor Laser",
        0xB8 : "Rhoda Vortex",
        0xB9 : "Emergency System",
        0xBA : "Nirai Overdrive",
        0xBB : "Nirai Overcharge",
        0xBC : "Ketar Repair Bot II",
        0xBD : "Signature: Terran",
        0xBE : "Signature: Vossk",
        0xBF : "Signature: Nivelian",
        0xC0 : "Signature: Midorian",
        0xC1 : "SunFire o50",
        0xC2 : "AB-4 \"Octopus\"",
        0xC3 : "Polytron Boost"
    },

    1 : {   0 : "Primary Weapon",
            1 : "Secondary Weapon",
            2 : "Turret",
            3 : "Module",
            4 : "Commodity"
        },

    2 : {   0  : "Laser",
            1  : "Blaster",
            2  : "Auto-cannon",
            3  : "Thermal Fusion",
            4  : "Rocket",
            5  : "Missile",
            6  : "EMP Bomb",
            7  : "Nuke",
            8  : "Turret",
            9  : "Shield",
            10 : "Armour",
            11 : "Mine",
            12 : "Compressor",
            13 : "Tractor Beam",
            14 : "Booster",
            15 : "Repair Bot",
            16 : "Thruster",
            17 : "Scanner",
            18 : "Khador Drive",
            19 : "Drill",
            20 : "Cabin",
            21 : "Cloak",
            22 : "Trade Goods",
            23 : "Ore",
            24 : "Core",
            25 : "Scatter Gun",
            26 : "Rhoda Vortex",
            27 : "Emergency Shield",
            28 : "Weapon Mod",
            29 : "Signature"
    },

    16 : {
            0 : "Manual",
            1 : "Auto"
    },

    17 : {
            0 : "No",
            1 : "Yes"
    },

    23 : {
            0 : "Manual",
            1 : "Auto"
    },

    30 : {
            0 : "No",
            1 : "Yes"
    },

    31 : {
            0 : "No",
            1 : "Yes"
    },

    44 : {
            0 : "No",
            1 : "Yes"
    }
}


ITEM_NAME_ID_LOOKUP = {v.lower():k for k, v in NAMED_INDEX_VALUES[0].items()}


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
            if key in NAMED_INDEX_VALUES:
                s+= ' : ' + str(value) + ' (' + NAMED_INDEX_VALUES[key].get(value, 'Unknown') + ')\n'
            else:
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
    parser = ArgumentParser(description = HELP_STR, formatter_class=RawTextHelpFormatter)
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

            if int.from_bytes(preamble, 'big') == 0: #preamble may be fixed-length (12b) or variable length in case of a bluelog item
                preamble += file.read(8)
            else:
                to_read = int.from_bytes(preamble, 'big')*8+8 #bluelog item preamble first number is a number of ingridients (x), total preamble length is 8*x+12 bytes
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

in_file_path = filedialog.askopenfilename(title='Please select your items.bin', filetypes=(("Abyss Engine Items Binary", "*.bin"),))
# args = parse_args()
items = parse_file(in_file_path)
#items = parse_file('/home/vladislav/Downloads/hd/items.bin')
log('Parsed', len(items), 'items')

selected_item = None

def getNextCommand():
    log('Selected item:', selected_item)
    if selected_item is not None and 0 <= selected_item < len(items):
        log('\n' + str(items[selected_item]))
    log('What to do:\n')


def handle_submit(event):
    global selected_item

    command = command_input_box.get()
    log(">>", command,"\n")

    sel = re.compile(r'sel (\d+)')
    findID = re.compile(r'findid (.+)')
    edit = re.compile(r'edit (\d+) (\d+)')

    command_input_box.delete(0, tk.END)

    if command == 'list':
        [log(item) for item in items]
    elif command == 'help':
        log(HELP_STR + "\n")
    elif findID.findall(command):
        itemName = findID.findall(command)[0].lower()
        if itemName == "":
            log("Please provide the name of the item to find (caps insensitive)")
        elif itemName in ITEM_NAME_ID_LOOKUP:
            log(f"Item found: ID {ITEM_NAME_ID_LOOKUP[itemName]}")
        else:
            log("Unrecognised item name, beware of symbols.")
    elif sel.findall(command):
        index = int(sel.findall(command)[0])
        if 0 <= index < len(items):
            selected_item = index
            # log(str(items[selected_item]))
        else:
            log('no such item')
            
    elif edit.findall(command):
        if not selected_item:
            log('\033[91m' + 'no item selected' + '\033[0m')
        else:
            index, value = edit.findall(command)[0]
            index, value = int(index), int(value)
            if isinstance(index, int) and index in items[selected_item].keys():
                prev_value = items[selected_item][index]
                items[selected_item][index] = value
                log('set index', str(index), 'value from', str(prev_value), 'to', str(items[selected_item][index]))
            else:
                log('cannot add a new index')
    elif command == 'exit':
        root.destroy()
    elif command == 'output':
        log('writing...')
        out_file_path = filedialog.asksaveasfilename(title='Where would you like to save your new file?', filetypes=(("Abyss Engine Items Binary", "*.bin"),))
        output(out_file_path, items)
        log('success')
    else:
        log('cannot recognize')

    getNextCommand()

submit_button.bind("<Button-1>", handle_submit)
root.bind("<Return>", handle_submit)


getNextCommand()
root.mainloop()

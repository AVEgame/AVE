import argparse
import os
import sys
import shutil
sys.path.insert(0, '..')
from core.utils import clean
from core.ave import Game

try:
    input = raw_input
except NameError:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('filepath', help="Path to the came file you would like to compile")
parser.add_argument('-o', '--output', help="Path to output directory", default='~/ave_micro_games/')
args = parser.parse_args()

if not(os.path.isfile(args.filepath)):
    print("Input file does not exist.")
    sys.exit(1)
else:
    with open(args.filepath, 'r') as f:
        game_text_list = f.readlines()

class Dummy:
    def __init__(self):
        pass

    def clear(self):
        pass

game_name = os.path.basename(args.filepath)
output = os.path.expanduser(args.output)

if not os.path.isdir(output):
    try:
        os.mkdir(output)
    except:
        print('Cannot create output directory')

output_game_dir = os.path.join(output, game_name)

if os.path.exists(output_game_dir):
    print("This will overwrite " + output_game_dir + " and all of it's contents.")
    resp = input("Continue? [Y]/n: ")
    yes = ['yes', 'y', 'ye', '']
    no = ['no', 'n']
    if len(resp) == 0:
        pass
    elif resp.lower() in no:
        print("Exiting")
        sys.exit(0)
    elif resp.lower() not in yes:
        print("You must choose yes or no")
        sys.exit(1)
    shutil.rmtree(output_game_dir)

os.mkdir(output_game_dir)
try:
    'a'
except:
    print("Could not create output directory")
    sys.exit(1)


title_text = ''
for line in game_text_list:
    line = clean(line)
    if len(line) > 0 and line[0] == "#":
        break
    elif line[:2] == "==" == line[-2:]:
        title_text += line + "\n"
    elif line[:2] == "--" == line[-2:]:
        title_text += line + "\n"
    elif line[:2] == "**" == line[-2:]:
        title_text += line + "\n"
    elif line[:2] == "~~" == line[-2:]:
        title_text += line + "\n"

rooms = {}
items = ''

count = -1

while count < len(game_text_list):
    keys = ['#', '%']
    cur_line = clean(game_text_list[count])
    if len(cur_line) > 0 and cur_line[0] == '#':
        cur_room = clean(cur_line[1:])
        cur_room_text = ''
        cur_room_text += cur_line + '\n'
        count += 1
        cur_line = clean(game_text_list[count])
        while count < len(game_text_list) and len(cur_line) > 0 and cur_line[0] not in keys:
            cur_line = clean(game_text_list[count])
            cur_room_text += cur_line + '\n'
            count += 1
        rooms[cur_room] = cur_room_text
    elif len(cur_line) > 0 and cur_line[0] == '%':
        cur_item = clean(cur_line[1:])
        items += cur_line + '\n'
        count += 1
        cur_line = clean(game_text_list[count])
        while count < len(game_text_list) and len(cur_line) > 0  and cur_line[0] not in keys:
            cur_line = clean(game_text_list[count])
            items += cur_line + '\n'
            count += 1
    else:
        count += 1

print(rooms['kitchen'])
print(items)

with open(os.path.join(output_game_dir, '__meta'), 'w') as f:
    f.write(title_text)

for key, value in rooms.iteritems():
    with open(os.path.join(output_game_dir, key), 'w') as f:
        f.write(value)

with open(os.path.join(output_game_dir, '__items'),'w') as f:
    f.write(items)

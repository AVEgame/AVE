attrs = {"+":"adds","?":"needs","?!":"unneeds","~":"rems"}

def game_to_js(txt):
    active = True
    rooms = {}
    items = {}
    preamb = True
    firstitem = True
    mode = "PREA"
    for line in [l for l in txt.split("\n") if len(l)>0] + ['#']:
        if line[:2] == "==" == line[-2:]:
            title = clean(line[2:-2])
        if line[:2] == "--" == line[-2:]:
            description = clean(line[2:-2])
        if line[:2] == "**" == line[-2:]:
            author = clean(line[2:-2])
        if line[:2] == "~~" == line[-2:]:
            if clean(line[2:-2]) == "off":
                active = False

        if line[0]=="#" or line[0] == '%':
            if not preamb and mode == "ROOM" and len(c_options) > 0:
                rooms[c_room] = (c_room, c_txt, c_options)
            if not firstitem and mode == "ITEM":
                items[c_item] = [c_texts, c_hidden]
            if line[0] == "#":
                mode = "ROOM"
                preamb = False
                while len(line) > 0 and line[0] == "#":
                    line = line[1:]
                c_room = clean(line)
                c_txt = []
                c_options = []
            elif line[0]=="%":
                mode = "ITEM"
                firstitem = False
                while len(line) > 0 and line[0] == "%":
                    line = line[1:]
                c_item = clean(line)
                c_hidden = False
                c_texts = []
        elif mode == "ITEM":
            if clean(line) == "__HIDDEN__":
                c_hidden = True
            elif clean(line) != "":
                next_item = {'name':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                text = line
                for a in attrs:
                    text = text.split(" "+a)[0]
                next_item['name'] = clean(text)
                lsp = line.split()
                for i in range(len(lsp)-1):
                    for a,b in attrs.items():
                        if lsp[i] == a:
                            next_item[b].append(lsp[i+1])
                c_texts.append(next_item)
        elif mode == "ROOM":
            if "=>" in line:
                lsp = line.split("=>")
                next_option = {'id':"",'option':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                next_option['option'] = clean(lsp[0])
                lsp = clean(lsp[1]).split()
                next_option['id'] = clean(lsp[0])
                for i in range(1,len(lsp),2):
                    for a,b in attrs.items():
                        if lsp[i] == a:
                            next_option[b].append(lsp[i+1])
                c_options.append(next_option)
            elif clean(line) != "":
                next_line = {'text':"",'needs':[],'unneeds':[],'adds':[],'rems':[]}
                text = line
                for a in attrs:
                    text = text.split(" "+a)[0]
                next_line['text'] = clean(text)
                lsp = line.split()
                for i in range(len(lsp)-1):
                    for a,b in attrs.items():
                        if lsp[i] == a:
                            next_line[b].append(lsp[i+1])
                c_txt.append(next_line)
    out = 'gameInfo={"title":"'+title+'","desc":"'+description+'","author":"'+author+'"}\n'
    out += 'rooms = {'
    my_options = []
    for key,value in rooms.items():
        opt = '"'+key+'" : Array(\n    Array('
        texts = []
        for t in value[1]:
            this_t = '\n        Array("'
            this_t += "\\\"".join(t["text"].split('"'))
            this_t += '",Array('
            this_t += 'Array('+",".join(['"'+a+'"' for a in t['adds']])+'),'
            this_t += 'Array('+",".join(['"'+a+'"' for a in t['rems']])+'),'
            this_t += 'Array('+",".join(['"'+a+'"' for a in t['needs']])+'),'
            this_t += 'Array('+",".join(['"'+a+'"' for a in t['unneeds']])+')))'
            texts.append(this_t)
        opt += ",".join(texts)
        opt += "),\n    Array("
        options = []
        for o in value[2]:
            this_o = '\n        Array("'
            this_o += o["option"]
            this_o += '","'
            this_o += o["id"]
            this_o += '",Array('
            this_o += 'Array('+",".join(['"'+a+'"' for a in o['adds']])+'),'
            this_o += 'Array('+",".join(['"'+a+'"' for a in o['rems']])+'),'
            this_o += 'Array('+",".join(['"'+a+'"' for a in o['needs']])+'),'
            this_o += 'Array('+",".join(['"'+a+'"' for a in o['unneeds']])+')))'
            options.append(this_o)
        opt += ",".join(options)
        opt += "))"
        my_options.append(opt)
    out += ",\n".join(my_options)
    out += '}\n'

    out += 'items = {'
    my_items = []
    for name,item in items.items():
        opt = '"'
        opt += name
        opt += '" : Array(Array('
        names = []
        for a in item[0]:
            n = 'Array("'
            try:
                n += a["name"]
            except IndexError:
                pass
            n += '",Array('
            n += 'Array(' + ",".join(['"'+b+'"' for b in a["adds"]]) + '),'
            n += 'Array(' + ",".join(['"'+b+'"' for b in a["rems"]]) + '),'
            n += 'Array(' + ",".join(['"'+b+'"' for b in a["needs"]]) + '),'
            n += 'Array(' + ",".join(['"'+b+'"' for b in a["unneeds"]]) + ')'
            n += "))"
            names.append(n)
        opt += ",".join(names)
        opt += '),'
        if item[1]:
            opt += "true"
        else:
            opt += "false"
        opt += ')'
        my_items.append(opt)
    out += ",".join(my_items)
    out += '}\n'
    if active:
        return out,'{"title":"'+title+'","desc":"'+description+'","author":"'+author+'"}'
    else:
        return out,None



def _clean_newlines(string):
    while "\n" in string:
        string = string.strip("\n")
    return string

def _clean(string):
    string = _clean_newlines(string)
    while len(string) > 0 and string[0] == " ":
        string = string[1:]
    while len(string) > 0 and string[-1] == " ":
        string = string[:-1]
    string = _clean_newlines(string)
    return string

def clean(string):
    string = _clean(string)
    return string

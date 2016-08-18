import json

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
    out = {'gameInfo':{'title':title,"desc": description,"author":author}}
    out["rooms"]={}
    out["items"]={}
    for key,value in rooms.items():
        out["rooms"][key] = []
        texts = []
        for t in value[1]:
            this_t = []
            this_t.append(t["text"])
            checks = []
            checks.append(t['adds'])
            checks.append(t['rems'])
            checks.append(t['needs'])
            checks.append(t['unneeds'])
            this_t.append(checks)
            texts.append(this_t)
        out["rooms"][key].append(texts)
        options = []
        for o in value[2]:
            this_o = []
            this_o.append(o["option"])
            this_o.append(o["id"])
            checks = []
            checks.append(o['adds'])
            checks.append(o['rems'])
            checks.append(o['needs'])
            checks.append(o['unneeds'])
            this_o.append(checks)
            options.append(this_o)
        out["rooms"][key].append(options)
    for name,item in items.items():
        out["items"][name] = []
        names = []
        for a in item[0]:
            this_n = []
            try:
                this_n.append(a["name"])
            except IndexError:
                pass
            checks = []
            checks.append(a["adds"])
            checks.append(a["rems"])
            checks.append(a["needs"])
            checks.append(a["unneeds"])
            this_n.append(checks)
            names.append(this_n)
        out["items"][name].append(names)
        out["items"][name].append(item[1])
    if active:
        return json.dumps(out),json.dumps({"title":title,"desc":description,"author":author})
    else:
        return json.dumps(out),None



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

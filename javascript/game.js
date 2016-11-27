menu_ls = Array()

function checkneeds(line){
    /// FINALLY make random room destinations work
    for(var j=0;j<line["needs"].length;j++){//?
        for(var i=0;i<line["needs"][j].length;i++){
            pass = false
            if(has(line["needs"][j][i])){
                pass=true;
                break;
            }
        }
        if(!pass){return false;}
    }
    for(var j=0;j<line["unneeds"].length;j++){//?!
        for(var i=0;i<line["unneeds"][j].length;i++){
            pass = false
            if(!has(line["unneeds"][j][i])){
                pass=true;
                break;
            }
        }
        if(!pass){return false;}
    }
    return true;
}

function has(thing){
    if(thing.indexOf("==")!=-1){
        tsp = thing.split("==")
        return (parse_number(tsp[0])==parse_number(tsp[1]))
    } else if(thing.indexOf(">=")!=-1){
        tsp = thing.split(">=")
        return (parse_number(tsp[0])>=parse_number(tsp[1]))
    } else if(thing.indexOf("<=")!=-1){
        tsp = thing.split("<=")
        return (parse_number(tsp[0])<=parse_number(tsp[1]))
    } else if(thing.indexOf(">")!=-1){
        tsp = thing.split(">")
        return (parse_number(tsp[0])>parse_number(tsp[1]))
    } else if(thing.indexOf("<")!=-1){
        tsp = thing.split("<")
        return (parse_number(tsp[0])<parse_number(tsp[1]))
    } else if(thing.indexOf("=")!=-1){
        tsp = thing.split("=")
        return (parse_number(tsp[0])==parse_number(tsp[1]))
    } else if(myNumberNames.indexOf(thing)!=-1){
        return (myNumbers[thing][0]>0)
    } else {
        return (myInventory.indexOf(thing)!=-1 || (thing.substring(0,1)=="!" && myInventory.indexOf(thing.substring(1))==-1));
    }
}

function parse_number(thing){
    if(myNumberNames.indexOf(thing)!=-1){
        return myNumbers[thing][0]
    }
    if(thing.indexOf("__R__")!=-1){
        if(thing=="__R__"){
            return Math.random()
        } else {
            return Math.random()*parseFloat(thing.split("__R__")[1] )
        }
    }
    return parseFloat(thing)
}

function loadRoom(id,add,sub){
    if(id.indexOf("__R__")!=-1){
        weights = Array()
        options = id.split("(")[1].split(")")[0].split(",")
        if(id.indexOf("[")!=-1){
            wsp = id.split("[")[1].split("]")[0].split(",")
        }
        for(var i=0;i<options.length;i++){
            if(id.indexOf("[")!=-1){
                if(i>0){
                    weights.push(parseFloat(wsp[i])+weights[i-1])
                } else {
                    weights.push(parseFloat(wsp[i]))
                }
            } else {
                weights.push(i+1)
            }
        }
        next = Math.random()*weights[weights.length-1]
        for(var i=0;i<options.length;i++){
            if(next < weights[i]){
                id = options[i]
                break
            }
        }
    }
    for(var i=0;i<add.length;i++){
        inventory_add(add[i])
    }
    for(var i=0;i<sub.length;i++){
        inventory_remove(sub[i]);
    }
    if(id=="__GAMEOVER__" || id=="__WINNER__"){
        menu = document.getElementById("menu").innerHTML;
        menu = menu.replace(/menuitem/g,"dummymenuitem");
        menu = menu.replace(/onclick=[^>]*>/g,">");
        document.getElementById("menu").innerHTML = menu
    }
    if(id=="__GAMEOVER__"){
        document.getElementById("gameendtext").innerHTML="GAME OVER";
        document.getElementById("gameend").style.display="block";
        return;
    }
    if(id=="__WINNER__"){
        document.getElementById("gameendtext").innerHTML="You Win!";
        document.getElementById("gameend").style.display="block";
        return;
    }
    details = getRoom(id);

    document.getElementById("roominfo").innerHTML=details[0];

    menu_ls = details[1]
    showMenu(0)
    inv = getInventory();
    inventory = "INVENTORY"
    for(var i=0;i<inv.length;i++){
        inventory += "<br />"+inv[i]
    }
    document.getElementById("inventory").innerHTML=inventory;

}

function showMenu(st){
    menuItems="";
    shown = 0
    if(st>0){
        menuItems+="<div class='menuitem' onClick='showMenu(";
            if(st<=5){menuItems+=0} else {menuItems+=(st-4)}
            menuItems+=")'>^";
        for(var i=0;i<5;i++){menuItems+="&nbsp;&nbsp;&nbsp;&nbsp;^";}
        menuItems+="</div>";
        shown++
    }
    for(var i=st;i<menu_ls.length;i++){
        if(shown>=6 && i+1<menu_ls.length){
            menuItems+="<div class='menuitem' onClick='showMenu(";
            if(st==0){menuItems+=(st+5)} else {menuItems+=(st+4)}
            menuItems+=")'>v";
            for(var i=0;i<5;i++){menuItems+="&nbsp;&nbsp;&nbsp;&nbsp;v";}
            menuItems+="</div>";
            break
        } else {
            addstr = "Array("
            for(var j=0;j<menu_ls[i]["adds"].length;j++){
                addstr +='"'+menu_ls[i]["adds"][j]+'"'
                if(j<menu_ls[i]["adds"].length-1){addstr+=",";}
            }
                addstr +=")"
            substr = "Array("
            for(var j=0;j<menu_ls[i]["rems"].length;j++){
                substr +='"'+menu_ls[i]["rems"][j]+'"'
                if(j<menu_ls[i]["rems"].length-1){substr+=",";}
            }
            substr +=")"
            menuItems+="<div class='menuitem' onClick='loadRoom(\""+menu_ls[i]["id"]+"\","+addstr+","+substr+")'>"+menu_ls[i]["option"]+"</div>";
            shown++
        }
    }
    document.getElementById("menu").innerHTML=menuItems;
}

function inventory_add(item){
    if(item.indexOf("=")!=-1 && myNumberNames.indexOf(item.split("=")[0])!=-1){
        myNumbers[item.split("=")[0]][0] = parse_number(item.split("=")[1])
    } else if(item.indexOf("+")!=-1 && myNumberNames.indexOf(item.split("+")[0])!=-1){
        myNumbers[item.split("+")[0]][0] += parse_number(item.split("+")[1])
    } else if(item.indexOf("-")!=-1 && myNumberNames.indexOf(item.split("-")[0])!=-1){
        myNumbers[item.split("-")[0]][0] -= parse_number(item.split("-")[1])
    } else if(myNumberNames.indexOf(item)!=-1){
        myNumbers[item.split("-")[0]][0] ++
    } else {
        myInventory.push(item)
    }
}
function inventory_remove(item){
    if(myNumberNames.indexOf(item)!=-1){
        myNumbers[item][0] --
    } else {
        index=myInventory.indexOf(item);
        if(index!=-1){
            myInventory.splice(index,1);
        }
    }
}

function getRoom(id){
    roomtext=""
    for(var i=0;i<rooms[id][1].length;i++){
        line=rooms[id][1][i]
        if(checkneeds(line)){
            for(var j=0;j<line["adds"].length;j++){//+
                inventory_add(line["adds"][j]);
            }
            for(var j=0;j<line["rems"].length;j++){//~
                inventory_remove(item)
            }
        roomtext += line["text"] + " "
        }
    }

    options=Array();
    for(var i=0;i<rooms[id][2].length;i++){
        line=rooms[id][2][i]
        if(checkneeds(line)){
            options.push(line)
        }
    }
    roomtext = text_parse(roomtext)
    return Array(roomtext,options)
}
function text_parse(txt){
    out = ""
    while(txt!=""){
        tsp = txt.split("<|",1)
        out += parse_part(tsp[0])
        if(tsp.length==1){
            txt = ""
        } else {
            tsp = tsp[1].split("|>",1)
            tsp[0] = tsp[0].replace(/</g,"&lt;");
            tsp[0] = tsp[0].replace(/>/g,"&gt;");
            out += tsp[0]
            if(tsp.length==1){
                txt = ""
            } else {
                txt = tsp[1]
            }
        }
    }
    return out
}

function parse_part(txt){
    txt = txt.replace(/</g,"&lt;");
    txt = txt.replace(/>/g,"&gt;");
    txt = txt.replace(/&lt;newline&gt;/g,"<br />");
    txt = txt.replace(/\[([^\]]+)\]\(([^\)]+)\)/,"<a href='$2'>$1</a>")
    for(var i=0;i<myNumberNames.length;i++){
        txt = txt.replace("$"+myNumberNames[i]+"$",myNumbers[myNumberNames[i]][0])
    }
    return txt
}

function getInventory(){
    var inve = Array()
    for(var i=0;i<myNumberNames.length;i++){
        if(myNumbers[myNumberNames[i]][2]){
            the_name = ""
            item = myNumbers[myNumberNames[i]][1]
            for(var j=0;j<item.length;j++){
                if(checkneeds(item[j])){
                    the_name=item[j]["name"]
                }
            }
            inve.push(the_name + ": "+ myNumbers[myNumberNames[i]][0])
        }
    }
    for(var i=0;i<myInventory.length;i++){
        if((myInventory[i] in items) && (!items[myInventory[i]][1])){
            item = items[myInventory[i]]
            for(var j=0;j<item[0].length;j++){
                if(checkneeds(item[0][j])){
                    inve.push(item[0][j]["name"])
                }
            }
        }
    }
    return inve
}

function gameRestart(){
    myInventory=Array("__WEB__");
    myNumbers=Array();
    myNumberNames=Array();
    for(item in items){
        if(items[item][2]){
            myNumberNames.push(item)
            myNumbers[item] = Array(parseFloat(items[item][3]),items[item][0],items[item][1])
        }
    }
    loadRoom("start",Array(),Array());
    document.getElementById("gameend").style.display="none";
}

function gameerror(){
    document.getElementById("error").style.display="block"
}

function gameList(){
    window.location.href = '/play';
}

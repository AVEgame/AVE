menu_ls = Array()

function loadRoom(id,add,sub){
    for(var i=0;i<add.length;i++){
        myInventory.push(add[i])
    }
    for(var i=0;i<sub.length;i++){
        index=myInventory.indexOf(sub[i]);
        if(index!=-1){myInventory.splice(index,1)}
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
    details[0] = details[0].replace("<","&lt;");
    details[0] = details[0].replace(">","&gt;");
    details[0] = details[0].replace("<newline>","<br />");
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

function getRoom(id){
    roomtext=""
    for(var i=0;i<rooms[id][1].length;i++){
        line=rooms[id][1][i]
        pass=true;
        for(var j=0;j<line["needs"].length;j++){//?
            if(myInventory.indexOf(line["needs"][j])==-1){
                pass=false;
            }
        }
        for(var j=0;j<line["unneeds"].length;j++){//?!
            if(myInventory.indexOf(line["unneeds"][j])!=-1){
                pass=false;
            }
        }
        if(pass){
            for(var j=0;j<line["adds"].length;j++){//+
                myInventory.push(line["adds"][j]);
            }
            for(var j=0;j<line["rems"].length;j++){//~
                index=myInventory.indexOf(line["rems"][j]);
                if(index!=-1){
                    myInventory.splice(index,1);
                }
            }
        roomtext += line["text"] + " "
        }
    }

    options=Array();
    for(var i=0;i<rooms[id][2].length;i++){
        line=rooms[id][2][i]
        pass=true;
        for(var j=0;j<line["needs"].length;j++){//?
            if(myInventory.indexOf(line["needs"][j])==-1){
                pass=false;
            }
        }
        for(var j=0;j<line["unneeds"].length;j++){//?!
            if(myInventory.indexOf(line["unneeds"][j])!=-1){
                pass=false;
            }
        }
        if(pass){
            options.push(line)
        }
    }
    return Array(roomtext,options)
}

function getInventory(){
    var inve = Array()
    for(var i=0;i<myInventory.length;i++){
        if((myInventory[i] in items) && (!items[myInventory[i]][1])){
            item = items[myInventory[i]]
            for(var j=0;j<item[0].length;j++){
                pass=true;
                for(var k=0;k<item[0][j]["needs"].length;k++){//?
                    if(myInventory.indexOf(item[0][j]["needs"][k])==-1){
                        pass=false;
                    }
                }
                for(var k=0;k<item[0][j]["unneeds"].length;k++){//?
                    if(myInventory.indexOf(item[0][j]["unneeds"][k])!=-1){
                        pass=false;
                    }
                }
                if(pass){
                    inve.push(item[0][j]["name"])
                }
            }
        }
    }
    return inve
}

function gameRestart(){
    myInventory=Array();
    loadRoom("start",Array(),Array());
    document.getElementById("gameend").style.display="none";
}

function gameerror(){
    document.getElementById("error").style.display="block"
}

function gameList(){
    window.location.href = '/play';
}

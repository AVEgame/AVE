
function loadRoom(id,add=Array(),sub=Array()){
    for(var i=0;i<add.length;i++){
        myInventory.push(add[i])
    }
    for(var i=0;i<sub.length;i++){
        index=myInventory.indexOf(sub[i]);
        if(index!=-1){myInventory=myInventory.splice(index,i)}
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
    menuItems="";
    for(var i=0;i<details[1].length;i++){
        addstr = "Array("
        for(var j=0;j<details[1][i][2].length;j++){
            addstr +='"'+details[1][i][2]+'"'
            if(j<details[1][i][2].length-1){addstr+=",";}
        }
        addstr +=")"
        substr = "Array("
        for(var j=0;j<details[1][i][3].length;j++){
            substr +='"'+details[1][i][3]+'"'
            if(j<details[1][i][3].length-1){substr+=",";}
        }
        substr +=")"
        menuItems+="<div class='menuitem' onClick='loadRoom(\""+details[1][i][1]+"\","+addstr+","+substr+")'>"+details[1][i][0]+"</div>";
    }
    document.getElementById("menu").innerHTML=menuItems;
    inv = getInventory();
    inventory = "INVENTORY"
    for(var i=0;i<inv.length;i++){
        inventory += "<br />"+inv[i]
    }
    document.getElementById("inventory").innerHTML=inventory;

}

function getRoom(id){
    roomtext=""
    for(var i=0;i<rooms[id][0].length;i++){
        line=rooms[id][0][i]
        pass=true;
        for(var j=0;j<line[1][2].length;j++){//?
            if(myInventory.indexOf(line[1][2][j])==-1){
                pass=false;
            }
        }
        for(var j=0;j<line[1][3].length;j++){//?!
            if(myInventory.indexOf(line[1][3][j])!=-1){
                pass=false;
            }
        }
        if(pass){
            for(var j=0;j<line[1][0].length;j++){//+
                myInventory.push(line[1][0][j]);
            }
            for(var j=0;j<line[1][1].length;j++){//~
                index=myInventory.indexOf(line[1][1][j]);
                if(index!=-1){
                    myInventory=myInventory.splice(index,-1);
                }
            }
        roomtext += line[0] + " "
        }
    }

    options=Array();
    for(var i=0;i<rooms[id][1].length;i++){
        line=rooms[id][1][i]
        pass=true;
        for(var j=0;j<line[2][2].length;j++){//?
            if(myInventory.indexOf(line[2][2][j])==-1){
                pass=false;
            }
        }
        for(var j=0;j<line[2][3].length;j++){//?!
            if(myInventory.indexOf(line[2][3][j])!=-1){
                pass=false;
            }
        }
        if(pass){
            options.push(Array(line[0],line[1],line[2][0],line[2][1]))
        }
    }
    return Array(roomtext,options)
}

function getInventory(){
    var inve = Array()
    for(var i=0;i<myInventory.length;i++){
        if(!items[myInventory[i]][1]){
            item = items[myInventory[i]]
            for(var j=0;j<item[0].length;j++){
                pass=true;
                for(var k=0;k<item[0][j][1][2].length;k++){//?
                    if(myInventory.indexOf(item[0][j][1][2][k])==-1){
                        pass=false;
                    }
                }
                for(var k=0;k<item[0][j][1][3].length;k++){//?
                    if(myInventory.indexOf(item[0][j][1][3][k])!=-1){
                        pass=false;
                    }
                }
                if(pass){
                    inve.push(item[0][j][0])
                }
            }
        }
    }
    return inve
}

function gameRestart(){
    myInventory=Array();
    loadRoom("start");
    document.getElementById("gameend").style.display="none";
}

function gameList(){
    window.location.href = '/play';
}

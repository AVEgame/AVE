function showMainTitle(){
    out = typeset(titleFromAVE())
    out += seperator()
    out += "<div id='menu'>"
    count = 0
    for(var game in gameList){
        count++
        out += "<div class='menuitem' onclick=\"showGameTitle('"+game+"')\">"+gameList[game]["title"]+"</div>"
    }

    document.getElementById("maingameselect").style.height = Math.max(250+20.4*count,400)

    if(!user){out += "<div class='menuitem' onclick=\"window.location='/play/user'\">- show all games -</div>"}
    else{out += "<div class='menuitem' onclick=\"window.location='/play'\">- show only default games -</div>"}
    out += "<div class='menuitem' onclick=\"showCredits()\">- credits -</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function showCredits(){
    out = typeset(creditsFromAVE())
    out += seperator()
    out += "<div id='menu'>"
    out += "<div class='menuitem' onclick=\"showMainTitle()\">Back to main menu</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function showGameTitle(id){
    out = "<div style='text-align:center'>"+gameList[id]["title"]+"</div>"
    out += seperator()
    out += "<div style='text-align:center'>By "+gameList[id]["author"]+"</div>"
    out += seperator()
    if(!gameList[id]["desc"]){}else{
    out += "<div style='text-align:center'>"
        out += gameList[id]["desc"]
    out += "</div>"
    out += seperator()
    }
    out += "<div id='menu'>"
    out += "<div class='menuitem' onclick='loadGame(\""+id+"\")'>Play game</div>"
    out += "<div class='menuitem' onclick='showMainTitle()'>Back to main menu</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function loadGame(id){
    window.location.href = '/play/'+id;
}

function seperator(){
    out = "<div style='text-align:center'>&nbsp;"
    for(var i=0;i<14;i++){
        out += "<span style='color:#cc0000'>~</span>&nbsp;<span style='color:#4d9906'>~</span>&nbsp;<span style='color:#32619e'>~</span>&nbsp;"
    }
    out += "</div>"
    return out;
}

function typeset(txt){
    txt = txt.replace(/ /g,"&nbsp;")
    txt = txt.replace(/%v%/g,version())
    txt = txt.replace(/=/g,"<span style='background-color:#32619e'>&nbsp;</span>")
    txt = txt.replace(/@/g,"<span style='background-color:#cc0000'>&nbsp;</span>")
    txt = txt.replace(/\^/g,"<span style='background-color:#4d9906'>&nbsp;</span>")
    txt = txt.replace(/AVE/g,"<span style='color:#cc0000'>A</span><span style='color:#4d9906'>V</span><span style='color:#32619e'>E</span>")
    split = txt.split("\n")
    txt = ""
    for(var i=0;i<split.length;i++){
        if(split[i].substring(0,2)=="<>"){
            txt += "<div style='text-align:center'>"
            txt += split[i].substring(2)
            txt += "</div>"
        } else if(split[i].substring(0,2)=="<-"){
            txt += "<div style='text-align:right'>"
            txt += split[i].substring(2)
            txt += "</div>"
        } else {
            txt += "<div>"
            txt += split[i]
            txt += "</div>"
        }
    }
    return txt
}

function showMainTitle(){
    out = typeset(titleFromAVE())
    out += seperator()
    out += "<div class='menu'>"
    for(var game in gameList){
        out += "<div class='menuitem' onclick=\"showGameTitle('"+game+"')\">"+gameList[game]["title"]+"</div>"
    }
    out += "<div class='menuitem' onclick=\"showCredits()\">- credits -</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function showCredits(){
    out = typeset(creditsFromAVE())
    out += seperator()
    out += "<div class='menu'>"
    out += "<div class='menuitem' onclick=\"showMainTitle()\">Back to main menu</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function showGameTitle(id){
    out = "<div style='text-align:center'>"+gameList[id]["title"]+"</div>"
    out += seperator()
    out += "<div style='text-align:center'>By "+gameList[id]["author"]+"</div>"
    out += seperator()
    out += "<div style='text-align:center'>"+gameList[id]["desc"]+"</div>"
    out += seperator()
    out += "<div class='menu'>"
    out += "<div class='menuitem' onclick='loadGame(\""+id+"\")'>Play game</div>"
    out += "<div class='menuitem' onclick='showMainTitle()'>Back to main menu</div>"
    out += "</div>"
    document.getElementById("main").innerHTML = out
}

function loadGame(id){
    window.location.href = '/play/'+id+'.ave';
}

function seperator(){
    out = "<div style='text-align:center'>&nbsp;"
    for(var i=0;i<14;i++){
        out += "<span style='color:red'>~</span>&nbsp;<span style='color:green'>~</span>&nbsp;<span style='color:blue'>~</span>&nbsp;"
    }
    out += "</div>"
    return out;
}

function typeset(txt){
    txt = txt.replace(/ /g,"&nbsp;")
    txt = txt.replace(/\n/g,"<br />")
    txt = txt.replace(/%v%/g,version())
    txt = txt.replace(/=/g,"<span style='background-color:blue'>&nbsp;</span>")
    txt = txt.replace(/@/g,"<span style='background-color:red'>&nbsp;</span>")
    txt = txt.replace(/\^/g,"<span style='background-color:green'>&nbsp;</span>")
    return txt
}

<?php
include("../intro.php");
echo("<script type='text/javascript' src='/ave/fromave.js?time=".date("U")."'></script>");
echo("<script type='text/javascript' src='/ave/gameselect.js?time=".date("U")."'></script>");
?>
<div class='gameselect' id='maingameselect'>
<div style='width:100%;text-align:center;margin-bottom:3px'>
<?php
for($i=0;$i<21;$i++){
    echo("<span style='color:red'>A</span><span style='color:green'>V</span><span style='color:blue'>E</span>&nbsp;");
}
?>
</div>
<div id='main'></div>
</div>

<?php
echo("
<script type='text/javascript'>
");
if(isset($_GET['user'])){echo("user=true");} else {echo("user=false");}
echo("
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType('application/json');
    xobj.open('GET', '/gamelist.json?time=".date("U")."', true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == '200') {
            json_data = JSON.parse(xobj.responseText);
            if(user){
                gameList = json_data
                for(var key in gameList){
                    if(key.substring(0,5)!='user/' && json_data[key]['active']){
                        gameList[key]['title'] = '&#9733; ' + gameList[key]['title']
                    }
                }
            } else {
                gameList = Array()
                for(var key in json_data){
                    if(key.substring(0,5)!='user/' && json_data[key]['active']){
                        gameList[key] = json_data[key]
                    }
                }
            }
            showMainTitle()
          }
    };
    xobj.send(null);
</script>
");

include("../outro.php");
?>

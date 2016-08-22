<?php
include("../intro.php");

echo("<script type='text/javascript' src='/ave/game.js?time=".date("U")."'></script>");
?>
<div class='game'>
<div style='width:100%;text-align:right;margin-bottom:3px'><span style='color:red'>A</span><span style='color:green'>V</span><span style='color:blue'>E</span></div>
<div id='gameend'>
<div id='gameendtext'>GAME OVER</div>
<div class='menuitem' onclick='gameRestart()'>Play again</div>
<div class='menuitem' onclick='gameList()'>Play a different game</div>
</div>
<div id='roominfo'></div>
<div id='inventory'></div>
<div id='menu'>
</div>
</div>
<?php
echo("
<script type='text/javascript'>
//var rooms = ''
//var items = ''
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType('application/json');
    xobj.open('GET', '/download/"); if(isset($_GET['user'])){echo("user/");} echo($_GET['title'].".json?time=".date("U")."', true); // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == '200') {
            json_data = JSON.parse(xobj.responseText);
            rooms = json_data['rooms']
            items = json_data['items']
            gameRestart();
          }
    };
    xobj.send(null); 
</script>
");

include("../outro.php");
?>

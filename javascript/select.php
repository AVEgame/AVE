<?php
include("../intro.php");
?>
<script type='text/javascript' src='gamelist.js'></script>
<script type='text/javascript' src='fromave.js'></script>
<script type='text/javascript' src='gameselect.js'></script>
<div class='game'>
<div style='width:100%;text-align:right;margin-bottom:3px'>
<?php
for($i=0;$i<21;$i++){
    echo("<span style='color:red'>A</span><span style='color:green'>V</span><span style='color:blue'>E</span>&nbsp;");
}
?>
</div>
<div id='main'></div>
</div>
<script type='text/javascript'>
showMainTitle()
</script>
<?php
include("../outro.php");
?>

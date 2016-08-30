<?php
if(isset($_GET['game'])){$game=$_GET['game'];}

$attrs = Array("+"=>"adds","?"=>"needs","?!"=>"unneeds","~"=>"rems");

function _clean_newlines($string){
    return str_replace("\n","",$string);
}

function _clean($string){
    $string = _clean_newlines($string);
    while(strlen($string) > 0 && substr($string,0,1) == " "){
        $string = substr($string,1);
    }
    while(strlen($string) > 0 && substr($string,-1,1) == " "){
        $string = substr($string,0,-1);
    }
    return $string;
}

function clean($string){
    $string = _clean($string);
    return $string;
}

$items = "";

$mode = "PREA";

if(isset($_GET['user'])){
$file = str_replace("avetoitems.php","../usergames/".$game.".ave",__FILE__);
} else {
$file = str_replace("avetoitems.php","games/".$game.".ave",__FILE__);
}
if(file_exists($file)){
$txt=file_get_contents($file);
$txt=explode("\n",$txt);
$txt[] = "#";
foreach($txt as $line){if(strlen($line)>0){
    if(substr($line,0,1) == "#"){$mode = "ROOM";}
    if(substr($line,0,1)=="%"){$mode = "ITEM";}
    if($mode == "ITEM"){
        $items.=$line."\n";
    }
}}

echo $items;
}

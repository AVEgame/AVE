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

function parse_req($line){
    global $attrs;
    while(preg_match("/(\([^\)]*) ([^\)]*\))/",$line)){
        $line = preg_replace("/(\([^\)]*) ([^\)]*\))/","$1,$2",$line);
    }
    $lsp = explode($line," ");
    $reqs = Array();
    foreach($attrs as $b=>$a){
        $reqs[$a] = Array();
    }
    for($i=0;$i<count($lsp)-1;$i++){
        foreach($attrs as $a=>$b){
            if($lsp[$i] == $a){
                if($a == "?" || $a == "?!"){
                    $lsp[$i+1] = str_replace("(","",$lsp[$i+1]);
                    $lsp[$i+1] = str_replace(")","",$lsp[$i+1]);
                    $reqs[$b][] = explode(",",$lsp[$i+1]);
                } else {
                    $reqs[$b][] = $lsp[i+1];
                }
            }
        }
    }
    return $reqs;
}

$rooms = Array();
$items = Array();
$preamb = true;
$firstitem = true;
$mode = "PREA";

if(isset($_GET['user'])){
$file = str_replace("avetojs.php","../usergames/".$game.".ave",__FILE__);
} else {
$file = str_replace("avetojs.php","games/".$game.".ave",__FILE__);
}
if(file_exists($file)){
$txt=file_get_contents($file);
$txt=explode("\n",$txt);
$txt[] = "#";
foreach($txt as $line){if(strlen($line)>0){
    if(substr($line,0,2) == "==" && substr($line,-2) == "=="){
        $title = clean(substr($line,2,-2));
    }
    if(substr($line,0,2) == "--" && substr($line,-2) == "--"){
        $description = clean(substr($line,2,-2));
    }
    if(substr($line,0,2) == "**" && substr($line,-2) == "**"){
        $author = clean(substr($line,2,-2));
    }

    if(substr($line,0,1)=="#" || substr($line,0,1) == "%"){
        if(!$preamb && $mode == "ROOM" && count($c_options) > 0){
            $rooms[$c_room] = Array($c_room, $c_txt, $c_options);
        }
        if(!$firstitem && $mode == "ITEM"){
            $items[$c_item] = Array($c_texts, $c_hidden);
        }
        if(substr($line,0,1) == "#"){
            $mode = "ROOM";
            $preamb = false;
            while(strlen($line) > 0 && substr($line,0,1) == "#"){
                $line = substr($line,1);
            }
            $c_room = clean($line);
            $c_txt = Array();
            $c_options = Array();
        } else if(substr($line,0,1)=="%"){
            $mode = "ITEM";
            $firstitem = false;
            while(strlen($line) > 0 && substr($line,0,1) == "%"){
                $line = substr($line,1);
            }
            $c_item = clean($line);
            $c_hidden = false;
            $c_texts = Array();
        }
    } else if($mode == "ITEM"){
        if(clean($line) == "__HIDDEN__"){
            $c_hidden = true;
        } else if(clean($line) != ""){
            $next_item = parse_req(clean($line));
            $text = $line;
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_item["name"] = clean($text);
            $c_texts[] = $next_item;
        }
    } else if($mode == "ROOM"){
        if(strpos($line,"=>")!==false){
            $lsp = explode("=>",$line);
            $next_option = parse_req(clean($line));
            $next_option["option"] = clean($lsp[0]);
            $lsp = explode(" ",clean($lsp[1]));
            $next_option["id"] = clean($lsp[0]);
            $c_options[] = $next_option;
        } else if(clean($line) != ""){
            $next_line = parse_req(clean($line));
            $text = $line;
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_line["text"] = clean($text);
            $c_txt[] = $next_line;
        }
    }
}}

$out = Array(
    "rooms" => $rooms,
    "items" => $items,
    "loaded" => true
);

} else {
$out = Array(
    "rooms" => Array(),
    "items" => Array(),
    "loaded" => false
);

}
echo json_encode($out);

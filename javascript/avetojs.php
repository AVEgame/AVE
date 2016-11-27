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

function do_comments($text){
    $comments = Array();
    while(strpos($text,"<|")!==false){
        $lsp = explode($text,"<|",1);
        $lsp[1] = explode($lsp[1],"|>",1);
        $text = $lsp[0]."<<".count($comments).">>".$lsp[1][1];
        $comments[] = $lsp[1][0];
    }
    return Array($text,$comments);
}

function undo_comments($text,$comments){
    foreach($comments as $i=>$j){
        $text = str_replace("<<".$i.">>",$j,$text);
    }
    return $text;
}

function parse_req($line){
    global $attrs;
    $doc = do_comments($line);
    $line = $doc[0];
    $comments = $doc[1];
    while(preg_match("/(\([^\)]*) ([^\)]*\))/",$line)){
        $line = preg_replace("/(\([^\)]*) ([^\)]*\))/","$1,$2",$line);
    }
    while(preg_match("/ +((>|<|=)=?) +/",$line)){
        $line = preg_replace("/ +((=|>|<)=?) +/","$1",$line);
    }
    $lsp = explode(" ",$line);
    $reqs = Array();
    foreach($attrs as $b=>$a){
        $reqs[$a] = Array();
    }
    for($i=0;$i<count($lsp)-1;$i++){
        foreach($attrs as $a=>$b){
            if($lsp[$i] == $a){
                if($a == "?" || $a == "?!"){
                    $lsp[$i+1] = str_replace("(","",undo_comments($lsp[$i+1],$comments));
                    $lsp[$i+1] = str_replace(")","",undo_comments($lsp[$i+1],$comments));
                    $reqs[$b][] = explode(",",undo_comments($lsp[$i+1],$comments));
                } else {
                    $reqs[$b][] = undo_comments($lsp[$i+1],$comments);
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
            $items[$c_item] = Array($c_texts, $c_hidden, $c_number, $c_default);
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
            $c_number = false;
            $c_default = 0;
            $c_texts = Array();
        }
    } else if($mode == "ITEM"){
        if(clean($line) == "__HIDDEN__"){
            $c_hidden = true;
        } else if(substr(clean($line),0,10) == "__NUMBER__"){
            $c_number = true;
            $sp = explode(" ",clean($line));
            if(count($sp)>1){
                $c_default = $sp[1]/1;
            }
        } else if(clean($line) != ""){
            $next_item = parse_req(clean($line));
            $doc = do_comments($line);
            $text = $doc[0];
            $comments = $doc[1];
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_item["name"] = clean(undo_comments($text,$comments));
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
            $doc = do_comments($line);
            $text = $doc[0];
            $comments = $doc[1];
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_line["text"] = clean(undo_comments($text,$comments));
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

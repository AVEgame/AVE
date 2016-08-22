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
$rooms = Array();
$items = Array();
$preamb = true;
$firstitem = true;
$mode = "PREA";

if(isset($_GET['user'])){
$txt=file_get_contents(str_replace("avetojs.php","../usergames/".$game.".ave",__FILE__));
} else {
$txt=file_get_contents(str_replace("avetojs.php","games/".$game.".ave",__FILE__));
}
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
            $next_item = Array("name"=>"","needs"=>[],"unneeds"=>[],"adds"=>[],"rems"=>[]);
            $text = $line;
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_item["name"] = clean($text);
            $lsp = explode(" ",$line);
            for($i=0;$i<count($lsp)-1;$i++){
                foreach($attrs as $a=>$b){
                    if($lsp[$i] == $a){
                        $next_item[$b][] = $lsp[$i+1];
                    }
                }
            }
            $c_texts[] = $next_item;
        }
    } else if($mode == "ROOM"){
        if(strpos($line,"=>")!==false){
            $lsp = explode("=>",$line);
            $next_option = Array("id"=>"","option"=>"","needs"=>Array(),"unneeds"=>Array(),"adds"=>Array(),"rems"=>Array());
            $next_option["option"] = clean($lsp[0]);
            $lsp = explode(" ",clean($lsp[1]));
            $next_option["id"] = clean($lsp[0]);
            for($i=1;$i<count($lsp);$i+=2){
                foreach($attrs as $a=>$b){
                    if($lsp[$i] == $a){
                        $next_option[$b][] = $lsp[$i+1];
                    }
                }
            }
            $c_options[] = $next_option;
        } else if(clean($line) != ""){
            $next_line = Array("text"=>"","needs"=>Array(),"unneeds"=>Array(),"adds"=>Array(),"rems"=>Array());
            $text = $line;
            foreach($attrs as $a=>$b){
                $text = explode(" ".$a,$text);
                $text = $text[0];
            }
            $next_line["text"] = clean($text);
            $lsp = explode(" ",$line);
            for($i=0;$i<count($lsp)-1;$i++){
                foreach($attrs as $a=>$b){
                    if($lsp[$i] == $a){
                        $next_line[$b][] = $lsp[$i+1];
                    }
                }
            }
            $c_txt[] = $next_line;
        }
    }
}}

$out = Array(
    "rooms" => $rooms,
    "items" => $items
);

echo json_encode($out);

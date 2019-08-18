<?php
$self="index.php";
$base_dir=dirname(__FILE__)."/image";
$unknown="moto";
$dirs=array("アサガオ"=>"asa","ヒルガオ"=>"hiru","そのほか"=>"other");
$m=isset($_GET["m"])?$_GET["m"] : "";
if($m=="mv"){
	$target=$_GET["target"];
	$to=$_GET["to"];
	$path=$base_dir."/$unknown/$target";
	$path_to="$base_dir/$to/$target";
	copy($path,$path_to);
	if(file_exists($path_to)){
		echo "gsd";
		unlink($path);
	} else {
		echo "エラーやり直してください";
		exit;
	}
	header("location: $self");
} else {
	$files=glob("$base_dir/$unknown/*.jpg");
	if(count($files)==0){
		echo "ご協力ありがとうございました。";exit;
	}
	shuffle($files);
	$target=basename($files[0]);
	$remain=count($files);
	$buttons = "";
	foreach($dirs as $key=>$dir){
		$fs=glob("$base_dir/$dir/*.jpg");
		$cnt=count($fs);
		$api="$self?m=mv&target=$target&to=$dir";
		$buttons.="[<a href='$api'>$key($cnt)</a>]";
	}
	echo <<<EOS
<html lang="ja">
<head><meta charset="utf-8"><title>アサガオとヨルガオの振り分け</title>
<meta name="viewport" content="width=300px">
<style>body{text-align: center;}</style></head><body>
<h1>機械学習のデータの分類</h1><br><br>
<h1>アサガオとヨルガオを振り分けてください！ご協力お願いします！</h1>
<h3 style="font-size:12px;">分け方：余計なものが入っている場合はその他です。
アサガオの画像はアサガオ、ヒルガオの画像はヒルガオに分類してください。
それ以外はその他です。</h3>
<h5>もしAlreadyとでたら、そのリンクをクリックしてください。</h5>
<h2>残り$remain  枚</h2>
<img src="./image/$unknown/$target" width="120" height="120"><br><br>$buttons
<footer>
<div>
<a href="https://scratch.mit.edu/studios/25097422/curators/">scratchサイト</a>
</div>
</footer>
</body>
</html>
EOS;
}

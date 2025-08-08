<?php
include 'mail.php';
include 'sql.php';
session_start();
function home(){
	header("location: ../index.php");
}
function generateLink($user){
	$token = random_int(10000000000, 99999999999);
	$time = time();
	sql("UPDATE users SET token = '$token' WHERE username = '$user';");
	$pass = sql("SELECT passward FROM users WHERE username = '$user';");
	$url = "http://".$_SERVER['SERVER_NAME']."/Reset.php?user=".$user."&time=".$time."&sig=".generateSig($user, $token, $time, $pass);
	sendMail($user, $url);
}
function validateLink($sig, $time, $user){
	$token = sql("SELECT token FROM users WHERE username = '$user';");
	$pass = sql("SELECT passward FROM users WHERE username = '$user';");
	if($token!=null){
		if (tokenExpiry($time)) {
			if(generateSig($user, $token, $time, $pass) == $sig){
				$_SESSION['login_user'] = $user;
				header("location: NewPass.php");
			}
			else{
				home();
			}
		}
		else{
			home();
		}
	}
}
function generateSig($user, $token, $time, $pass){
	return substr(hash("sha256", $user."|".$token."|".$time."|".$pass), 0, 8);
}
function tokenExpiry($time){
	$expiry = $time + 6*60*60; // 6 Hours
	if(($expiry - time()) <=0){
		return false;
	}
	return true;
}
if($_SERVER["REQUEST_METHOD"] == "POST"){
	if($_POST['user']!=null){
		generate_link($_POST['user']);
	}
	else{
		home();
	}
}
else{
	if($_GET['sig']!=null){
		validateLink($_GET['sig'], $_GET['time'], $_GET['user']);
	}
	else{
		home();
	}
}
?>
<?php
include 'sql.php';
session_start();
$count = 0;
if($_SERVER["REQUEST_METHOD"] == "POST"){
	$user = $_POST['username'];
	$pass = $_POST['password'];
	sql("SELECT id FROM users WHERE username = '$user' and password = '$pass';");
	if($count == 1) {
         $_SESSION['login_user'] = $user;
         header("location: home.php");
      }else {
         echo "Username/Password incorrect";
      }
}
?>
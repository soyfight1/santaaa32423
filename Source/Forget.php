<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <title>Source Code Review Challange - Vulnmachines</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body style="background: url(Logo.png) no-repeat left #000000;">
<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css">
<a style="text-align: right;" href="Source.zip">Source Code</a>
<div class="login">
  <h2 class="active">Forget Password</h2>
  <form>
<input type="text" class="text" name="username" id="username">
     <span>username</span>
    <br> 
    <label id="forget" style="display:none;" for="checkbox-1-1">We have e-mailed your password reset link.</label>
    <input type="button" class="signin" onclick="forget();" value="Send Password Reset Link"><hr>
  </form>
</div>
</body>
<script>
function forget(){
	document.getElementById('forget').style.display = 'inline';
	var http = new XMLHttpRequest();
	var url = 'Reset.php';
	var params = 'user='+document.getElementById('username').value;
	http.open('POST', url, true);
	http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	http.send(params);
}</script></html>
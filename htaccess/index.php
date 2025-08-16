<?php

require_once __DIR__.'/inc/top.php';

if (isset($_GET['page']) && is_string($_GET['page']))
{
	$page = __DIR__.'/inc/'.$_GET['page'];

	if (!file_exists($page))
	{
		printf('<div class="error">This page doesn\'t exist!</div>');
		exit();
	}

	require_once $page;
}
else
	require_once __DIR__.'/inc/home.php';

require_once __DIR__.'/inc/footer.php';

?>

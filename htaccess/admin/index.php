<?php

if (!isset($_SERVER['REQUEST_URI']) || $_SERVER['REQUEST_URI'] != '/admin/')
	die('<div class="error">Invalid URI</div></div></body></html>');

require_once __DIR__.'/../inc/top.php';

define('CHALLENGE_FLAG_PART1', 'FLAG_PART_1');

print "<p>";

printf('You bypassed the first <strong>.htaccess</strong> and successfully entered the <em>admin</em> area.<br />
Flag part 1 is <strong>%s</strong>
<br /><br />Now try to bypass the second one to enter the <em>superadmin</em> are.', CHALLENGE_FLAG_PART1);
print "</p>";

print '<a href="/superadmin/">Superadmin</a>';

require_once __DIR__.'/../inc/footer.php';

?>

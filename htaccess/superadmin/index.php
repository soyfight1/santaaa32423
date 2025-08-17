<?php

if (!isset($_SERVER['SCRIPT_NAME']) || $_SERVER['SCRIPT_NAME'] != '/superadmin/index.php')
	die('<div class="error">Invalid URI</div></div></body></html>');

require_once __DIR__.'/../inc/top.php';

define('CHALLENGE_FLAG_PART2', 'FLAG_PART 2');

print "<p>";
printf('Congratulations! You bypassed the second <strong>.htaccess</strong> too.<br /><br />
Flag part 2 is <strong>%s</strong>.<br /><br />
Final flag is <strong>part1_part2</strong> (include the underscore).', CHALLENGE_FLAG_PART2);
print "</p>";

require_once __DIR__.'/../inc/footer.php';

?>

<?php

ob_start();

(include_once 'config.php') === false
    ? die
    : (include_once $incDir .'/'. $securityFile . $incExt) === false
        ? die
        : (include_once $incDir .'/'. $headerFile . $incExt) === false
            ? die
            : isset($_GET['p'])
                ? is_string($_GET['p'])
                    ? secure($_GET['p'])
                        ? include $_GET['p'] . $pageExt
                        : include_once 'home' . $pageExt
                    : include_once 'home' . $pageExt
                : include_once 'home' . $pageExt;
(include_once $incDir .'/'. $footerFile . $incExt) === false
    ? ob_clean()
    : null ;

ob_end_flush();

?>

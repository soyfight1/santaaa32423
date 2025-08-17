<?php

if( defined('CONFIG') === false ) die;

function secure($url)
{
    define('START',   1);
    define('END',     2);
    define('CONTAIN', 4);
    define('MATCH',   8);

    $filters = Array(
        'http://'  => START,
        'https://' => START,
        'ftp://'   => START,
        'ftps://'  => START,
        'file://'  => START,
        '/'        => START,
        '..'       => CONTAIN
    );

    foreach ($filters AS $rule => $type)
    {
        $rule = preg_quote($rule);
        switch ($type)
        {
            case START   : $pattern = '#^'.$rule.'#i';  break;
            case END     : $pattern = '#'.$rule.'$#i';  break;
            case CONTAIN : $pattern = '#'.$rule.'#i';   break;
            case MATCH   : $pattern = '#^'.$rule.'$#i'; break;
        }
        if (preg_match($pattern, $url))
            return false;
    }

    return true;
}

?>

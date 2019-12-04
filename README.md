# ChargePoints

## lighttpd configuration ##
This is the fastcgi component of lighttpd.conf. It's pointing to two different directories hosting different flask apps.
```
fastcgi.server = ("/ChargePoints" =>
((
    "socket" => "/var/run/lighttpd/test-fcgi.sock",
    "bin-path" => "/var/www/ChargePoints/application.fcgi",
    "check-local" => "disable",
    "max-procs" => 1
))
,

"/testing" =>
((
    "socket" => "/var/run/lighttpd/test-fcgi2.sock",
    "bin-path" => "/var/www/testing/test.fcgi",
    "check-local" => "disable",
    "max-procs" => 1
))


)

alias.url = (
"/static" => "/var/www/ChargePoints/static"
)

url.rewrite-once = (
"^(/static($|/.*))$" => "$1",
"^(/.*)$" => "/$1"
)
```

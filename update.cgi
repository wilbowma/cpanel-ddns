#!/home/wilbowma/bin/petite --script
(import (oleg cgi processing))

(define (output-ip)
  (let* ([json-data '((cpanel_jsonapi_version . 2)
                     (cpanel_jsonapi_module . ZoneEdit)
                     (cpanel_jsonapi_func . edit_zone_record)
                     (address . ,(getenv "$REMOTE_ADDR"))
                     ;; The below values depend on your website
                     (line . 29)
                     (domain . example.com)
                     (name . subdomain)
                     (ttl . 14400)
                     (type . A))]
        ;; These are your cpanel credentials
        [username "user"]
        [password "password"]
        [cpanel_url "http://cpanel.example.com"]
        ;; building the curl commands
        [opts "-c cookies.txt -b cookies.txt"]
        [json_api (fold-left 
                    (lambda (str pair)
                      (string-append 
                        str
                        (any->string (car pair))
                        "="
                        (any->string (cdr pair))
                        "&"))
                    "json-api/cpanel?" 
                    json-data)])
    (system 
      (string-append "curl " opts
                     " -d " username 
                     " --data-urlencode '" password "'"
                     " '" cpanel_url "/login/'"))
    (system
      (string-append "curl " opts
                     " '" cpanel_url "/" json_api "'"))))

(define (check-password passw)
  ;; Maybe hash it using string->number and string-hash
  (eq? passw "ddns password" ))

(define (check-useragent agent)
  ;; In case you want ot spoof the agent for added security
  (string=? agent "DDNS"))

(define (check-referer referer)
  ;; In case you want to spoof the referer for added security
  (string=? referer "example.com/somepage that doesn't exist"))

(define (check-request)
  (and (with-exception-handler
         (lambda (c) 
           (error 'main "Missing password"))
         (lambda () (check-password (cgi:lookup 'password 'string))))
       (check-useragent (getenv "HTTP_USER_AGENT"))
       (check-referer (getenv "HTTP_REFERER"))
       #t))

(define (response)
  "Content-type: text/plain\n\n")

(with-exception-handler
  cgi:exception-handler
  (lambda () 
    (if (check-request) 
        (begin
          (display (response))
          (output-ip))
        (error 'main "invalid password"))))

# Brief
You probably need to setup and config nginx in case you are not using load balaner provided by public cloud.

# Install nginx
```bash
# assuming you are root user
yum update
yum install epel-release
yum update

yum install nginx
systemctl enable nginx
systemctl start nginx
```

# Install cert bot
```bash
sudo yum install certbot
```

# Acquire cert
```bash
certbot certonly --manual
```

You may need to include `sparkbase/cert-bot.conf`, here is an example:
```
    # Test setting when you trying to get cert from let's encrypt
    # you can put whatever you want in /var/www/html
    server {
        listen              80;
        server_name         superset.dmbricks.com;

        location ~ ^/.well-known/acme-challenge/ {
            default_type "text/plain";
            rewrite /.well-known/acme-challenge/(.*) /$1 break;
            root /var/www/html/letsencrypt;
        }
    }
```

Once you got the cert, you can include proxy setting for the server, for example: `sparkbase/superset.conf`:
```
   # for https://superset.dmbricks.com
    server {
        listen              80;
        server_name         superset.dmbricks.com;
        return 301 https://superset.dmbricks.com$request_uri;
    }
    server {
        listen              443 ssl;
        server_name         superset.dmbricks.com;

        ssl_certificate     /etc/letsencrypt/live/superset.dmbricks.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/superset.dmbricks.com/privkey.pem;

        location / {
            proxy_pass http://superset:8088;

            proxy_http_version  1.1;
            proxy_cache_bypass  $http_upgrade;
            proxy_set_header Upgrade           $http_upgrade;
            proxy_set_header Connection        "upgrade";
            proxy_set_header Host              $host;
            proxy_set_header X-Real-IP         $remote_addr;
            proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host  $host;
            proxy_set_header X-Forwarded-Port  $server_port;
        }
    }
```

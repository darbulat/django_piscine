server {
	listen 80 default_server;
	listen [::]:80 default_server;

	return 301 https://$host$request_uri;
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    charset  utf-8;
    # max upload size
    client_max_body_size 512M;   # adjust to taste


    location / {
        include proxy_params;
        proxy_pass http://unix:/project/django_gunicorn.sock;
        proxy_buffering off;
    }
    location /static {
        alias /project/d08/static;
    }
    location /media {
        alias /project/d08/media;
    }
    # disable all robots
    location /robots.txt {
        return 200 "User-agent: *\nDisallow: /";

    }
}


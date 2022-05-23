server
{
	listen 80 default_server;
	listen [::]:80 default_server;
	return 301 https://$server_name$request_uri;
}

server
{
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
	ssl_certificate		/etc/ssl/certs/nginx-selfsigned.crt;
	ssl_certificate_key	/etc/ssl/private/nginx-selfsigned.key;

    location / {
        include proxy_params;
        proxy_pass http://unix:/project/django_gunicorn.sock;
        proxy_buffering off;
    }
}


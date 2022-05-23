server
{
	listen 80 default_server;
	listen [::]:80 default_server;

    location / {
        include proxy_params;
        proxy_pass http://unix:/project/django_gunicorn.sock;
        proxy_buffering off;
    }
}


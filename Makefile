install:
    sudo apt update
    sudo apt install -y nginx

configure-nginx:
    sudo cp nginx.conf /etc/nginx/sites-available/flask-api
    sudo ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx

start-gunicorn:
    gunicorn --bind 127.0.0.1:8000 -w 4 shamir.api.app:app


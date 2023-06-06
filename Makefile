configure-nginx:
    sudo apt update
    sudo apt install -y nginx
    sudo cp config/nginx.conf /etc/nginx/sites-available/flask-api
    sudo ln -s /etc/nginx/sites-available/flask-api /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx

start-gunicorn:
	gunicorn -c config/gunicorn.py shamir.api.app:app


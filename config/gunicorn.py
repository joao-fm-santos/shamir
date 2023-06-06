# On AWS, the gunicorn server is running on port 8000
# And all incoming HTTP traffic is being routed from public_ip:80 
# to "127.0.0.1:8000" from NGINX.
# See the repo for more information on how to set up NGINX.
bind = "127.0.0.1:8000"
workers = 1
loglevel = "debug"

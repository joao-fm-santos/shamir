# shamir

[![License: MIT](https://img.shields.io/badge/licence-mit-blue.svg)](LICENSE)

## Introduction 
The shamir is a one-time secret sharing application that allows users to 
safely share secrets by using unique IDs as references. 

Each secret can only be accessed once and has a expiration of 15 minutes.

With this API, you can share sensitive information within teams 
without directly exposing them in chat applications or other communication channels. 

In this application, we provide some shell aliases to facilitate requesting secret creation and 
secret retrieval. The goal here is to do the minimum effort to share a secret, as such each alias 
will copy the secret or the ID to the clipboard after the request has been made, which makes it 
very convenient to use.

Below you can find a guide with step-by-step instructions for deploying the 
the API on AWS EC2 using Nginx and Gunicorn.

## Features

- Secret sharing: share secrets by using unique IDs as references, ensuring confidentiality.
- Team collaboration: Enable teams to share sensitive information without exposing it in chat applications or other channels.
- Easy deployment: Deploy the Shamir API on AWS EC2 with Nginx and Gunicorn, following the instructions in this guide.

## Prerequisites

- AWS EC2 instance with Ubuntu 18.04 or higher as the operating system.
- Basic knowledge of AWS EC2, SSH, and command line.

## Installation

1. Connect to your AWS EC2 instance via SSH.
2. Clone the Shamir API repository:

   ```shell
   git clone https://github.com/squerez/shamir.git
   ```
3. Navigate to the project directory:

   ```shell
   cd shamir/
   ```
4. Install required dependencies:

   ```shell
   pip install -r requirements.txt
   ```
5. Install NGINX:

   ```shell
   make install
   ```
6. Replace `YOUR_DOMAIN_OR_PUBLIC_IP` in the `config/nginx.conf` with your domain or public ip.
   and then run:

   ```shell
   make configure-nginx
   ```
7. Start gunicorn:
   ```shell
   make start-gunicorn
   ```
   Adjust the gunicorn configuration in `config/gunicorn.py` according to your preferred settings.

## Usage 

To access the Shamir API, use the public IP or domain name of your 
AWS EC2 instance along with the appropriate endpoints. 

Follow the guidelines below:

    Create a secret:
        Endpoint: http://your-public-ip-or-domain/create
        Method: POST
        Request body: { "secret": "your-secret" }
        Response: { "id": "unique-id" }

    Get a secret:
        Endpoint: http://your-public-ip-or-domain/get/<secret-id>
        Method: POST
        Response: { "message": "shared-secret" }

Please note that you need to replace your-public-ip-or-domain
with the actual public IP or domain name of your AWS EC2 instance.

### Setting aliases 

In your `.zshrc`, add the following aliases:

```
# Shamir API Aliases
export ssc='shamir_create'
export ssg='shamir_get'

shamir_create() {
    SHAMIR_RESPONSE=$(
        curl -s -X POST -H "Content-Type: application/json" -d "{\"secret\": \"$1\"}" http://your-public-ip-or-domain/create
    )

    echo $SHAMIR_RESPONSE | jq -r '.id' | xsel -b
    echo "Secret created with ID: $(echo $SHAMIR_RESPONSE | jq -r '.id')"
}

shamir_get() {
    SHAMIR_RESPONSE=$(
        curl -s -X GET http://your-public-ip-or-domain/get/$1
    )

    echo $SHAMIR_RESPONSE | jq -r '.message' | xsel -b
    echo "Secret copied from ID: '$1'"
}
```
This sets the `ssc` and `ssg` alias to the `shamir_create` and `shamir_get` functions, which get and create secrets directly in the API by doing `curl` requests.
Please note that you need to replace your-public-ip-or-domain with the actual public IP or domain name of your AWS EC2 instance.

Once you have done these modifications, save the file and run `source ~/.zshrc` to apply the aliases.

## Additional Information

- Make sure to open the necessary ports (e.g., port 80) in your AWS EC2 security group settings to allow inbound traffic.
- Customize the Nginx configuration file (nginx.conf) and the Gunicorn command as per your requirements.
    
## License

This project is licensed under the MIT License.

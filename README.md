<div align="center">
  <img src="noxcrux_server/static/images/logo_readme.svg">
</div>

# noxcrux 🔒
noxcrux is a Django web app and API which allows you to create and store passwords horcruxes to improve your online security.  

## Introduction 🖋️
The persons intended by this project are people who are a minimum aware of online security risks and at least use a password manager.  

noxcrux was inspired by [this article](https://kaizoku.hashnode.dev/double-blind-passwords-aka-horcruxing#double-blind-passwords-aka-horcruxing) and the concept of horcruxes from the universe of Harry Potter.  
The aim of this project is to split passwords in multiple horcruxes to mitigate the single point of failure risk induced by password managers.  

**Password horcruxes are not 2FA/MFA and does not pretend to replace it at all.** A password is a sole factor (knowledge) and noxcrux allows you to distribute it across platforms.

The project is still in early development stage (see the [features](#features) and the [to-do list](#todo-list) below) but the end goal is to offer to the users multiple noxcrux' servers to connect to and distribute their online accounts access security to different places.  

A web extension will be later developed to allow end users to easily manage their noxcrux' servers and to retrieve and assemble their complete password when they want to login to a website.  

### Demo
Here is a link of a live demo of this project:  
https://hydrogen.noxcrux.com/

⚠️ **This is for demonstration purposes only, you should not rely on it.** ⚠️  
⚠️ **I do not guarantee any SLA and I may shutdown the service or wipe the database without any warrant.** ⚠️

## Table of contents 📋
See below the top level parts of this README:  

+ [Technologies](#technologies-%EF%B8%8F)
+ [Features](#features-)
+ [Getting Started](#getting-started-%EF%B8%8F)
+ [Docker](#docker-)
+ [API Reference](#api-reference-)
+ [Todo list](#todo-list-)
+ [Contributing](#contributing-)
+ [Support](#support-)
+ [Licence](#licence-)

## Technologies ⚙️
noxcrux is powered by [Django](https://www.djangoproject.com/) a well-known python web framework and [DRF](https://www.django-rest-framework.org/) for the API ([Spectacular](https://github.com/tfranzel/drf-spectacular) for the reference).  
It also makes use of [Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/) and [SASS](https://sass-lang.com/) for the web interface.  

Here is a table with the main technologies, and their current version:  

| Technology            | Version   |
|-----------------------|:---------:|
| Django                | 3.2       |
| Django Rest Framework | 3.12      |
| DRF Spectacular       | 0.17      |
| Bootstrap             | 4.5       |
| jQuery                | 3.5       |
| SASS                  | 1.32      |

## Features ✅
Here is a list of the main features provided by this project:  
+ [x] CRUD on horcruxes
+ [x] Horcrux generator
+ [x] Horcrux sharing
+ [x] Personal account management
+ [x] Sessions management
+ [x] 2-Factor Authentication
+ [x] Self API Reference
+ [x] Brute-force protection
+ [x] Easy & Secure deployment with Docker

## Getting Started 🛠️
Here is what you need to do to get a noxcrux server up & running. This is also the recommended way to install it for a development setup.

Here are the commands to build the application straight from the sources, find below the [Docker instructions](#docker) for a production-ready environment or to just quickly get a server running.

### Prerequisites
noxcrux is being developed and tested on debian-based distro, so you will see below the commands for these distributions.

Django is a python web framework so first you need python and pip to later install modules.  
I bet you already have them both installed but just in case, here are the commands.  

⚠️ **python3 is required and noxcrux is being developed and tested against python 3.8** ⚠️
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip
```

### Modules
Fetch the code from the repository and enter the folder.  
```bash
git clone https://github.com/noxPHX/noxcrux.git && cd noxcrux
```
Install Django and the other modules.  
```bash
pip3 install -r requirements.txt
```
Ideally, you may setup a virtual environment if you do not want to mess with your host dependencies.
```bash
sudo apt install python3-venv
python3 -m venv ./.venv/
source .venv/bin/activate
pip3 install -r requirements.txt
```

### SASS
As mentioned before, noxcrux makes use of [SASS](https://sass-lang.com/), so you need to compile SCSS files into regular CSS files because these files are not tracked by git.  
In order to install it, follow the instructions from https://sass-lang.com/.  
I personally prefer to grab the latest release from https://github.com/sass/dart-sass/releases and untar the file somewhere in my path to be able to use it.  
```bash
wget -O /tmp/sass.tgz https://github.com/sass/dart-sass/releases/download/1.32.5/dart-sass-1.32.5-linux-x64.tar.gz
tar -xzf /tmp/sass.tgz -C /tmp
mv /tmp/dart-sass/* /usr/local/bin
rm -r /tmp/sass.tgz /tmp/dart-sass
```

### Database
noxcrux uses PostgreSQL as database engine, for an easy setup you can use [Docker](https://docs.docker.com/get-docker/) and [Compose](https://docs.docker.com/compose/) and simply running the following commands in the docker directory:
```bash
cd docker
echo 'noxcrux_db_passwd' > secrets/noxcrux_db_passwd.txt
docker-compose up -d noxcrux_db
```
Otherwise, you can check how to install and configure PostgreSQL manually [here](https://www.postgresqltutorial.com/postgresql-getting-started/).

### Configuration
In order to properly run the application, you might want to define some environment variables.  
Find below a table with each variable, their description, type and default value.  

| Variable               | Description                             | Type                                                              | Default          |
|------------------------|-----------------------------------------|-------------------------------------------------------------------|------------------|
| DEBUG                  | Enable or disable debug mode            | Boolean                                                           | True             |
| REGISTRATION_OPEN      | Enable or disable user registration     | Boolean                                                           | True             |
| ALLOWED_HOSTS          | Allowed hosts to access the application | Comma-separated values (eg "localhost,127.0.0.1")                 | *                |
| DB_HOST                | Database IP address or hostname         | String (eg "172.26.0.74" if using the noxcrux_db container)       | 172.26.0.74      |
| DB_PORT                | Database port                           | String                                                            | 5432             |
| DB_NAME                | Database name                           | String                                                            | noxcrux          |
| DB_USER                | Database user                           | String                                                            | noxcrux          |
| DB_PASSWORD            | Database password                       | String                                                            | noxcrux          |
| CORS_ALLOW_ALL_ORIGINS | Enable or disable all origins for CORS  | Boolean                                                           | False            |
| CORS_ALLOWED_ORIGINS   | Allowed origins for CORS                | Comma-separated values (eg "https://localhost,https://127.0.0.1") | http://localhost |

For the last step of the configuration, you need to generate your secret key for Django, the following command will suffice:
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' > secret_key.txt
```
If you cannot use python (eg with Docker setup), you can use this plain bash command:
```bash
cat /dev/urandom | tr -dc 'a-z0-9\!\@\#\$\%\^\&\*\(\-\_\=\+\)' | head -c 50 > secret_key.txt
```

### Final steps
Before running the server there are only the database migrations left:
```bash
python3 manage.py migrate
```
Finally, start the server.  
```bash
python3 manage.py runserver
```

## Docker 🐳
### Stack
The `docker-compose.yaml` file defines 3 services:
+ **noxcrux_db**, which is a PostgreSQL container with a volume to persists the database
+ **noxcrux_web**, which contains gunicorn serving the python application
+ **noxcrux_nginx**, a nginx container which handles SSL and serve static files thanks to a shared volume with **noxcrux_web**

### Requirements
For a quick & easy setup you can use [Docker](https://docs.docker.com/get-docker/) and [Compose](https://docs.docker.com/compose/), the following versions are the minimal requirements:

| Tool          | Version |
|:-------------:|:-------:|
| Docker        | 19      |
| Compose       | 1.29    |

### Setup
I do not provide (yet) an image on the [Docker hub](https://hub.docker.com/) so you need to build your image locally.  

The instructions below are also valid for a production deployment.  
First you need to fetch the code if you do not have already and enter the folder.  
```bash
git clone https://github.com/noxPHX/noxcrux.git && cd noxcrux
```

As of earlier, you need to generate the secret key, and you might want to adjust the environment variables in the `docker-compose.yaml` file. Please refer to the [Configuration](#configuration) section.

### SSL
The Compose stack comes with a nginx container which needs a certificate and its private key as well as Diffie-Hellman parameters.
For the certificate, you can retrieve a free one from [Let's Encrypt](https://letsencrypt.org/) and place it in the `docker/ssl` folder.  

Otherwise, you can quickly generate a self-signed certificate for testing purposes (for a production environment you need a valid certificate):
```bash
openssl req -x509 -newkey rsa:4096 -nodes -keyout docker/ssl/privkey.pem -out docker/ssl/fullchain.pem -days 365 -subj '/CN=localhost' -addext "subjectAltName=IP:127.0.0.1,IP:0.0.0.0"
```

Regarding the D-H parameters you can generate them as follows:
```bash
openssl dhparams -out docker/ssl/dhparams.pem 4096
```
*Depending on your machine, you might have time to grab a coffee* ☕

### Run!

When you are ready, these commands will suffice to build the images and run the application. 
```bash
docker-compose build
docker-compose up -d
```

## API Reference 🔌
### Swagger UI
[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool which facilitates interaction with an API. Integrated in [DRF-Spectacular](https://github.com/tfranzel/drf-spectacular), simply running the application provides your own API reference, you can find it browsing the */web/api/docs* URL.  
Alternatively, you can find it here : https://hydrogen.noxcrux.com/web/api/docs/

### Schema
If you want to build your own OpenAPI schema, for instance to import it in your development tools, execute the following command.
```bash
python3 manage.py spectacular --file schema.yaml
```

## Todo list 📝
Here is a list of what is left to be done:  

+ [ ] Security Headers
+ [ ] Import / Export Horcruxes
+ [ ] Password / TOTP recovery
+ [ ] Tests
+ [ ] User groups sharing ❔
+ [ ] Themes ❔
+ [ ] Delegated authentication ❔
+ [ ] Landing page ❔
+ [ ] & More

*❔ marked features are unsure to be implemented yet*

## Contributing 🤝
Pull requests are welcome. For major changes, please open a discussion first to talk about what you would like to change.

### Bug reports
Please file an [issue](https://github.com/noxPHX/noxcrux/issues) if anything isn't working the way it is expected.

### Security
Please see the [Security Policy](https://github.com/noxPHX/noxcrux/security/policy).  

## Support ⭐️
Give a ⭐️ if you like this project and want to support it!

## Licence 📃
[GNU General Public Licence v3.0](https://github.com/noxPHX/noxcrux/blob/main/LICENSE)

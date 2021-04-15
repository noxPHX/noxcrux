<div align="center">
  <img src="noxcrux_server/static/images/logo_readme.svg">
</div>

# noxcrux <img width="20" src="noxcrux_server/static/images/favicon.svg">
noxcrux is a Django web app and API which allows you to create and store passwords horcruxes to improve your online security.  

## Introduction 🖋️
The persons intended by this project are people who are a minimum aware of online security risks and at least use a password manager.  

noxcrux was inspired by [this article](https://kaizoku.hashnode.dev/double-blind-passwords-aka-horcruxing#double-blind-passwords-aka-horcruxing) and the concept of horcruxes from the universe of Harry Potter.  
The aim of this project is to split passwords in multiple horcruxes to mitigate the single point of failure risk induced by password managers.  

**Password horcruxes are not 2FA/MFA and does not pretend to replace it at all.** A password is a sole factor (knowledge) and noxcrux allows you to distribute it across platforms.

The project is still in early development stage (see the [features](#features) and the [to-do list](#todo-list) below) but the end goal is to offer to the users multiple noxcrux' servers to connect to and distribute their online accounts access security to different places.  
At the moment there is no live demo of this project so if you are interested in using it you need to set it up yourself for one or multiple servers (see [instructions](#getting-started) below).  

A web extension will be later developed to allow end users to easily manage their noxcrux' servers and to retrieve and assemble their complete password when they want to login to a website.  

## Table of contents 📋
See below the top level parts of this README:  

+ [Technologies](#technologies)
+ [Features](#features)
+ [Getting Started](#getting-started)
+ [Usage](#usage)
+ [API Reference](#api-reference)
+ [Todo list](#todo-list)
+ [Contributing](#contributing)
+ [Licence](#licence)

## Technologies ⚙️
noxcrux is powered by [Django](https://www.djangoproject.com/) a well-known python web framework and [DRF](https://www.django-rest-framework.org/) for the API ([Spectacular](https://github.com/tfranzel/drf-spectacular) for the reference).  
It also makes use of [Bootstrap](https://getbootstrap.com/), [jQuery](https://jquery.com/) and [SASS](https://sass-lang.com/) for the web interface.  

Here is a table with the main technologies, and their current version:  

| Technology            | Version   |
|-----------------------|:---------:|
| Django                | 3.2       |
| Django Rest Framework | 3.12.4    |
| DRF Spectacular       | 0.15.1    |
| Bootstrap             | 4.5.2     |
| jQuery                | 3.5.1     |
| SASS                  | 1.32.5    |

## Features ✅
Here is a list of the main features provided by the API and the web interface:  
+ [x] CRUD on horcruxes
+ [x] Personal account management
+ [x] Horcrux generator
+ [x] 2-Factor Authentication
+ [x] Friendship
+ [x] Horcrux sharing
+ [x] Self API Reference
+ [x] Brute-force protection

## Getting Started 🛠️
Here is what you need to do to get a noxcrux server up & running.

### Prerequisites
noxcrux is being developed and tested on debian-based distro, so you will see below the commands for these OSes.

Django is a python web framework so first you need python and pip to later install modules.  
I bet you already have them both installed but just in case, here are the commands.  
```bash
sudo apt update && sudo apt upgrade
sudo apt install python3 python3-pip
```

### Installing
Fetch the code from the repository and enter the folder.  
```bash
git clone https://github.com/noxPHX/noxcrux.git && cd noxcrux
```
Install Django and the other modules.  
```bash
pip3 install -r requirements.txt
```
As mentioned before, noxcrux makes use of SASS, so you need to compile SCSS files into regular CSS files because these files are not tracked by git.  
In order to install it, follow the instructions from https://sass-lang.com/.  
I personally prefer to grab the latest release from https://github.com/sass/dart-sass/releases and untar the file somewhere in my path to be able to use it.  

Create the database scheme (I still use sqlite at the moment).  
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
Finally, start the server.  
```bash
python3 manage.py runserver
```

### Docker
## API Reference 🔌
Running the application provides your own API reference, you can find it browsing the */api/docs* endpoint.

## Todo list 📝
Here is a list of what is left to be done:  

+ [ ] PostgreSQL
+ [ ] Deployment (Docker)
+ [ ] Horcrux / Friend lookup
+ [ ] Import / Export Horcruxes
+ [ ] User groups sharing (?)
+ [ ] Themes (?)
+ [ ] Delegated authentication (?)
+ [ ] Landing page (?)

*(?) marked features are unsure to be implemented yet*

## Contributing 🤝
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Licence 📃
[GPL-3.0](https://github.com/noxPHX/noxcrux/blob/main/LICENSE)

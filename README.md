# Utsavify 
#### Video Demo:  https://youtu.be/BVXHvJ73tSw
#### Description:
Welcome to Utsavify, your go-to platform for organizing and managing events with ease.
Utsavify is a web application (currently backend) designed to simplify event management Currently, just API-endpoints. Here, you can create your own clubs, host events and share the information about it.
![Landing Page of Utsavify!](https://github.com/payalmohnani/Utsavify/blob/main/static/Landing_Page.png)
This performs the CRUD operations for Society/Club, Events, and Users.
### Society or Club Creation
Get started by creating your club or community. Utsavify lets you set up your space for all your events.
### Event
As a user and creator of a club/society, you can easily create events within your club and/or for other students. Just provide the details, and you're good to go.
A user can get the information about upcoming events.
### User
You can Sign In or Register yourself using **Create** user.
Or can get your profile Information using **Read ** or Get.
### API documentation of the file:
We provide detailed API documentation through Swagger UI, making integration and development a smooth process.
![Documentation](https://github.com/payalmohnani/Utsavify/blob/main/static/API_doc.png)
### Login
Most operation other than "Read" require User to be authenticated (Logged In). First, SignIn or Register by the Create User command and then LogIn
![Authorization](https://github.com/payalmohnani/Utsavify/blob/main/static/Login.png)
 

## Installation
#### Clone the Repo
Run:
```
git clone https://github.com/payalmohnani/Utsavify.git
```
#### Activate virtual Environment
Activate your virtual environment by executing the **Activate.bat** in venv/Scripts directory of the root folder.

#### Install Dependencies 
Run:
```
pip install -r requirements.txt
```
#### Run Tests
Run:
```
pytest
```
If all tests pass, move further.
#### Start the server
Run following command in the root (project) folder
```
python project.py
```
And voila! project is live at Localhost
http://localhost:8000/

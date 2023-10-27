# Utsavify 
#### Video Demo:  https://youtu.be/BVXHvJ73tSw
#### Description:
Utsavify is a web application (currently backend) designed to simplify event management Currently, just API-endpoints. Here, you can create your own clubs, host events and share the information about it.
![Landing Page of Utsavify!](https://github.com/payalmohnani/Utsavify/blob/main/static/Landing_Page.png)
This performs the CRUD operations for Society/Club, Events, and Users.
### Society
Create and Manage your own Society or Club. 
![Documentation](https://github.com/payalmohnani/Utsavify/blob/main/static/Doc_1.png)
### Event
Any Society can create, update or delete its upcoming Event.
A user can get the information about upcoming events.
API documentation of the file:
### User
You can Sign In or Register yourself using **Create** user.
Or can get your profile Information using **Read ** or Get.
![Documentation](https://github.com/payalmohnani/Utsavify/blob/main/static/Doc_2.png)
### Login
Most operation other than "Read" require User to be authenticated (Logged In). First, SignIn or Register by the Create User command and then LogIn
![Authorization](https://github.com/payalmohnani/Utsavify/blob/main/static/Login.png)

### Other Details
Postgres Database is used and Alembic is used to handle migrations (So, main programming stays in Python only.) 

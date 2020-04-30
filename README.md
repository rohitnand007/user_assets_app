#Readme:

The Web Application is built using python and Flask for backend and Html, css and Bootstrap for front-end

#Running the server...
change the instance/config.py file to connect to your mysql database accordingly.

#go to root of your directory to and use command: flask run

#The server runs in Development environment.

1)once the database url is changed, run the following commands to setup db and running the migrations.
>flask db init
>flask db migrate
>flask db upgrade.

#Pathway to check the usage:
1) when the server runs: open your browser and type http://localhost:5000/
2) The page you witness is the default home page for unauthenticated users.
3) click on Register link on the top nav-bar.
4) Create an account with name and password and other attributes(any value is accepted except Null values).
5) once successfully registered, an object is created and saved in the User model and other needed static data is created in anonymouusly in the backend such as location, inventory,etc.. for maintaining the databse schema relationships between the model entities.(The databse is created according to the UML diagram sent to me)
6) You'll be redirected towards the login page, use your name and password for logging in.
7) A current_user object is created and all other actions are saved to this object.
8) Click on create assets list page to view assets , then click on create asset to create a new asset and edit and delete the asset accordingly.
9) Assets of one user cannot be viewed by other users.

10) Testing:

create a new database for testing purposes and change the url in tests.py file in the root folder.
Run: Python tests.py for running the unit tests accordingly.
Test cases are based for entry creation, views etc.

P.S Please rech out for any further queries or assistance.

Thanks and regards,
Rohit Yerramsetty
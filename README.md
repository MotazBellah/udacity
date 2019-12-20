# Currency Converter

Web application contains a list of Udacity Nanodegree and allow the user to choose any program wants to enroll into

## Code style

- This project is written in python 3.
- Flask framework.

## Database Installation on Heroku
### User postgresql on Heroku

1. Create App on Heroku.

2. On app’s “Overview” page, click the “Configure Add-ons” button.

3. In the “Add-ons” section of the page, type in and select “Heroku Postgres.

4. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision..

5. Click the “Heroku Postgres :: Database” link.

6. Click on “Settings”, and then “View Credentials.”. This information to hock my App to the DB

7. use the Credentials to connect the application with the DB

## Create table on DB

- run `python database_setup.py` in order to execute SQL query to create the enrollments table

## Run

- To build the image from Dockerfile run on project directory run `docker build -t flask-backend:latest . `

- To Run the container run `docker run -d -p 5000:5000 flask-backend`

- In order to get the command run `docker ps -a`, which is `python app.py`

- To run the application run `python app.py`

### Create DB

- run `python create.py`

- run `python app.py`

- go to localhost:7000

### Run the tests

- run `python convert_test.py`

A KanBan application for keeping track of various activities with 
each activity having various cards, updated daily.

Technologies used: Flask, Flask-SQLAlchemy, SQLite, matplotlib, pandas, os, datetime, HTML, CSS, Bootstrap, 
Vue.JS, Celery, Redis, smtplib, flask-jwt-extended, brcypt, flask_cors, weasyprint

Flask Flask-SQLAlchemy: Basic routing and database related operations 
Flask_cors: CORS management for the application
Flask-JWT-Extended: Create and manage web tokens
matplotlib: Visualization of trendlines (graphs)
OS library: secret key, root address for saving files
HTML, CSS, Bootstrap: Designing webpages
Datetime library: Retrieve date and time, for timestamps and setting timer expiry
Vue.JS: Create frontend and interface to connect with Flask API
Celery, Redis, smtplib: Asynchronous batch jobs
Pandas: Export data as CSV files
weasyprint: Convert HTML reports to PDF format

API Design: APIs have been created and utilized for signing up and logging in to the user’s account. They are 
also used for performing CRUD operations on lists, as well as cards. APIs are finally used for 
export jobs.


Architecture and Features: The backend folder consists of the business logic – Flask routes, cache description, 
asynchronous jobs, and such. It also contains the report format and the project 
database. The frontend folder consists of all the different views and JS/.VUE files for 
running the application.
There is a sign-up/sign-in form for users, after which they are redirected to the Board view 
for them, from where they can manage their lists and cards, including options to update, 
delete, and export lists/cards, get summaries of lists, and an option to convert the web 
application to a desktop application (Progressive Web Application). There is functionality 
for daily reminders via Google Space and monthly reports sent in PDF reports via email


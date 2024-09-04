## App point system
A system to manage Android apps and user points, featuring both admin and user-facing panels.

## Description
The App Point System allows admin to manage apps, and assign tasks. Users can view apps, complete tasks, and upload screenshots for verification. The system is designed with REST APIs, ensuring authentication and permissions.

## Visuals
[Screencast of admin panel and user panel](https://drive.google.com/file/d/1yEV0vc-rdIO3QHHgGqsLSquzhlYj824l/view?usp=sharing)

## Installation
Clone the repository:
```
git clone https://gitlab.com/varshamohan08/app_point_system.git
cd app_point_system
```
Install dependencies:
```
pip install -r requirements.txt
```
Set up the database:
```
python manage.py migrate
```
Run the application:
```
python manage.py runserver
```
## Dockerization
Build the Docker image:
```
docker build -t point_app .
```
Run the container:
```
docker run -p 8000:8000 point_app
```
(Optional) If using Docker Compose:
```
docker-compose up -d
```
Open the application in the browser at `http://localhost:8000`.

## Usage
**Admin Facing** - Where admin user can add an android app as well as the number of points - earned by user for downloading the app.

**User Facing** - where the user can see the apps added by the admin and the points. The user can Signup and Login, see their profiles, points they earned, points break up and tasks that should be completed. User also have the option to upload a screenshot (which includes drag and drop) for that particular task.

## Author
[Varsha Mohan](https://gitlab.com/varshamohan08)

## License
[MIT License](https://gitlab.com/varshamohan08/app_point_system/-/blob/353d7a2c75855f53a70ab7495d1a81db73c60869/LICENSE)

## Project status
The project is currently under development.

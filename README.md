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

## Problem Set I - Regex
```
import re

text = '{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}'

numbers = re.findall(r'(?<=id":)\d+', text)

print(numbers)

# Output
['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '648', '649', '650', '651', '652', '653']
```
## Problem Set 3
**A. Write and share a small note about your choice of system to schedule periodic tasks (such as downloading a list of ISINs every 24 hours). Why did you choose it? Is it reliable enough; Or will it scale? If not, what are the problems with it? And, what else would you recommend to fix this problem at scale in production?**

**System for Scheduling Periodic Tasks**

For scheduling periodic tasks, such as downloading a list of ISINs every 24 hours, one common approach is to use Celery with a message broker like RabbitMQ or Redis. Celery is a powerful, flexible task queue that allows you to execute tasks asynchronously and schedule periodic tasks.
- Scalability: Celery is designed to handle a large number of tasks and can scale horizontally by adding more worker nodes.
- Flexibility: It supports various message brokers and backends, making it adaptable to different needs.
- Reliability: Celery is reliable and can handle task retries, error logging, and monitoring. It ensures that tasks are executed even if the system or worker fails.
- Scalability: Celery scales well by distributing tasks across multiple worker nodes. However, it requires proper configuration and monitoring to handle large volumes of tasks effectively.

Problems
- Complexity: Celery can be complex to set up and manage, especially with multiple workers and brokers.
- Performance: Celery may have performance issues if not properly tuned or if the message broker becomes a bottleneck.

Solution: Use containerization (e.g., Docker) and orchestration tools (e.g., Kubernetes) to simplify deployment and scaling.

**B. In what circumstances would you use Flask instead of Django and vice versa?**

**Flask is suited for lightweight and flexible applications** or microservices, while **Django is ideal for larger projects** requiring extensive built-in features and a structured approach. The choice depends on the specific needs and scale of the project.

**Use Flask when:**

- You need a lightweight and flexible framework with minimal built-in features, allowing for greater control over components and architecture.
- The project scope is small to medium, and you prefer to have fine-grained control over each component and dependency.


Pros:
- Lightweight: Less overhead and more control over components.
- Flexibility: Allows for easier customization and integration with other libraries.

Cons:
- Manual Setup: Requires more manual setup for features like authentication, form handling, and database integration

**Use Django when:**

- Full-Featured Applications: You need a comprehensive framework with built-in features such as authentication, ORM, admin interface, and form handling.
- Rapid Development: You want to leverage a lot of built-in functionalities to speed up development.
- Large Projects: The project is large and complex, requiring a robust framework with conventions and tools to manage different aspects of the application.

Pros:

- Structured: Offers a structured approach with clear conventions and best practices.

Cons:


- Less Flexible: More opinionated and less flexible compared to Flask, which may impose constraints on how the application is structured
# Task Scheduler

A Django-based Task Scheduler application that allows users to create, manage, and track tasks, with features for reminders and time tracking.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and authentication
- Task creation, updating, and deletion
- Reminder notifications via email
- Time tracking for tasks
- Admin panel for managing all tasks

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery, Redis
- **Email Service**: Mailjet
- **Containerization**: Docker

## Setup Instructions

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone git@github.com:avinashn686/task_scheduler.git
    cd repository-name
    ```

2. Ensure you have Docker and Docker Compose installed. 

3. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```
    use command : " docker-compose run web python manage.py createsuperuser " to create a superuser

4. Open your browser and go to `http://localhost:8000/`.

    To access admin page: http://localhost:8000/admin/

## API Endpoints

### User Registration

- **POST** `/register/`
    - Register a new user.

### User Login

- **POST** `/login/`
    - Log in to the application.

### User Logout

- **POST** `/logout/`
    - Log out from the application.

### Task Management

- **GET** `/tasks/`
    - Retrieve all tasks for the logged-in user or all tasks for admins.

- **POST** `/tasks/`
    - Create a new task.

- **PUT** `/tasks/{id}/`
    - Update an existing task.

- **DELETE** `/tasks/{id}/`
    - Delete a task.

### Time Tracking

- **PATCH** `/tasks/{id}/time-tracking/`
    - Update time spent on a task.

## Usage

1. Register a new user via the registration endpoint.
2. Log in using the login endpoint to receive an authentication token.
3. Use the token to access the task management endpoints.
4. Create, update, and delete tasks as needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [Avinash](mailto:avinashn686@gmail.com).

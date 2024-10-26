# Real-Time Chat App

A web-based chat application built using Django, Django Channels, WebSockets, HTML, and CSS. This app allows multiple users to communicate in real time.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **Real-Time Communication**: Instant messaging using WebSockets for real-time updates.
- **User Authentication**: Sign up, log in, and log out functionality.
- **Multiple Chat Rooms**: Users can create and join different chat rooms.
- **Message History**: Persistent message storage, allowing users to view previous conversations.
- **Responsive Design**: Optimized for both desktop and mobile view.

## Tech Stack
- **Backend**: Django, Django Channels
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or PostgreSQL in production)
- **WebSockets**: Django Channels and Redis as the channel layer (for production)
- **Asynchronous Framework**: ASGI

## Setup and Installation

### Prerequisites
- Python 3.7+
- Redis (for channel layer in production)

### Installation Steps

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/real-time-chat-app.git
    cd real-time-chat-app
    ```

2. **Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**
    - Create a `.env` file in the project root and add the necessary configurations (e.g., `SECRET_KEY`, `DEBUG`).
    - Ensure Redis is running on your local machine or update the channel layer configuration with your Redis server URL.

5. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**
    ```bash
    python manage.py runserver
    ```

8. **Visit the app**
    Open your browser and go to `http://127.0.0.1:8000/` to access the chat app.

## Usage
1. **Sign Up/Login**: Create an account or log in to an existing one.
2. **Create or Join a Chat Room**: Browse existing chat rooms or create a new one.
3. **Start Chatting**: Type messages to chat in real-time with other users in the room.

## Folder Structure

```plaintext
mysite/
├── messaging/                  # Django app for the chat functionality
│   ├── templates/         # HTML templates
│   ├── static/            # Static files (CSS, JS)
│   ├── consumers.py       # WebSocket consumers for handling real-time events
│   ├── routing.py         # Channels routing configuration
│   └── views.py           # Views for rendering chat pages
├── config/
│   ├── settings.py        # Django project settings
│   ├── asgi.py            # ASGI config for Django Channels
│   └── urls.py            # Project URL configuration
├── manage.py
└── README.md



Steps to Contribute
Fork the project.
Create a feature branch: git checkout -b feature-name
Commit your changes: git commit -m 'Add feature name'
Push to the branch: git push origin feature-name
Open a pull request.



MessageApp Real-Time Chat Application

A full-stack chat application built with Django, Django Channels, and WebSockets. Users can sign up, log in, edit profiles, browse other users, and engage in real-time messaging using modern frontend technologies (HTML, CSS, JavaScript).

Features

User Authentication: Secure sign-up, login, and logout.

Profile Management: Update personal information and profile picture (Cloudinary integration).

User Directory: View a list of registered users and their basic info.

Real-Time Chat: Send and receive messages instantly via WebSockets (Django Channels + Daphne).

Message Editing: Edit or delete past messages in real time.

Responsive Design: Mobile-first styling with fluid layouts.

Deployment: Hosted on Render with CI/CD for seamless updates.

Tech Stack

Backend: Django 5.1.1, Django Channels 4.1

ASGI Server: Daphne

Database: SQLite (development), PostgreSQL optional in production

Storage: Cloudinary (media files)

WebSockets: Redis channel layer (In-memory for quick dev) via channels.layers.InMemoryChannelLayer

Frontend: HTML5, CSS3, JavaScript, Font Awesome icons

Deployment: Render.com with whitenoise for static

Getting Started

Prerequisites

Python 3.10+

Git

(Optional) Redis for production WebSocket channel layer

Installation

Clone the repository:

git clone https://github.com/your-username/MessagingApp_Deploy.git
cd MessagingApp_Deploy/mysite

Create & activate virtual environment:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Install dependencies:

pip install -r ../requirements.txt

Environment variables:

Copy .env.example to .env

Set:

SECRET_KEY=<your_django_secret>
DEBUG=True
CLOUDINARY_URL=...
SOCKET_URL=ws://localhost:8000/ws/chat/<room_id>/

Apply migrations & collect static:

python manage.py migrate
python manage.py collectstatic --noinput

Run development server:

daphne mysite.asgi:application --port 8000 --bind 0.0.0.0

Open the app:
Visit http://localhost:8000/rooms/ in your browser.

Project Structure

MessagingApp_Deploy/
├── mysite/                    # Django project
│   ├── messaging/             # Chat app
│   │   ├── consumers.py       # WebSocket consumers
│   │   ├── routing.py         # Channels routing
│   │   ├── templates/         # HTML templates
│   │   ├── static/            # Static assets (css, js, images)
│   │   └── views.py           # View functions
│   ├── config/                # Settings and ASGI/Wsgi
│   ├── manage.py
│   └── requirements.txt       # Dependencies
└── README.md

Environment & Deployment

Static Files: Served by whitenoise in production

Media Files: Managed by Cloudinary via DEFAULT_FILE_STORAGE

WebSocket URL: Configurable via SOCKET_URL env var

Render.com: Automatic build & deploy with the following commands:

Build: pip install -r requirements.txt && pip install cloudinary django-storages && cd mysite && python manage.py collectstatic --noinput && python manage.py migrate

Start: cd mysite && daphne mysite.asgi:application --port $PORT --bind 0.0.0.0

Contributing

Fork the repo.

Create a feature branch: git checkout -b feature/YourFeature

Commit changes: git commit -m "Add YourFeature"

Push to branch: git push origin feature/YourFeature

Open a Pull Request.

License

Distributed under the MIT License. See LICENSE for details.

Made with ❤️ by Lucas Yepez for secure, scalable, real-time communication.


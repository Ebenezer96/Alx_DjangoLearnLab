
# Social Media API

A Django REST Framework-based API for a social media platform. This project provides endpoints for user authentication, posts, comments, likes, and user interactions.

## Features

- User authentication and profile management
- Create, read, update, and delete posts
- Comment on posts
- Like/unlike posts and comments
- Follow/unfollow users
- User feed
- Token-based authentication

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Usage

Access the API at `http://localhost:8000/api/`

## Project Structure

```
social_media_api/
├── manage.py
├── requirements.txt
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```

## License

MIT License

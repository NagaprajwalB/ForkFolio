# 🍴 ForkFolio — Recipe Sharing App

A full-featured recipe sharing platform built with Python & Django.

## Features

- 👤 User registration, login & profiles
- 📝 Create, edit, delete recipes with photos
- 🧂 Ingredient lists with quantity & units
- 📋 Step-by-step cooking instructions
- 🔍 Search by title, description, or ingredient
- 🏷️ Filter by category, difficulty, and max cook time
- ⭐ Star ratings (1–5) with written reviews
- 🗂️ Admin panel for full content management

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed sample data (optional)
```bash
python manage.py seed_data
```
This creates:
- 8 categories (Italian, Indian, Breakfast, Desserts, etc.)
- 4 sample recipes with ingredients & steps
- Demo user: `chef_demo` / `demo1234`

### 4. Create admin superuser
```bash
python manage.py createsuperuser
```

### 5. Run the server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**
Admin: **http://127.0.0.1:8000/admin**

## Project Structure

```
recipe_project/
├── recipe_project/        # Django project settings
│   ├── settings.py
│   └── urls.py
├── recipes/               # Main app
│   ├── models.py          # Category, Recipe, Ingredient, Step, Rating
│   ├── views.py           # All views
│   ├── forms.py           # Forms & formsets
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin config
│   └── management/
│       └── commands/
│           └── seed_data.py
├── templates/
│   └── recipes/           # All HTML templates
├── static/                # CSS / JS / images
├── media/                 # User-uploaded photos
├── requirements.txt
└── README.md
```

## URL Routes

| URL | View |
|-----|------|
| `/` | Home page |
| `/recipes/` | Browse all recipes |
| `/recipes/create/` | Create new recipe |
| `/recipes/<slug>/` | Recipe detail |
| `/recipes/<slug>/edit/` | Edit recipe |
| `/recipes/<slug>/delete/` | Delete recipe |
| `/profile/<username>/` | User profile |
| `/register/` | Register |
| `/login/` | Login |
| `/logout/` | Logout |
| `/admin/` | Admin panel |

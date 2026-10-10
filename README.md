<div align="center">

# 🛍️ JU Creator's Hub

### Student-Powered E-Commerce Platform

*A Django-based marketplace helping student entrepreneurs showcase products and connect with buyers in the Jahangirnagar University community.*

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Framework-092E20?logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Markup-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)

</div>

---

## 🌱 About the Project

**JU Creator's Hub** is a web-based e-commerce platform designed to support student-run businesses at Jahangirnagar University. It gives student entrepreneurs a central place to display products, manage listings, and handle customer orders, while buyers can discover products and shop through a simple interface.

## ✨ Key Features

| 🛒 Buyer | 🏪 Seller | ⚙️ Administration |
|---|---|---|
| Browse products and view details | Create and manage product listings | Manage application data through Django Admin |
| Search for products | Add product images, prices, and descriptions | Oversee registered users and records |
| Add items to a shopping cart | View incoming orders and order items | Manage records according to configured permissions |
| Place orders and review order history | Approve or reject order requests | |

## 🧰 Tech Stack

- **Backend:** Python, Django
- **Frontend:** Django Templates, HTML, CSS, JavaScript
- **Database:** SQLite (default development configuration)
- **Authentication:** Django authentication system
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
my_app/
├── .gitignore
├── README.md
└── creatorhub/
    ├── manage.py
    ├── creatorhub/        # Django project settings and URL configuration
    ├── ecommerce/         # Main e-commerce application
    │   ├── migrations/
    │   ├── templates/
    │   ├── models.py
    │   ├── forms.py
    │   ├── views.py
    │   └── urls.py
    └── assets/            # Static and product-related assets
```

> The structure above is a high-level overview. Exact files and directories may vary by branch or local setup.

## 🚀 Getting Started

### Prerequisites

- Python installed on your computer
- `pip`
- Git

### 1. Clone the repository

```bash
git clone https://github.com/cometkhadija/my_app.git
cd my_app/creatorhub
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the project's required packages, including Django and Pillow if image fields are used:

```bash
python -m pip install Django Pillow
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. The Django admin page is available at **http://127.0.0.1:8000/admin/**.

## 🔐 Security Notes

This project is intended for development use unless configured otherwise. Before deployment:

- Keep `SECRET_KEY` out of source control and load it from an environment variable.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` for the deployment environment.
- Configure HTTPS, secure cookies, and trusted CSRF origins as appropriate.
- Avoid committing virtual environments, private data, or local database files containing sensitive information.
- Follow the [Django deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).

## 🛠️ Future Improvements

- Automated tests for buyer and seller workflows
- Improved product filtering and seller analytics
- Buyer–seller messaging
- Product ratings and reviews
- Payment integration and deployment setup


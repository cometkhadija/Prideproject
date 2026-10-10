# JU Creator's Hub — Student-Powered E-Commerce

**JU Creator's Hub** is a Django-based e-commerce web application designed to help student entrepreneurs at Jahangirnagar University showcase and sell their products through a shared online platform. It connects buyers with student-run shops and provides basic tools for product discovery, cart management, order placement, and seller-side order handling.

> **Project type:** Academic web development project  
> **Backend:** Python / Django  
> **Frontend:** Django Templates, HTML, CSS, JavaScript  
> **Database:** SQLite (configured by default)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [User Roles](#user-roles)
- [Security Notes](#security-notes)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

## Overview

Small student-led businesses often have limited access to a dedicated online storefront. JU Creator's Hub aims to provide a centralized digital space where students can list products, manage inventory, receive orders, and reach customers within and around the university community.

The application supports product categories such as food, clothing, jewellery, and art. Its role-based experience separates buyer activities from seller tools and administrative management.

## Key Features

### Buyer

- Browse product listings and category pages.
- View product details, descriptions, prices, and images.
- Search for products by keyword.
- Add products to a shopping cart and update quantities.
- Proceed through checkout and submit order information.
- View order history and order details.
- Access account information and relevant store policies.

### Seller

- Register and access a seller account.
- Add, edit, and remove product listings.
- Manage product descriptions, images, prices, and categories.
- View products associated with the seller account.
- Review incoming orders and approve or reject individual order items.
- Access seller dashboard and account pages.

### Administrator

- Use Django's admin interface to manage application data.
- Oversee user accounts, product listings, and orders.
- Support moderation and general platform administration.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django 5.2 |
| Frontend | HTML, CSS, JavaScript, Django Templates |
| Database | SQLite by default |
| Authentication | Django built-in authentication |
| Media | Django media handling for product images |
| Version control | Git and GitHub |

## Project Structure

```text
Prideproject/
├── creatorhub/
│   ├── creatorhub/          # Django project settings and URL configuration
│   ├── ecommerce/           # Main application: models, views, forms, URLs, templates
│   │   ├── migrations/      # Database migrations
│   │   └── templates/       # HTML templates
│   ├── assets/              # Project image assets
│   ├── media/               # Uploaded/product media used by the project
│   ├── manage.py            # Django management utility
│   └── db.sqlite3           # Local development database, if present
└── README.md
```

## Getting Started

Follow these instructions to run the project locally. The commands below assume that Python is installed and that you are running commands from the repository root.

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_FOLDER>
```

Replace the placeholders with your Git repository URL and folder name.

### 2. Open the Django project directory

```bash
cd creatorhub
```

### 3. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

The repository does not currently include a project-level `requirements.txt`. Install the core packages in your activated environment:

```bash
python -m pip install "Django>=5.2,<5.3" Pillow
```

`Pillow` is needed for Django image-field support. If additional packages are introduced, record them in a `requirements.txt` file so other developers can reproduce the environment.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to set the administrator username and password.

### 7. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser. The Django admin site is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Usage

1. Open the home page and browse available products.
2. Register or log in to access account-specific features.
3. Buyers can add products to the cart and place orders through the checkout flow.
4. Sellers can manage product listings and review incoming order items from seller pages.
5. Administrators can use the Django admin site for administrative tasks.

Exact page access depends on the account role and the current application configuration.

## User Roles

- **Buyer:** Discovers products, manages a cart, and places and reviews orders.
- **Seller:** Maintains product listings and handles incoming order items.
- **Admin:** Oversees users and application records through administrative tools.

## Security Notes

This repository is configured for local development. Before deploying it publicly:

- Move `SECRET_KEY` out of source code and load it from an environment variable.
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` appropriately.
- Configure HTTPS, secure cookies, and production-ready static/media file handling.
- Do not commit local databases, virtual environments, uploaded private data, or secrets to version control.
- Review Django's deployment checklist: https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

The current project settings include development-oriented configuration, so do not deploy them unchanged to a production server.

## Future Enhancements

Potential extensions include product ratings and reviews, wishlist functionality, promotional coupons, seller analytics, buyer–seller messaging, and deployment for broader use across university communities.



## License

No license file was found in the provided project archive. Unless a license is added, reuse and redistribution permissions are not explicitly granted. Add a `LICENSE` file if you intend to publish the project for open-source use.

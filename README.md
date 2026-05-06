# 🛒 Django Full-Stack E-Commerce Platform


## 📖 Overview
A complete, scalable, and responsive full-stack with two ready templates to show that I can work with any templates and cooperate with front-end developers (as a Full-stack developer). Online shop built from the ground up using Django and JavaScript. This project handles the entire e-commerce lifecycle, from product browsing and shopping carts to custom user authentication and a custom administrative dashboard and ALSO the payment page. 

## ✨ Key Features
*   **Custom Admin Dashboard:** A dedicated, secure panel (`admin_dashboard`) for managing products, articles, and users.
*   **Advanced Product Management:** Includes product galleries, brand filtering, categories, and visit tracking (`product_module`).
*   **User Panel & Authentication:** Secure registration, login, profile editing, and password recovery (`account_module`, `user_panel_module`).
*   **Shopping Cart & Orders:** Full cart functionality, order tracking, and payment result handling (`order_module`).
*   **Content Management:** Integrated article/blog system with commenting functionality (`article_module`).
*   **Multi-Language Support:** Fully localized for English, Italian, and Persian (`en`, `it`, `fa` locales).

## 🛠️ Tech Stack
*   **Backend:** Python 3, Django
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
*   **Database:** SQLite (Development) 
*   **Version Control:** Git & GitHub
> **Architecture Note:** This project is intentionally built using Django's native **MVT (Model-View-Template)** architecture for rapid server-side rendering. It does ***not*** use Django REST Framework (DRF), demonstrating a deep, focused understanding of core Django forms, sessions, context processors, and template inheritance.


## 🚀 Local Installation Setup
You can run this project locally using either standard Python/Virtual Environments or using Docker (Recommended).

### Option A: Using Docker (Recommended)
This project is fully containerized for easy deployment. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aleffeyn/E-Commerce-Website-Django-JS.git](https://github.com/aleffeyn/E-Commerce-Website-Django-JS.git)
   cd E-Commerce-Website-Django-JS
2. **Set up Environment Variables:**

   Create a `.env` file in the root directory and add your keys (e.g., `SECRET_KEY=your_secret_key`).


3. **Build and Run the Container:**
   ```bash
   docker-compose up --build
   ```
   The server will now be running at `http://localhost:8000`. Because the local volume is mapped, any code changes you make will instantly sync to the container, and your local `db.sqlite3` database will be preserved.

### Option B: Standard Python Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/aleffeyn/E-Commerce-Website-Django-JS.git
   cd E-Commerce-Website-Django-JS

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Environment Variables:**
   * Create a `.env` file in the root directory.
   * Add your secure keys (e.g., `SECRET_KEY=your_secret_key`, `DEBUG=True`).
   
   
5. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   
## ☁️ Enterprise Deployment (Kubernetes)
This repository includes production-ready Kubernetes manifests. The `/k8s` directory contains the Deployment and LoadBalancer Service configurations designed for high availability. Note: The current replicas are set to `1` to maintain SQLite database integrity; for horizontal scaling, the database should be migrated to **PostgreSQL**.  
## 📧 Email Configuration (Account Activation & Password Recovery)

This project features a fully functioning email system that sends automated emails for account activation links and password reset requests. To test these features locally, you must configure an SMTP email backend (like a Gmail account) using environment variables.

**1. Generate an App Password (if using Gmail)**
If you are using a standard Gmail account to send these emails, regular passwords will not work due to security restrictions. You must enable 2-Step Verification on your Google account and generate an **App Password**. 

**2. Update your `.env` file**
Add the following variables to your `.env` file, replacing the placeholder values with your actual email credentials:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_digit_app_password
```

***3. How the Logic Works***
The project uses the Django SMTP backend to send emails.
The project's `settings.py` is already configured to securely read these credentials from your `.env` file. When a user registers or requests a password reset, the `utils/email_service.py` module automatically generates an HTML email using the templates located in the `templates/emails/` directory and sends it via this SMTP connection.

_Note: If you are testing offline and do not want to set up an actual email account, you can temporarily change the email backend in `settings.py` to print emails directly to your terminal:
`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`_

## ⚖️ License & Copyright
**© 2026 Hossein Shahamatjou. All Rights Reserved.**



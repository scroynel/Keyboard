# ⌨️ Keyboard Project

**Keyboard** is a full-stack web application designed to manage an online keyboard-related platform.  
The project includes product management, user authentication, shopping cart functionality, and order processing.

## 🚀 Features

- 🛒 Product catalog and shopping cart
- 👤 User registration and authentication
- 📦 Order creation and management
- 💳 Basic payment workflow
- 🧩 Modular and scalable architecture
- 🐳 Docker support for easy deployment

## 🧠 Technology Stack

- **Backend:** Python (Django)
- **Frontend:** HTML, CSS, Tailwind, JavaScript
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose
- **Templates & Static Files:** Django Templates

## 📁 Project Structure

```bash
Keyboard/
├── cart/ # Shopping cart logic
├── keyboard/ # Core Django project settings and configuration
├── keyboard_postgres_db/ # PostgreSQL database configuration
├── orders/ # Order creation and management
├── payments/ # Payment processing module
├── users/ # User authentication and profiles
├── wishlist/ # Wishlist functionality
├── static/ # Static assets (CSS, JavaScript, images)
├── templates/ # HTML templates
├── theme/ # Frontend theme and UI components
├── Dockerfile # Docker image configuration
├── docker-compose.yml # Docker Compose setup
├── manage.py # Django project entry point
├── requirements.txt # Python dependencies
└── package.json # Frontend dependencies
```

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/scroynel/Keyboard.git
```

```bash
cd Keyboard
```

### 2️⃣ Create .env file with own data

```bash
POSTGRES_USER = user_name
POSTGRES_DB = db_name
POSTGRES_PASSWORD = db_password
DB_HOST = db
DB_PORT = 5432


# Stripe keys
STRIPE_SECRET_KEY = sk_test_key
STRIPE_PUBLIC_KEY = pk_test_key
STRIPE_WEBHOOK_SECRET = whsec_key
```

### 3️⃣ Docker Build → Create → Run

```bash
docker compose up --build
```

### 4️⃣ Login to Stripe

```bash
stripe login
```

### 5️⃣ Start listening for events

```bash
stripe listen --forward-to localhost:8000/payments/webhook/
```

### 6️⃣ Create a super user to enter to admin panel

```bash
docker exec -it django_keyboard python manage.py createsuperuser
```

### 7️⃣ Open your browser and go to:

👉 http://localhost:8000/

🤝 Contributing
Contributions are welcome!
Feel free to open issues or submit pull requests.

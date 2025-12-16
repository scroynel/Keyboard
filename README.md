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
cd Keyboard
```

### 2️⃣ Create virtual environment

python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows

### 3️⃣ Install dependencies

pip install -r requirements.txt

### 4️⃣ Run migrations

python manage.py migrate

### 5️⃣ Start development server

python manage.py runserver
Open your browser and go to:
👉 http://127.0.0.1:8000/

🐳 Docker (Optional)
docker compose up --build

🤝 Contributing
Contributions are welcome!
Feel free to open issues or submit pull requests.

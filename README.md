# 🏋️‍♂️ Hypertrophy Predictor

An intelligent, data-driven web application designed to optimize bodybuilding routines, caloric intake, and progressive overload tracking for aesthetic physique development. Built with a robust Python backend and deployed natively on AWS infrastructure.

## 🚀 Features
* **Data-Driven Analytics:** Employs [Scikit-Learn/Pandas] to analyze workout splits and macronutrient profiles.
* **Custom Modeling:** Tailored recommendations for specific hypertrophy protocols (e.g., Arnold split, PPL).
* **Secure Infrastructure:** Production-grade deployment using Gunicorn and Nginx as a reverse proxy.
* **Scalable Database:** Integrated with [MySQL/PostgreSQL] for reliable user data and progression tracking.

## 🛠️ Tech Stack
* **Backend:** Python 3.14, Django 6.0
* **Data Science:** Pandas, Scikit-Learn, NumPy
* **Database:** [MySQL / PostgreSQL]
* **Infrastructure:** AWS EC2 (Ubuntu 24.04), Gunicorn, Nginx
* **Security:** Let's Encrypt SSL/TLS, UFW Firewall

## ⚙️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/Hypertrophy-Predictor.git](https://github.com/YourUsername/Hypertrophy-Predictor.git)
   cd Hypertrophy-Predictor
Create and activate a virtual environment:

Bash


python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install dependencies:

Bash


pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and add your local database credentials and Django secret key.

Run Database Migrations:

Bash


python manage.py migrate
Start the local server:

Bash


python manage.py runserver
☁️ Cloud Architecture & Deployment
This application is fully containerized and hosted on AWS. The deployment pipeline consists of:

EC2 Instance: Ubuntu environment utilizing NVMe SSD storage.

Gunicorn Daemon: A custom systemd service running the Django WSGI application asynchronously.

Nginx Reverse Proxy: Securely routes port 80/443 traffic to the internal Unix socket, handling static file serving and SSL termination.

🤝 Contact
Created by www.linkedin.com/in/sairaj-patil-717a65258


# 🔐 SecureAuth

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-black?logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-purple?logo=bootstrap)
![Security](https://img.shields.io/badge/Security-SQL_Injection%20%7C%20XSS-orange)
![License](https://img.shields.io/badge/Project-PAP-green)

SecureAuth is a web application developed as part of the **Professional Aptitude Project (PAP)** for the **Computer Equipment Management Technician** course.

The project demonstrates the difference between a **vulnerable authentication system** and a **secure authentication system**, focusing on common web security vulnerabilities such as **SQL Injection** and **Cross‑Site Scripting (XSS)**.

---

# 📌 Project Overview

Modern web applications store sensitive data such as login credentials and personal information.  
However, improper handling of user input can introduce vulnerabilities.

This project demonstrates:

- A **vulnerable login system**
- A **secure login system**
- **SQL Injection authentication bypass**
- A scenario where **SQL Injection leads to XSS**

The objective is to show how poor coding practices can compromise a system and how secure development techniques can prevent these attacks.

---

# ⚙️ Technologies Used

### Frontend
- HTML
- Bootstrap

### Backend
- Python
- Flask

### Database
- SQLAlchemy

Flask handles the web server and application logic, while SQLAlchemy manages database interaction.

---

# 🏗️ System Architecture

The application follows a **Client–Server architecture**.

```
User (Browser)
      │
      ▼
Flask Web Server
      │
      ▼
Database (SQLAlchemy)
```

The user sends HTTP requests to the Flask server, which processes the request and communicates with the database before returning a response.

---

# 🔑 Authentication Flow

The login system can be represented by a simple **state machine**:

1. **Initial State**
   - User accesses the login page

2. **Validation State**
   - Server checks credentials

3. **Authenticated State**
   - Access to dashboard granted

4. **Error State**
   - Invalid credentials or blocked attack

In the vulnerable system, manipulated input may force authentication even without valid credentials.

---

# 💥 Security Demonstrations

## SQL Injection

SQL Injection occurs when user input is directly inserted into an SQL query.

Example attack:

```
' OR '1'='1
```

This makes the SQL condition always true and allows authentication bypass.

---

## SQL Injection Leading to XSS

The project also demonstrates a scenario where SQL Injection injects malicious HTML/JavaScript into the page.

Example payload:

```
' UNION SELECT '1','<script>alert("XSS")</script>','3' --
```

Possible consequences:

- JavaScript execution in the user's browser
- Cookie or session theft
- Malicious redirections
- Actions performed on behalf of the user

---

# 🧪 Testing

The project includes several types of testing:

- Functional tests
- Security tests
- Comparison between vulnerable and secure systems

These tests demonstrate how the secure implementation prevents SQL Injection.

---

# 🚀 Possible Improvements

Future improvements could include:

- Password hashing
- Login attempt rate limiting
- Multi‑factor authentication

---

# 📚 Learning Outcomes

This project demonstrates that small programming mistakes can lead to serious security vulnerabilities.

By applying secure practices such as:

- Parameterized queries
- Input validation
- Secure data handling

developers can significantly reduce the risk of exploitation.

---

# 👨‍💻 Author

**Diogo Manuel Vieira Dos Santos**

Miguel Torga Secondary School

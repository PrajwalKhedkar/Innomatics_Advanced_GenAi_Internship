# 🎬 Movie Ticket Booking System (FastAPI)

## 🚀 Project Overview

This project is a backend system built using **FastAPI** that simulates a real-world cinema ticket booking platform. It allows users to browse movies, check seat availability, book tickets, and manage bookings through REST APIs.

---

## ⚙️ Features

### ✅ Core Features

* View all movies with details (price, language, seats)
* Get movie by ID
* Movie summary (price stats, seat count, genre count)

### 🎟️ Booking System

* Book tickets with seat selection
* Seat availability updates dynamically
* Apply promo codes (SAVE10, SAVE20)

### 🔄 Seat Workflow

* Hold seats temporarily
* Confirm booking
* Release held seats

### 🔍 Advanced Features

* Filter movies (genre, language, price, seats)
* Search movies (title, genre, language)
* Sort movies (price, duration, seats)
* Pagination support
* Combined browse API (filter + sort + paginate)

### 📊 Bookings Management

* View all bookings
* Search bookings by customer name
* Sort bookings
* Paginate bookings

---

## 🛠️ Tech Stack

* **FastAPI**
* **Python**
* **Pydantic**
* **Uvicorn**

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run server

```bash
uvicorn main:app --reload
```

### 3. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints (Examples)

* `GET /movies`
* `GET /movies/{movie_id}`
* `GET /movies/filter`
* `POST /bookings`
* `POST /seat-hold`
* `POST /seat-confirm/{hold_id}`
* `DELETE /seat-release/{hold_id}`
* `GET /movies/search`
* `GET /movies/browse`

---

## 💡 Learning Outcomes

* Built REST APIs using FastAPI
* Implemented real-world workflows (Hold → Confirm → Release)
* Applied validation using Pydantic
* Learned search, sorting, and pagination logic
* Designed scalable backend architecture

---

## 📎 GitHub Repository

[Add your GitHub link here]

---

## 🙏 Acknowledgement

Thanks to **Innomatics Research Labs** for the guidance and learning opportunity.

---

## 📌 Author

**Prajwal Khedkar**

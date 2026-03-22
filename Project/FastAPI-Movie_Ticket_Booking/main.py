from fastapi import FastAPI, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
import math

app=FastAPI()


#==================DATA=====================
movies = [
    {"id": 1, "title": "Avengers Doomsday", "genre": "Action", "language": "English", "duration_mins": 150, "ticket_price": 550, "seats_available": 120},
    {"id": 2, "title": "The Batman 2", "genre": "Action", "language": "English", "duration_mins": 140, "ticket_price": 300, "seats_available": 0},
    {"id": 3, "title": "Dune: Part Three", "genre": "Drama", "language": "English", "duration_mins": 155, "ticket_price": 400, "seats_available": 0},
    {"id": 4, "title": "Avatar 3", "genre": "Action", "language": "English", "duration_mins": 160, "ticket_price": 450, "seats_available": 90},
    {"id": 5, "title": "Spider-Man: Brand New Day", "genre": "Comedy", "language": "English", "duration_mins": 130, "ticket_price": 350, "seats_available": 110},
    {"id": 6, "title": "Ramayana: Part 1", "genre": "Drama", "language": "Hindi", "duration_mins": 170, "ticket_price": 500, "seats_available": 95},
    {"id": 7, "title": "Kantara: Chapter 1", "genre": "Action", "language": "Kannada", "duration_mins": 145, "ticket_price": 320, "seats_available": 100},
    {"id": 8, "title": "War 2", "genre": "Action", "language": "Hindi", "duration_mins": 150, "ticket_price": 420, "seats_available": 105},
    {"id": 9, "title": "Toxic", "genre": "Drama", "language": "Hindi", "duration_mins": 140, "ticket_price": 380, "seats_available": 0},
    {"id": 10, "title": "Dhurandhar", "genre": "Action", "language": "Hindi", "duration_mins": 150, "ticket_price": 500, "seats_available": 115}
]

bookings = []
booking_counter = 1
holds = []
hold_counter = 1

# ================= HELPERS =================
def find_movie(movie_id):
    for m in movies:
        if m["id"] == movie_id:
            return m
    return None

def calculate_ticket_cost(price, seats, seat_type, promo_code=""):
    multiplier = 1
    if seat_type == "premium":
        multiplier = 1.5
    elif seat_type == "recliner":
        multiplier = 2

    original = price * seats * multiplier
    discount = 0
    if promo_code == "SAVE10":
        discount = 0.1
    elif promo_code == "SAVE20":
        discount = 0.2

    final = original * (1 - discount)

    return original, final

def filter_movies_logic(genre, language, max_price, min_seats):
    result = movies

    if genre is not None:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if language is not None:
        result = [m for m in result if m["language"].lower() == language.lower()]
    if max_price is not None:
        result = [m for m in result if m["ticket_price"] <= max_price]
    if min_seats is not None:
        result = [m for m in result if m["seats_available"] >= min_seats]

    return result

# ================= DAY 1 =================
@app.get("/")
def home():
    return {"message": "Welcome to Moctale Booking"}

@app.get("/movies")
def get_movies():
    return {
        "total_movies": len(movies),
        "total_seats_available": sum(m["seats_available"] for m in movies),
        "movies": movies
    }

@app.get("/movies/summary")
def summary():
    prices = [m["ticket_price"] for m in movies]
    genre_count = {}
    for m in movies:
        genre_count[m["genre"]] = genre_count.get(m["genre"], 0) + 1
    return {
        "total_movies": len(movies),
        "most_expensive_ticket": max(prices),
        "cheapest_ticket": min(prices),
        "total_seats": sum(m["seats_available"] for m in movies),
        "movies_by_genre": genre_count
    }



@app.get("/bookings")
def get_bookings():
    return {
        "total_bookings": len(bookings),
        "total_revenue": sum(b["total_cost"] for b in bookings) if bookings else 0,
        "bookings": bookings
    }

# ================= DAY 2 =================
class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    movie_id: int = Field(gt=0)
    seats: int = Field(gt=0, le=10)
    phone: str = Field(min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

# ================= DAY 3 =================
@app.post("/bookings")
def create_booking(req: BookingRequest):
    global booking_counter

    movie = find_movie(req.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if movie["seats_available"] < req.seats:
        raise HTTPException(400, "Not enough seats")

    original, final = calculate_ticket_cost(
        movie["ticket_price"], req.seats, req.seat_type, req.promo_code
    )

    movie["seats_available"] -= req.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": req.customer_name,
        "movie": movie["title"],
        "seats": req.seats,
        "seat_type": req.seat_type,
        "original_cost": original,
        "total_cost": final
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

@app.get("/movies/filter")
def filter_movies(
    genre: Optional[str] = None,
    language: Optional[str] = None,
    max_price: Optional[int] = None,
    min_seats: Optional[int] = None
):
    data = filter_movies_logic(genre, language, max_price, min_seats)
    return {"count": len(data), "movies": data}

# ================= DAY 4 =================
class NewMovie(BaseModel):
    title: str = Field(min_length=2)
    genre: str = Field(min_length=2)
    language: str = Field(min_length=2)
    duration_mins: int = Field(gt=0)
    ticket_price: int = Field(gt=0)
    seats_available: int = Field(gt=0)

@app.post("/movies", status_code=201)
def add_movie(movie: NewMovie):
    for m in movies:
        if m["title"].lower() == movie.title.lower():
            raise HTTPException(400, "Duplicate movie")

    new = movie.dict()
    new["id"] = len(movies) + 1
    movies.append(new)
    return new

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, ticket_price: Optional[int] = None, seats_available: Optional[int] = None):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if ticket_price is not None:
        movie["ticket_price"] = ticket_price
    if seats_available is not None:
        movie["seats_available"] = seats_available

    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    for b in bookings:
        if b["movie"] == movie["title"]:
            raise HTTPException(400, "Cannot delete movie with bookings")

    movies.remove(movie)
    return {"message": "Deleted"}




# ================= DAY 5 =================
class HoldRequest(BaseModel):
    customer_name: str
    movie_id: int
    seats: int

@app.post("/seat-hold")
def hold_seat(req: HoldRequest):
    global hold_counter

    movie = find_movie(req.movie_id)
    if not movie or movie["seats_available"] < req.seats:
        raise HTTPException(400, "Not enough seats")

    movie["seats_available"] -= req.seats

    hold = {
        "hold_id": hold_counter,
        "customer_name": req.customer_name,
        "movie_id": req.movie_id,
        "seats": req.seats
    }

    holds.append(hold)
    hold_counter += 1

    return hold

@app.get("/seat-hold")
def get_holds():
    return holds
@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter

    for h in holds:
        if h["hold_id"] == hold_id:
            movie = find_movie(h["movie_id"])

            if not movie:
                raise HTTPException(status_code=404, detail="Movie not found")

            booking = {
                "booking_id": booking_counter,
                "customer_name": h["customer_name"],
                "movie": movie["title"],
                "seats": h["seats"],
                "total_cost": movie["ticket_price"] * h["seats"]
            }

            bookings.append(booking)
            holds.remove(h)
            booking_counter += 1

            return booking

    raise HTTPException(status_code=404, detail="Hold not found")


@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    for h in holds:
        if h["hold_id"] == hold_id:
            movie = find_movie(h["movie_id"])

            if not movie:
                raise HTTPException(status_code=404, detail="Movie not found")

            movie["seats_available"] += h["seats"]
            holds.remove(h)

            return {"message": "Released successfully"}

    raise HTTPException(status_code=404, detail="Hold not found")

# ================= DAY 6 =================
@app.get("/movies/search")
def search(keyword: str):
    result = [m for m in movies if keyword.lower() in m["title"].lower() or keyword.lower() in m["genre"].lower() or keyword.lower() in m["language"].lower()]
    if not result:
        return {"message": "No results"}
    return {"total_found": len(result), "data": result}

@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):
    if sort_by not in ["ticket_price", "title", "duration_mins", "seats_available"]:
        raise HTTPException(400, "Invalid sort field")

    reverse = True if order == "desc" else False
    return sorted(movies, key=lambda x: x[sort_by], reverse=reverse)

@app.get("/movies/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {
        "total": len(movies),
        "total_pages": math.ceil(len(movies)/limit),
        "data": movies[start:start+limit]
    }

@app.get("/bookings/search")
def search_booking(name: str):
    return [b for b in bookings if name.lower() in b["customer_name"].lower()]

@app.get("/bookings/sort")
def sort_booking(order: str = "asc"):
    return sorted(bookings, key=lambda x: x["total_cost"], reverse=(order=="desc"))

@app.get("/bookings/page")
def paginate_booking(page: int = 1, limit: int = 2):
    start = (page-1)*limit
    return bookings[start:start+limit]

@app.get("/movies/browse")
def browse(
    keyword: Optional[str] = None,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    data = movies

    if keyword:
        data = [m for m in data if keyword.lower() in m["title"].lower()]
    if genre:
        data = [m for m in data if m["genre"].lower() == genre.lower()]
    if language:
        data = [m for m in data if m["language"].lower() == language.lower()]

    reverse = True if order == "desc" else False
    data = sorted(data, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    return {
        "total": len(data),
        "page": page,
        "data": data[start:start+limit]
    }




@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")
    return movie

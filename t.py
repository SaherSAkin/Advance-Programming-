from io import BytesIO
import requests
import tkinter as tk
import pygame
from tkinter import messagebox
from PIL import Image, ImageTk

pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("game-music.mp3")
pygame.mixer.music.play(-1)

def show_no_results_message():
    messagebox.showinfo("No Results Found", "Sorry, no results found for your query.")


def fetch_and_display_poster(poster_path, label):
    if poster_path:
        try:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            poster_data = requests.get(poster_url, timeout=10).content
            poster_image = Image.open(BytesIO(poster_data))
            poster_image.thumbnail((250, 375)) 
            poster_photo = ImageTk.PhotoImage(poster_image)
            
            label.config(image=poster_photo, text="")
            label.image = poster_photo
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            label.config(text="Failed to load poster", image="")
        except Exception as e:
            print(f"Error loading poster: {e}")
            label.config(text="Error loading poster", image="")
    else:
        label.config(text="No Poster Available", image="")


def search_movie():
    api_key = "b4dcb8296c5a74dac1ebd2d9174658d6"
    movie_name = movie_entry.get()
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if not data.get("results"):
            show_no_results_message()
        else:
            movie = data["results"][0]
            title_label.config(text="Title: " + movie.get("title", "N/A"))
            year_label.config(text="Release Date: " + movie.get("release_date", "N/A"))
            genre_label.config(text="Average Rating: " + str(movie.get("vote_average", "N/A")))

            plot_text.delete(1.0, tk.END)
            plot_text.insert(tk.END, "Overview: " + movie.get("overview", "N/A"))

            fetch_and_display_poster(movie.get("poster_path"), poster_label)
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        messagebox.showinfo("Error", "An error occurred while fetching movie details.")


def search_tv_show():
    api_key = "b4dcb8296c5a74dac1ebd2d9174658d6"
    tv_show_name = movie_entry.get()
    url = f"https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={tv_show_name}"

    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if not data.get("results"):
            show_no_results_message()
        else:
            tv_show = data["results"][0]
            title_label.config(text="Title: " + tv_show.get("name", "N/A"))
            year_label.config(text="First Air Date: " + tv_show.get("first_air_date", "N/A"))
            genre_label.config(text="Average Rating: " + str(tv_show.get("vote_average", "N/A")))

            plot_text.delete(1.0, tk.END)
            plot_text.insert(tk.END, "Overview: " + tv_show.get("overview", "N/A"))

            fetch_and_display_poster(tv_show.get("poster_path"), poster_label)
    except Exception as e:
        print(f"Error fetching TV show details: {e}")
        messagebox.showinfo("Error", "An error occurred while fetching TV show details.")


def search_person():
    api_key = "b4dcb8296c5a74dac1ebd2d9174658d6"
    person_name = movie_entry.get()
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={person_name}"

    try:
        response = requests.get(url, timeout=30)
        data = response.json()

        if not data.get("results"):
            show_no_results_message()
        else:
            person = data["results"][0]
            title_label.config(text="Name: " + person.get("name", "N/A"))
            
            known_for = person.get("known_for", [])
            known_titles = [item.get('title', item.get('name')) for item in known_for]
            year_label.config(text="Known For: " + ", ".join(known_titles))

            genre_label.config(text="Popularity: " + str(person.get("popularity", "N/A")))

            plot_text.delete(1.0, tk.END)
            plot_text.insert(tk.END, "Bio information is not available in this search response.")

            fetch_and_display_poster(person.get("profile_path"), poster_label)
    except Exception as e:
        print(f"Error fetching person details: {e}")
        messagebox.showinfo("Error", "An error occurred while fetching person details.")


window = tk.Tk()
window.title("Movie Searcher")
window.geometry("1000x700")
window.configure(bg="#f4f4f9")


heading_label = tk.Label(window, text="Movie Searcher", font=("Segoe UI", 36, 'bold'), bg="#f4f4f9", fg="#333")
heading_label.pack(pady=20)


sidebar_frame = tk.Frame(window, bg="#2E3B55", width=250)
sidebar_frame.pack(side="left", fill="y")  

bg_image_url = "https://img.freepik.com/free-photo/education-day-scene-fantasy-style-aesthetic_23-2151040233.jpg?semt=ais_hybrid"  # Replace with your image URL

response = requests.get(bg_image_url, timeout=30)
bg_image_data = response.content if response.status_code == 200 else None
if not bg_image_data:
    print("Failed to fetch image.")
bg_image = Image.open(BytesIO(bg_image_data)) if bg_image_data else Image.new("RGB", (250, 700))
bg_image = bg_image.resize((250, 700)) 
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(sidebar_frame, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

sidebar_label = tk.Label(sidebar_frame, text="Search Options", font=("Arial", 18, "bold"), fg="white", bg="#2E3B55")
sidebar_label.pack(pady=20)

movie_button = tk.Button(sidebar_frame, text="Search Movie", font=("Arial", 14), command=search_movie, bg="#5e81ac", fg="white")
movie_button.pack(fill="x", padx=20, pady=5)

tv_show_button = tk.Button(sidebar_frame, text="Search TV Show", font=("Arial", 14), command=search_tv_show, bg="#5e81ac", fg="white")
tv_show_button.pack(fill="x", padx=20, pady=5)

person_button = tk.Button(sidebar_frame, text="Search Person", font=("Arial", 14), command=search_person, bg="#5e81ac", fg="white")
person_button.pack(fill="x", padx=20, pady=5)

entry_frame = tk.Frame(window, bg="#f4f4f9")
entry_frame.pack(pady=15)

tk.Label(entry_frame, text="Enter Search Query:", font=("Arial", 24), bg="#f4f4f9", fg="#333").pack(side="left", padx=5)
movie_entry = tk.Entry(entry_frame, width=40, font=("Arial", 18), relief="solid", bd=2, highlightthickness=1, highlightbackground="#ccc")
movie_entry.pack(side="left", padx=10)
search_button = tk.Button(entry_frame, text="Search", font=("Arial", 18), bg="#5e81ac", fg="white", relief="solid", command=search_movie)
search_button.pack(side="left", padx=5)

content_frame = tk.Frame(window, bg="#f4f4f9")
content_frame.pack(fill="both", expand=True, padx=20, pady=10)

content_frame.grid_columnconfigure(0, weight=1) 
content_frame.grid_columnconfigure(1, weight=2) 

poster_label = tk.Label(content_frame, text="Poster", font=("Arial", 14), bg="#f4f4f9", width=300, height=250)
poster_label.grid(row=0, column=0, rowspan=4, padx=20, pady=10) 

details_frame = tk.Frame(content_frame, bg="#f4f4f9")
details_frame.grid(row=0, column=1, sticky="nw", padx=20, pady=10)

title_label = tk.Label(details_frame, text="Title: N/A", font=("Arial", 16), bg="#f4f4f9")
title_label.pack(anchor="w", pady=2)

year_label = tk.Label(details_frame, text="Release Date: N/A", font=("Arial", 16), bg="#f4f4f9")
year_label.pack(anchor="w", pady=2)

genre_label = tk.Label(details_frame, text="Average Rating: N/A", font=("Arial", 16), bg="#f4f4f9")
genre_label.pack(anchor="w", pady=2)

plot_text = tk.Text(details_frame, wrap="word", width=50, height=10, font=("Arial", 14), bg="#f9f9f9", relief="solid", bd=1)
plot_text.pack(fill="both", expand=True, pady=10)

window.mainloop()

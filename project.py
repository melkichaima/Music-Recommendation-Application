from auth import get_auth_header
import requests
import json
import tkinter as tk
from tkinter import messagebox  
import webbrowser
import re

base_url = "https://api.spotify.com/v1/"
headers = get_auth_header()



def get_artist_id(artist_names):
    '''Get user fav artist id from spotify'''
    artist_ids = []
    for artist in artist_names:
        query = f"search?q={artist}&type=artist&limit=1"
        try:
            result = requests.get(base_url + query, headers=headers)
        except requests.RequestException:
            messagebox.showerror("ERROR","Request Error! Try again")
        json_result = json.loads(result.content)
        try:
            artist_ids.append(json_result["artists"]["items"][0]["id"])
        except(KeyError):
            if len(artist_ids)>0:
                pass
            messagebox.showinfo("","Provide correct artist names(at most 5) separated with comma")
    artist_id = ",".join(artist_ids)
    return artist_id



def get_recommendations(artist,mood,genre):
    '''gets song recommendations from spotify '''
    if re.search("^[a-zA-Z0-9]+(,?[a-zA-Z0-9])*$",artist):
        ...
    else:
        raise ValueError
    if mood == "happy":
        min_dance,max_dance = 0.6,1.0
        min_energy,max_energy = 0.6,1.0
        min_valence,max_valence = 0.7,1.0

    if mood == "calm":
        min_dance,max_dance = 0.0,0.5
        min_energy,max_energy = 0.0,0.5
        min_valence,max_valence = 0.4,0.8

    if mood == "energetic":
        min_dance,max_dance = 0.7,1.0
        min_energy,max_energy = 0.7,1.0
        min_valence,max_valence = 0.6,1.0

    if mood == "sad":
        min_dance,max_dance = 0,0.4
        min_energy,max_energy = 0,0.4
        min_valence,max_valence = 0.0,0.3
    
    url = (
            base_url
            + f"recommendations?limit=10&market=US&seed_artists={artist}&seed_genres={genre}&min_danceability={min_dance}&max_danceability={max_dance}&min_energy={min_energy}&max_energy={max_energy}&min_popularity=47&min_valence={min_valence}&max_valence={max_valence}"
        )
    try:
        result = requests.get(url,headers=headers)
    except requests.RequestException:
        messagebox.showerror("ERROR","Request Error! Try again")

    json_result = json.loads(result.content)
    tracks =[]
    try:
        for track in json_result["tracks"]:
            name = track["name"]
            track_url = track["external_urls"]['spotify']
            tracks.append({"name":name, "url":track_url})
    except:
        messagebox.showerror("error","Try running again!") 
        
    return tracks

def open_url(url):
    '''Opens the spotify song url in web beowser'''
    if re.search(r"^https?:\/\/open\.spotify\.com\/track\/([a-zA-Z0-9])+$",url):
        webbrowser.open_new(url)
    else:
        raise ValueError

def display_songs():
    '''Display song and url on gui'''

    artist = name_input.get().split(",")
    artist_list = artist[:5]
    #print(artist_list)
    mood = mood_var.get()
    #print(mood)
    genre = [genre_list[i] for i, genre in enumerate(genre_vars) if genre.get() == 1]
    while len(genre)+len(artist_list) > 5:
        genre.pop()
    artist_id = get_artist_id(artist_list)
    #print(genre)
    #print(artist_id)
    songs = get_recommendations(artist_id,mood,",".join(genre))
    for i, song in enumerate(songs):
        url = song['url']
        display_label = tk.Label(root, text=f"{song['name']} : {url}", font=("Helvetica", 12), fg="blue", cursor="hand2")
        display_label.place(x=30, y=320 + i * 30)
        display_label.bind("<Button-1>", lambda e, url=url: open_url(url))



def main():

    global name_input,mood_var,root,genre_vars,genre_list

# GUI 
    root = tk.Tk()

    root.geometry(f"800x650")
    root.title("Spotify Song Recommendation App")

# set background image
    bg_image = tk.PhotoImage(file="app.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create input fields for name
    name_label = tk.Label(root, text="Favrouite Artists :", font=("Helvetica", 12))
    name_label.place(x=50, y=50)
    name_input = tk.Entry(root, font=("Helvetica", 12))
    name_input.place(x=190, y=50)

# Create radio buttons for mood selection
    mood_label = tk.Label(root, text="Mood:", font=("Helvetica", 12))
    mood_label.place(x=50, y=100)
    mood_var = tk.StringVar()
    mood_var.set("happy")
    mood_options = [("Happy", "happy"),("Calm", "calm"),("Energetic","energetic"),("Sad", "sad"),]
    for text, value in mood_options:
        mood_button = tk.Radiobutton(root, text=text, variable=mood_var, value=value)
        mood_button.place(x=120 + 80 * mood_options.index((text, value)), y=100)
    
# Create checkboxes for genre selection
    genre_label = tk.Label(root, text="Genres:", font=("Helvetica", 12))
    genre_label.place(x=50, y=150)
    genre_list = [
        "pop",
        "rock",
        "disco",
        "hip-hop",
        "r-n-b",
        "indie",
        "k-pop",
        "metal",
        "jazz",
        "groove",
        "acoustic",
        "country",
        "anime",
        "edm",
        "romance",
        "electronic",
        "classical",
    ]
    genre_vars = []
    checkboxes = []

    for i, genre in enumerate(genre_list):
        var = tk.IntVar()
        genre_vars.append(var)
        checkbox = tk.Checkbutton(root, text=genre, variable=var)
        checkbox.place(x=120 + (i % 5) * 75, y=150 + (i // 5) * 30)
        checkboxes.append(checkbox)
        
# generate recommendation button
    generate_recommendation = tk.Button(
        root, text="Generate Recommendations", command=display_songs, font=("Helvetica", 12)
    )
    generate_recommendation.place(x=160, y=280)

    root.mainloop()



if __name__ =="__main__":
    main()

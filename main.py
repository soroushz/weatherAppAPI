import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import datetime

# Function to fetch weather data
def get_weather(city):
    api_key = "850fdb8d7f1539d8a526b19bcbcddc4b"  # Replace with your actual API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    return response.json()

# Function to update the weather data in the UI
def update_weather(city):
    if city:
        weather_data = get_weather(city)
        if weather_data['cod'] == 200:
            weather_values = [
                f"{weather_data['main']['temp']} °C",
                f"{weather_data['main']['feels_like']} °C",
                f"{weather_data['main']['pressure']} hPa",
                f"{weather_data['main']['humidity']}%",
                f"{weather_data['wind']['speed']} m/s",
                datetime.datetime.now().strftime("%H:%M:%S")
            ]
            for value_label, value in zip(value_labels, weather_values):
                value_label.config(text=value)
        else:
            messagebox.showerror("Error", "City not found")
    else:
        messagebox.showwarning("Warning", "Please enter a city name")

# Function to handle enter key press
def on_enter(event=None):
    city = city_entry.get()
    update_weather(city)

# Function to handle entry click and focus out for placeholder text
def on_entry_click(event):
    if city_entry.get() == 'Enter city name':
        city_entry.delete(0, "end")
        city_entry.config(fg='#000000')

def on_focusout(event):
    if city_entry.get() == '':
        city_entry.insert(0, 'Enter city name')
        city_entry.config(fg='#808080')

# Create main window
root = tk.Tk()
root.title("Weather App")
root.geometry("610x400")
root.resizable(False, False)
root.configure(bg='#D6EAF8')

# Create a modern styled entry box
entry_frame = tk.Frame(root, bg='#D6EAF8')
entry_frame.pack(pady=20)

city_entry = tk.Entry(entry_frame, font=("Helvetica", 14), bd=0, relief=tk.FLAT, fg="#000000", bg="#AED6F1", insertbackground='#000000')
city_entry.pack(padx=10, pady=10, ipadx=10, ipady=5, fill=tk.X, expand=True)
city_entry.bind("<Return>", on_enter)
city_entry.insert(0, 'Enter city name')
city_entry.bind('<FocusIn>', on_entry_click)
city_entry.bind('<FocusOut>', on_focusout)
city_entry.config(fg='#808080')

entry_frame.pack_propagate(False)
entry_frame.configure(width=300, height=50)

# Add the logo in the middle
logo_frame = tk.Frame(root, bg='#D6EAF8')
logo_frame.pack(pady=20)

logo_image = Image.open("images/weather.png")
logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Resize the logo to be bigger
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(logo_frame, image=logo_photo, bg='#D6EAF8')
logo_label.pack()

# Weather info labels and values
info_frame = tk.Frame(root, bg='#D6EAF8')
info_frame.pack(side=tk.BOTTOM, pady=20)

label_bg = '#AED6F1'
value_bg = '#E8F6F3'

labels = ["Temperature", "Feels Like", "Pressure", "Humidity", "Wind Speed", "Current Time"]
units = ["°C", "°C", "hPa", "%", "m/s", ""]

labels_frame = tk.Frame(info_frame, bg=label_bg)
labels_frame.pack(fill=tk.X)

values_frame = tk.Frame(info_frame, bg=value_bg)
values_frame.pack(fill=tk.X)

label_widgets = []
value_labels = []

for label in labels:
    label_widgets.append(tk.Label(labels_frame, text=label, font=("Helvetica", 12), bg=label_bg, fg='#000000'))
    label_widgets[-1].pack(side=tk.LEFT, padx=10, pady=5, expand=True)

    value_labels.append(tk.Label(values_frame, text="", font=("Helvetica", 12), bg=value_bg, fg='#000000'))
    value_labels[-1].pack(side=tk.LEFT, padx=10, pady=5, expand=True)

# Run the application
root.mainloop()

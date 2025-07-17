import tkinter as tk
from tkinter import messagebox, ttk
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
from PIL import Image, ImageTk
import io

# Color palette
COLORS = {
    "dark_blue": "#1a2b4a",
    "medium_blue": "#2a4b7c",
    "light_blue": "#3a6bac",
    "accent_blue": "#4d8fd1",
    "text_white": "#ffffff",
    "text_light": "#e0e0e0",
    "text_gray": "#b0b0b0",
    "card_bg": "#2a3b5a",
    "highlight": "#5da8ff"
}

def get_weather_icon(icon_code):
    """Fetch weather icon from OpenWeatherMap"""
    try:
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(url, stream=True)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        return ImageTk.PhotoImage(image)
    except:
        # Return a blank image if icon can't be loaded
        blank = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        return ImageTk.PhotoImage(blank)

def create_weather_app():
    root = tk.Tk()
    root.title("BlueSky Weather")
    root.geometry("850x550+300+150")
    root.resizable(False, False)
    root.config(bg=COLORS["dark_blue"])

    # === Weather Data Storage ===
    weather_data = {
        "current": {},
        "forecast": []
    }

    # === UI Elements ===
    def create_gradient(width, height, color1, color2):
        """Create a vertical gradient from color1 to color2"""
        image = Image.new("RGB", (width, height))
        for y in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * y / height)
            g = int(color1[1] + (color2[1] - color1[1]) * y / height)
            b = int(color1[2] + (color2[2] - color1[2]) * y / height)
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        return ImageTk.PhotoImage(image)

    # Convert hex colors to RGB tuples
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    top_color = hex_to_rgb(COLORS["medium_blue"])
    bottom_color = hex_to_rgb(COLORS["dark_blue"])
    gradient = create_gradient(850, 100, top_color, bottom_color)

    # Header with gradient background
    header = tk.Label(root, image=gradient, bg=COLORS["dark_blue"])
    header.image = gradient  # Keep reference
    header.place(x=0, y=0, width=850, height=100)

    # Search section
    search_frame = tk.Frame(root, bg=COLORS["dark_blue"], bd=0, highlightthickness=0)
    search_frame.place(x=50, y=30, width=750, height=40)

    textfield = tk.Entry(search_frame, justify="left", width=25, font=("Arial", 14), 
                        bg=COLORS["card_bg"], fg=COLORS["text_white"], border=0, 
                        insertbackground=COLORS["text_white"])
    textfield.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
    textfield.focus()

    search_icon = tk.PhotoImage(file="Layer 6.png")

    def update_ui():
        """Update the UI with current weather data"""
        current = weather_data["current"]
        
        # Current weather
        temp_label.config(text=f"{current['temp']:.1f}°C")
        desc_label.config(text=current['description'].capitalize())
        
        # Weather details
        detail_labels["humidity"].config(text=f"{current['humidity']}%")
        detail_labels["pressure"].config(text=f"{current['pressure']} hPa")
        detail_labels["wind"].config(text=f"{current['wind_speed']} m/s")
        detail_labels["feels_like"].config(text=f"{current['feels_like']:.1f}°C")
        detail_labels["visibility"].config(text=f"{current['visibility']/1000:.1f} km")
        detail_labels["clouds"].config(text=f"{current['cloudiness']}%")
        
        # Weather icon
        icon_image = get_weather_icon(current['icon'])
        weather_icon.config(image=icon_image)
        weather_icon.image = icon_image
        
        # Forecast
        for i, day_data in enumerate(weather_data["forecast"][:5]):
            card = forecast_cards[i]
            card["day"].config(text=day_data["day"])
            card["date"].config(text=day_data["date"])
            card["temp"].config(text=f"{day_data['temp']:.1f}°C")
            card["desc"].config(text=day_data["description"].capitalize())
            
            icon_image = get_weather_icon(day_data["icon"])
            card["icon"].config(image=icon_image)
            card["icon"].image = icon_image

    def get_weather(event=None):
        """Fetch weather data from API"""
        city = textfield.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return

        try:
            # Show loading state
            search_btn.config(state=tk.DISABLED)
            root.config(cursor="watch")
            root.update()
            
            # Geocoding
            geolocator = Nominatim(user_agent="bluesky_weather")
            location = geolocator.geocode(city)
            if location is None:
                raise ValueError("City not found")

            # Timezone
            obj = TimezoneFinder()
            result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
            timezone.config(text=result.split("/")[-1].replace("_", " "))

            # Coordinates
            long_lat.config(text=f"{round(location.latitude,4)}°N, {round(location.longitude,4)}°E")

            # Local time
            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)

            # Weather API
            api_key = "d0bebc59ce406c638d2aeb77b036ff4f"
            current_api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            forecast_api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            
            # Current weather
            response = requests.get(current_api)
            response.raise_for_status()
            current_data = response.json()
            
            weather_data["current"] = {
                "temp": current_data["main"]["temp"],
                "feels_like": current_data["main"]["feels_like"],
                "humidity": current_data["main"]["humidity"],
                "pressure": current_data["main"]["pressure"],
                "wind_speed": current_data["wind"]["speed"],
                "description": current_data["weather"][0]["description"],
                "icon": current_data["weather"][0]["icon"],
                "visibility": current_data.get("visibility", 0),
                "cloudiness": current_data["clouds"]["all"]
            }
            
            # Forecast
            response = requests.get(forecast_api)
            response.raise_for_status()
            forecast_data = response.json()
            
            daily_data = {}
            for entry in forecast_data["list"]:
                date_txt = entry["dt_txt"]
                date = date_txt.split(" ")[0]
                time = date_txt.split(" ")[1]
                
                # Use midday forecast for each day
                if time == "12:00:00":
                    dt = datetime.strptime(date, "%Y-%m-%d")
                    daily_data[date] = {
                        "day": dt.strftime("%a"),
                        "date": dt.strftime("%m/%d"),
                        "temp": entry["main"]["temp"],
                        "description": entry["weather"][0]["description"],
                        "icon": entry["weather"][0]["icon"]
                    }
            
            weather_data["forecast"] = list(daily_data.values())
            
            # Update UI
            update_ui()
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not connect to weather service:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve weather data:\n{e}")
        finally:
            search_btn.config(state=tk.NORMAL)
            root.config(cursor="")

    search_btn = tk.Button(search_frame, image=search_icon, command=get_weather, 
                         bg=COLORS["accent_blue"], activebackground=COLORS["highlight"],
                         bd=0, relief=tk.FLAT, cursor="hand2")
    search_btn.image = search_icon
    search_btn.pack(side=tk.RIGHT, padx=5)

    # Current weather display
    current_weather_frame = tk.Frame(root, bg=COLORS["dark_blue"], bd=0)
    current_weather_frame.place(x=50, y=100, width=350, height=200)

    # Time and location info
    time_info_frame = tk.Frame(current_weather_frame, bg=COLORS["dark_blue"])
    time_info_frame.pack(pady=10)

    clock = tk.Label(time_info_frame, font=("Arial", 20, "bold"), 
                    bg=COLORS["dark_blue"], fg=COLORS["text_white"])
    clock.pack(side=tk.LEFT)

    timezone = tk.Label(time_info_frame, font=("Arial", 12), 
                       bg=COLORS["dark_blue"], fg=COLORS["text_gray"])
    timezone.pack(side=tk.LEFT, padx=10)

    long_lat = tk.Label(current_weather_frame, font=("Arial", 10), 
                       bg=COLORS["dark_blue"], fg=COLORS["text_gray"])
    long_lat.pack()

    # Main weather display
    weather_display_frame = tk.Frame(current_weather_frame, bg=COLORS["dark_blue"])
    weather_display_frame.pack(pady=10)

    temp_label = tk.Label(weather_display_frame, font=("Arial", 48, "bold"), 
                         bg=COLORS["dark_blue"], fg=COLORS["text_white"])
    temp_label.pack(side=tk.LEFT)

    weather_icon = tk.Label(weather_display_frame, bg=COLORS["dark_blue"])
    weather_icon.pack(side=tk.LEFT, padx=10)

    desc_label = tk.Label(current_weather_frame, font=("Arial", 14), 
                         bg=COLORS["dark_blue"], fg=COLORS["text_light"])
    desc_label.pack()

    # Weather details
    details_frame = tk.Frame(root, bg=COLORS["dark_blue"])
    details_frame.place(x=100, y=300, width=350, height=280)

    detail_labels = {}
    details = [
        ("Humidity", "humidity", "%"),
        ("Pressure", "pressure", "hPa"),
        ("Wind Speed", "wind", "m/s"),
        ("Feels Like", "feels_like", "°C"),
        ("Visibility", "visibility", "m"),
        ("Cloudiness", "clouds", "%")
    ]

    for i, (label_text, key, unit) in enumerate(details):
        row = i // 2
        col = i % 2
        
        frame = tk.Frame(details_frame, bg=COLORS["card_bg"], padx=10, pady=5)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        tk.Label(frame, text=label_text, font=("Arial", 10), 
                bg=COLORS["card_bg"], fg=COLORS["text_gray"]).pack(anchor="w")
        
        detail_labels[key] = tk.Label(frame, text=f"--{unit}", font=("Arial", 12, "bold"), 
                                    bg=COLORS["card_bg"], fg=COLORS["text_white"])
        detail_labels[key].pack(anchor="w")

    # Five Day Forecast
    forecast_frame = tk.Frame(root, bg=COLORS["dark_blue"])
    forecast_frame.place(x=420, y=100, width=380, height=400)

    tk.Label(forecast_frame, text="5-DAY FORECAST", font=("Arial", 12, "bold"), 
            bg=COLORS["dark_blue"], fg=COLORS["text_white"]).pack(pady=5)

    forecast_cards = []
    for i in range(5):
        card = tk.Frame(forecast_frame, bg=COLORS["card_bg"], padx=10, pady=10)
        card.pack(fill=tk.X, pady=3)
        
        day_frame = tk.Frame(card, bg=COLORS["card_bg"])
        day_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        day_label = tk.Label(day_frame, text="---", font=("Arial", 12, "bold"), 
                           bg=COLORS["card_bg"], fg=COLORS["text_white"])
        day_label.pack()
        
        date_label = tk.Label(day_frame, text="MM/DD", font=("Arial", 9), 
                            bg=COLORS["card_bg"], fg=COLORS["text_gray"])
        date_label.pack()
        
        icon_label = tk.Label(card, bg=COLORS["card_bg"])
        icon_label.pack(side=tk.LEFT, padx=10)
        
        temp_frame = tk.Frame(card, bg=COLORS["card_bg"])
        temp_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        temp_label = tk.Label(temp_frame, text="--°C", font=("Arial", 14, "bold"), 
                            bg=COLORS["card_bg"], fg=COLORS["text_white"])
        temp_label.pack()
        
        desc_label = tk.Label(temp_frame, text="---", font=("Arial", 10), 
                             bg=COLORS["card_bg"], fg=COLORS["text_gray"])
        desc_label.pack()
        
        forecast_cards.append({
            "day": day_label,
            "date": date_label,
            "icon": icon_label,
            "temp": temp_label,
            "desc": desc_label
        })

    # Footer
    footer = tk.Label(root, text="BlueSky Weather © 2025 | Made with Python and Tkinter by Anushka", 
                     font=("Arial", 9), bg=COLORS["dark_blue"], fg=COLORS["text_gray"])
    footer.pack(side=tk.BOTTOM, pady=10)

    # Bind Enter key to search
    textfield.bind("<Return>", get_weather)
    
    # Initial UI state
    temp_label.config(text="--°C")
    desc_label.config(text="Enter a city name")
    timezone.config(text="Timezone")
    long_lat.config(text="Latitude, Longitude")
    
    return root

if __name__ == "__main__":
    app = create_weather_app()
    app.mainloop()



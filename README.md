# 🌤️ Real-Time Weather App (KivyMD)

A modern, cross-platform Desktop/Mobile Weather Application built with **Python**, **KivyMD**, and the **OpenWeatherMap API**. Features live weather updates, dynamic weather icons, real-time clocks, and searchable city locations.

---

## 🌟 Key Features
- 🌡️ **Live Weather Metrics**: Displays temperature (°C), humidity, wind speed, pressure, min/max temp, sunrise, and sunset times.
- 🌆 **City Search**: Easily search weather details for any city around the world.
- 🎨 **Dynamic UI**: Uses custom KivyMD cards and weather condition icons (`Clear`, `Clouds`, `Rain`, `Snow`, etc.).
- 🕒 **Live Digital Clock**: Real-time date and time updates.
- 💾 **Local Data Persistence**: Remembers your last searched city across app restarts.

---

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **UI Framework:** Kivy & KivyMD
- **API Requests:** `requests` module
- **Data Handling:** OpenWeatherMap API (JSON Data), `pickle`

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/YOUR_USERNAME/kivymd-weather-app.git](https://github.com/YOUR_USERNAME/kivymd-weather-app.git)
cd kivymd-weather-app
pip install -requirements.txt

### 3. API Key Setup
​Get a free API key from OpenWeatherMap.
​Run the included setup script to save your key locally:
python create_key.py


###​4. Run the App:
python3 WeatherApp.py


├── .assets/                # Weather condition icons/images
├── main.py                 # Main application source code
├── create_key.py           # Helper script to store OpenWeatherMap API Key
├── requirements.txt        # Project dependencies
├── .gitignore              # Ignored local files (API key & cache)
└── README.md               # Project documentation


from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import FloatLayout
from time import strftime, localtime
from kivy.metrics import sp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import json
import pickle
import requests


with open('.key.db', 'rb') as f:
    data = pickle.load(f)

def get_data(city):
    api = data['key']
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
    try:
        return requests.get(url, timeout=10).json()
    except requests.exceptions.RequestException:
        return {"cod": 0, "message": "Network error. Check internet connection."}


kv = '''
#:import FitImage kivymd.uix.fitimage.FitImage
MDScreen:
    MDCard:
        id : upper
        orientation: 'horizontal'
        size_hint: 1, 0.08
        pos_hint:
            {'center_x': 0.5, 'center_y': 0.96}
        padding: 20
        spacing: 380
        elevation: 2
        radius: [20]
        md_bg_color: 1,1,0,1
        
        MDIconButton:
            icon: 'cloud-refresh'
            on_release: app.main('_')
        
        MDFlatButton:
            id: city
            text: 'City'
            bold: True
            italic: True
            font_size: '25dp'
            on_release: app.city_input()

    MDCard:
        padding: 20
        spacing: 20
        pos_hint:
            {'center_x': 0.5, 'center_y': 0.72}
        size_hint: 0.95, 0.37
        md_bg_color: '#1E90FF'
        elevation: 3
        radius: [20]
        
        FloatLayout:
            FitImage:
                id: weather_image
                size_hint: None, None
                size: "150dp", "150dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.65}
            
            Label:
                id: temp
                text: 'Loading....'
                pos_hint:
                    {'center_x':0.5, 'center_y':0.2}
                font_size: '35dp'
                bold: True
            
            Label:
                id: con
                text: 'Loading.....'
                pos_hint:
                    {'center_x':0.5, 'center_y': 0.05}
                font_size: '30dp'
                italic: True
    
    Label:
        id: date_time
        text: 'Date | time'
        pos_hint:
            {'center_x': 0.5, 'center_y': 0.88}
        font_size: '18dp'
        color: '#F5DEB3'
    
    GridLayout:
        id: main_layout
        cols: 2
        spacing: 30
        padding: 20
        pos_hint:
            {'center_x':0.5, 'center_y': 0.27}
        size_hint : 1, 0.5
        
'''

class WeatherApp(MDApp):
    def build(self):
        try:
            with open('.city_name.json') as f:
                self.city_db = json.load(f)
        except FileNotFoundError:
            self.city_db = {'city': 'Bankura'}
        
        self.city = self.city_db['city']
        self.we_data = get_data(self.city)
        sm = Builder.load_string(kv)
        Clock.schedule_interval(self.update, 1)
        return sm

    def update(self, dt):
        ti = self.root.ids.date_time
        format = '%A, %b %d   |   %H:%M:%S'
        ti.text = strftime(format)

    def popup(self, title, description):
        ok_btn = MDRaisedButton(text = "Ok")
        ok_btn.bind(on_release = self.close_btn)
            
        self.dialog = MDDialog(
            title="Info", text = description,
            auto_dismiss=True,
            buttons=[ok_btn])
        self.dialog.open()

    def close_btn(self, instance):
        self.dialog.dismiss()
    
    def city_input(self):
        bar = self.root.ids.upper
        bar.remove_widget(self.root.ids.city)
        
        self.input_city = MDTextField(
            hint_text= self.city,
            size_hint = (None, None),
            size = (250, 50),
            mode = 'rectangle'
        )
        
        self.input_city.bind(focus=self.on_change)
        bar.add_widget(self.input_city)
        self.input_city.focus = True
        
    def on_change(self, instance, focus):
        if not focus:
            if instance.text.strip():
                self.city = instance.text.strip().title()
                self.city_db['city'] = self.city
                with open('.city_name.json', 'w') as f:
                    json.dump(self.city_db, f)
                
                self.we_data = get_data(self.city)
                self.main('_')
            
            bar = self.root.ids.upper
            bar.remove_widget(instance)
            bar.add_widget(self.root.ids.city)
    
    def on_start(self):
        Clock.schedule_once(self.main, 5)
        
    
    def main(self, _):
        self.root.ids.city.text = self.city
        
        if self.we_data.get("cod") != 200:
            self.popup('Error', self.we_data['message'])
            return
        
        feel = f"{self.we_data['main']['feels_like'] - 273.15:.1f} °C"
        humi = f"{self.we_data['main']['humidity']} %"
        pres = f"{self.we_data['main']['pressure']} hPa"
        min_tem = f"{self.we_data['main']['temp_min'] - 273.15:.1f} °C"
        max_tem = f"{self.we_data['main']['temp_max'] - 273.15:.1f} °C"
        speed = f"{self.we_data['wind']['speed']} m/s SSE"
        sunset_dt = self.we_data['sys']['sunset']
        sunrise_dt = self.we_data['sys']['sunrise']
        sunset = strftime('%H:%M', localtime(sunset_dt))
        sunrise = strftime('%H:%M', localtime(sunrise_dt))
        
        
        image_data = {
            'Clear': '.assets/Clear.png',
            'Clouds': '.assets/Clouds.png',
            'Rain': '.assets/Rain.png',
            'Drizzle': '.assets/Drizzle.png',
            'Thunderstorm': '.assets/Thunder.png',
            'Snow': '.assets/Snow.png',
            'Mist': '.assets/Mist.png',
            'Haze': '.assets/Haze.png',
            'Fog': '.assets/Fog.png',
            'Smoke': '.assets/Smoke.png',
            'Dust': '.assets/Dust.png',
            'Sand': '.assets/Sand.png',
            'Tornado': '.assets/Tor.png',
            'Er': '.assets/no_png.png'
        }
        
        im = image_data
        cl = self.we_data['weather'][0]['main']
        we_image = self.root.ids.weather_image
        we_image.source = im.get(cl, im['Er'])
        self.root.ids.temp.text = f"{self.we_data['main']['temp']-273.15:.1f} °C"
        self.root.ids.con.text = cl
        
        data = [
            ('thermometer', 'Feels like', feel),
            ('water-percent', 'Humidity', humi),
            ('weather-windy', 'Wind Speed', speed),
            ('gauge', 'Pressure', pres),
            ('thermometer-low', 'Min Temperature', min_tem),
            ('thermometer-high', 'Max Temperature', max_tem),
            ('weather-sunset-up', 'Sunrise', sunrise),
            ('weather-sunset-down', 'Sunset', sunset)
        ]
         
        layout = self.root.ids.main_layout
        layout.clear_widgets()
        RGB = 255.0
        for icon_, con, situa in data:
            card = MDCard(
                orientation='horizontal',
                padding=20,
                spacing=20,
                md_bg_color= (204.0/RGB, 247.0/RGB, 253.0/RGB, 0.9),
                elevation=2,
                radius=[20]
            )
            
            icon_box = FloatLayout()

            icon_box.add_widget(
                MDIcon(
                    icon=icon_,
                    font_size = sp(80),
                    pos_hint =
                        {'center_x': 0.1, 'center_y': 0.5}
                )
            )

            icon_box.add_widget(
                MDLabel(
                    text=con,
                    halign='center',
                    font_style="Subtitle1",
                    italic = True,
                    pos_hint =
                        {'center_x':0.6, 'center_y':0.7}
                )
            )

            icon_box.add_widget(
                MDLabel(
                    text=situa,
                    halign='center',
                    font_style="H6",
                    font_size = '20dp',
                    bold=True,
                    pos_hint =
                        {'center_x': 0.6, 'center_y': 0.3}
                )
            )

            card.add_widget(icon_box)
            layout.add_widget(card)


WeatherApp().run()
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import speech_recognition as sr
import threading

class JapCounterApp(App):
    def build(self):
        self.count = 0
        self.is_listening = False
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # UI Elements
        self.label_title = Label(text="🙏 Naam Jap Counter", font_size='30sp')
        self.label_count = Label(text="0", font_size='80sp', color=(0, 1, 0, 1))
        self.status = Label(text="Click Start to Begin", font_size='18sp')
        
        self.start_btn = Button(text="Start Listening", size_hint=(1, 0.2), background_color=(0, 0.7, 0, 1))
        self.start_btn.bind(on_press=self.toggle_listening)
        
        # Add to layout
        self.layout.add_widget(self.label_title)
        self.layout.add_widget(self.label_count)
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.start_btn)
        
        return self.layout

    def toggle_listening(self, instance):
        if not self.is_listening:
            self.is_listening = True
            self.start_btn.text = "Stop Listening"
            self.status.text = "Listening for 'Ram'..."
            threading.Thread(target=self.listen_voice).start()
        else:
            self.is_listening = False
            self.start_btn.text = "Start Listening"
            self.status.text = "Stopped"

    def listen_voice(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while self.is_listening:
                try:
                    audio = r.listen(source, phrase_time_limit=2)
                    text = r.recognize_google(audio, language='hi-IN').lower()
                    if "ram" in text:
                        self.count += text.count("ram")
                        self.label_count.text = str(self.count)
                except:
                    continue

if __name__ == '__main__':
    JapCounterApp().run()
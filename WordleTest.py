from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="AdMob Test App"))
        layout.add_widget(Label(text="Check log for ad status"))
        return layout
    
    def on_start(self):
        if platform == 'android':
            try:
                from kivmob import KivMob
                
                ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
                BANNER_ID = "ca-app-pub-3940256099942544/6300978111"
                
                self.ads = KivMob(ADMOB_APP_ID)
                self.ads.new_banner(BANNER_ID, top_pos=True)
                self.ads.request_banner()
                self.ads.show_banner()
                print("AdMob initialization successful!")
            except Exception as e:
                print(f"AdMob initialization failed: {e}")
        else:
            print("Running on desktop - ads would show on Android")

if __name__ == "__main__":
    TestApp().run()
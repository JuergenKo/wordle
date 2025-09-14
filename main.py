from kivmob import KivMob
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text="Hello Ads")

    def on_start(self):
        try:
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")  # Test App ID
            self.ads.new_banner("ca-app-pub-3940256099942544/6300978111", top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()
        except Exception as e:
            import traceback
            print("⚠️ AdMob init failed:", e)
            traceback.print_exc()

TestApp().run()

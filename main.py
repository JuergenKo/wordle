from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivmob import KivMob

# Replace with your own AdMob App ID and Banner Unit ID
ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"      # Test App ID
BANNER_UNIT_ID = "ca-app-pub-3940256099942544/6300978111"    # Test Banner Unit ID

class MainLayout(BoxLayout):
    pass

class BannerApp(App):
    def build(self):
        # Initialize AdMob
        self.ads = KivMob(ADMOB_APP_ID)
        
        # Load banner
        self.ads.new_banner(BANNER_UNIT_ID, top_pos=False)  # bottom of screen
        self.ads.request_banner()
        self.ads.show_banner()

        return MainLayout()

if __name__ == "__main__":
    BannerApp().run()

from kivmob import KivMob
from kivy.app import App
from kivy.uix.label import Label


class BannerApp(App):
    def build(self):
        ads = KivMob("ca-app-pub-3940256099942544~3347511713")  # Google test App ID
        ads.new_banner("ca-app-pub-3940256099942544/6300978111", top_pos=False)
        ads.request_banner()
        ads.show_banner()
        return Label(text="Hello with Banner!")


if __name__ == "__main__":
    BannerApp().run()

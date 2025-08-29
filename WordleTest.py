from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivmob import KivMob


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.label = Label(text="Testing KivMob Banner Ad...")
        layout.add_widget(self.label)

        # Initialize AdMob (use the test app ID from buildozer.spec)
        self.ads = KivMob("ca-app-pub-3940256099942544~3347511713")

        # Request and show a banner (test unit ID from Google)
        self.ads.new_banner("ca-app-pub-3940256099942544/6300978111",
                            top_pos=False)  # False = bottom banner
        self.ads.request_banner()
        self.ads.show_banner()

        return layout


if __name__ == "__main__":
    TestApp().run()

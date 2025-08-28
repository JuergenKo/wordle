# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 20:22:53 2025

@author: juerg
"""

from kivy.app import App
from kivy.uix.label import Label
from kivmob import KivMob

ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
BANNER_ID = "ca-app-pub-3940256099942544/6300978111"

class TestApp(App):
    def build(self):
        return Label(text="Hello AdMob")

    def on_start(self):
        self.ads = KivMob(ADMOB_APP_ID)
        self.ads.new_banner(BANNER_ID, top_pos=True)
        self.ads.request_banner()
        self.ads.show_banner()

if __name__ == "__main__":
    TestApp().run()
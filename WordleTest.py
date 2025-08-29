# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 20:22:53 2025

@author: juerg
"""

from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

# For Android, use KivMob
if platform == 'android':
    from kivmob import KivMob
else:
    # Mock for desktop testing
    class KivMob:
        def __init__(self, app_id):
            print(f"Mock KivMob initialized with app ID: {app_id}")
        
        def new_banner(self, banner_id, top_pos=True):
            print(f"Mock banner created with ID: {banner_id}")
        
        def request_banner(self):
            print("Mock banner requested")
        
        def show_banner(self):
            print("Mock banner shown")

ADMOB_APP_ID = "ca-app-pub-3940256099942544~3347511713"
BANNER_ID = "ca-app-pub-3940256099942544/6300978111"

class TestApp(App):
    def build(self):
        return Label(text="Hello AdMob Test\nCheck log for ad status")
    
    def on_start(self):
        try:
            self.ads = KivMob(ADMOB_APP_ID)
            self.ads.new_banner(BANNER_ID, top_pos=True)
            self.ads.request_banner()
            self.ads.show_banner()
            print("AdMob initialization successful!")
        except Exception as e:
            print(f"AdMob initialization failed: {e}")

if __name__ == "__main__":
    TestApp().run()
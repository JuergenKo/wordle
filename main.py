import sys, os

with open("/data/data/org.test.hellokivy/files/app_start.log", "w") as f:
    f.write("✅ main.py started\n")
    f.write(f"sys.version={sys.version}\n")
    f.write(f"os.getcwd()={os.getcwd()}\n")

from kivy.app import App
from kivy.uix.label import Label

print(">>> main.py has started <<<")

class HelloApp(App):
    def build(self):
        print(">>> build() called <<<")
        return Label(text="Hello from Kivy!")

if __name__ == "__main__":
    print(">>> running app <<<")
    HelloApp().run()

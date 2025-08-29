from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import platform


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Basic Kivy Test"))
        layout.add_widget(Label(text="If this works, we'll add ads"))
        return layout

if __name__ == "__main__":
    TestApp().run()
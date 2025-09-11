import traceback
import sys
from kivy.config import Config

# Set window size for debugging
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')

def main():
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        
        class WordleApp(App):
            def build(self):
                return Label(text='Hello Wordle!')
        
        WordleApp().run()
    except Exception as e:
        # Print error to logcat
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        # Keep the app open for a bit to see the error
        import time
        time.sleep(10)
        raise

if __name__ == '__main__':
    main()

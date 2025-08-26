from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivmob import KivMob

class WordleHelperApp(App):
    def build(self):
        Logger.info("KivMob: Initializing AdMob...")
        self.debug_label = Label(text="Initializing...", size_hint_y=None, height=100, color=(1, 0, 0, 1)) # Red text for visibility
        self.debug_label.text_size = (self.debug_label.width, None) # Allow text wrapping

        # Create the main layout
        layout = BoxLayout(orientation='vertical')
        
        # Add the debug label at the top
        layout.add_widget(self.debug_label)
        
        # Add your app content in the middle
        content = Label(text="Your Wordle Game Goes Here", size_hint_y=0.8)
        layout.add_widget(content)
        
        # Add an empty widget at the bottom to reserve space for the banner
        # This helps us see if the banner is pushing content up
        banner_space = Label(text="[Banner Space]", size_hint_y=0.1, color=(0, 0, 1, 1))
        layout.add_widget(banner_space)
        
        # Now initialize KivMob
        try:
            self.ads = KivMob('ca-app-pub-3940256099942544~3347511713') # TEST ID
            self.banner_ad_id = 'ca-app-pub-3940256099942544/6300978111' # TEST ID
            self.debug_label.text = "KivMob initialized successfully."
            Logger.info("KivMob: Initialized successfully.")
        except Exception as e:
            error_msg = f"Failed to init KivMob: {e}"
            self.debug_label.text = error_msg
            Logger.error(error_msg)
        
        return layout

    def on_start(self):
        self.debug_label.text += "\nApp started, loading banner..."
        Logger.info("KivMob: App started, loading banner.")
        try:
            # Set a callback for when the banner is successfully loaded
            self.ads.set_banner_callback(self.banner_loaded)
            # Create the banner. This starts the loading process.
            self.ads.new_banner(self.banner_ad_id)
            self.ads.banner_pos = 'bottom'
            self.debug_label.text += "\nBanner loading started..."
            Logger.info("KivMob: Banner loading started.")
            # DO NOT call show_banner() here. Wait for the callback.
        except Exception as e:
            error_msg = f"\nError in on_start: {e}"
            self.debug_label.text += error_msg
            Logger.error(error_msg)

    # Define a new method that will be called when the banner is ready
    def banner_loaded(self):
        self.debug_label.text += "\nBanner LOADED! Showing it now."
        Logger.info("KivMob: Banner loaded callback received.")
        # NOW it is safe to show the banner
        self.ads.show_banner()

if __name__ == '__main__':
    WordleHelperApp().run()
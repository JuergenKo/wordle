

import sys
import os 
from kivy.config import Config


# Set this BEFORE any other Kivy imports
if sys.platform == 'android':
    os.environ['KCFG_GRAPHICS_FULLSCREEN'] = 'auto'
    os.environ['KCFG_GRAPHICS_RESIZABLE'] = '0'
    os.environ['KCFG_GRAPHICS_WINDOW_STATE'] = 'visible'
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'resizeable', '0')
    Config.set('graphics', 'window_state', 'visible')
else:
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '700')
# Write the configuration
Config.write()

# Only now import the rest of Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout

# Fix for Windows pen/touchscreen issue
if sys.platform == 'win32':
    Config.set('input', 'wm_pen', 'ignore')
    Config.set('input', 'wm_touch', 'mouse')
    Config.set('input', 'wm_pen', 'disable')



class WordleSolver:
    def __init__(self, guess_words_file="words_choose.txt", solution_words_file="solutions.txt"):
        self.guess_words = self.load_words(guess_words_file)
        self.solution_words = self.load_words(solution_words_file)
        self.possible_words = self.solution_words.copy()
        self.best_starting_word = "tares"  # Best starting word
        self.guess_history = []  # Store history of guesses and feedback
        self.current_guess = "tares"  # Track the current guess
        self.known_letters = {}  # position: letter
        self.excluded_letters = set()
        self.included_letters = {}  # letter: positions where it can't be
    
    def load_words(self, filename):
        """Load words from a file, one word per line"""
        try:
            with open(filename, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: File {filename} not found. Using empty word list.")
            return []
    
  
   
    def update_from_feedback(self, guess, feedback):
        """
        Update constraints based on user feedback
        feedback: string of 5 characters: 
          'g' for green (correct letter, correct position)
          'y' for yellow (correct letter, wrong position)
          'x' for gray (letter not in word)
        """
        if len(guess) != 5 or len(feedback) != 5:
            return False
        
        # Add to history
        self.guess_history.append((guess.upper(), feedback))
        
        print("Added to history ",guess.upper(), feedback)
        # Create temporary copies for validation
        temp_known = self.known_letters.copy()
        temp_excluded = self.excluded_letters.copy()
        temp_included = self.included_letters.copy()
        
        try:
            for i, (letter, fb) in enumerate(zip(guess, feedback)):
                if fb == 'g':
                    # Green: letter is correct in this position
                    temp_known[i] = letter
                    # Remove this letter from excluded if it was there
                    if letter in temp_excluded:
                        temp_excluded.remove(letter)
                elif fb == 'y':
                    # Yellow: letter is in word but not in this position
                    if letter not in temp_included:
                        temp_included[letter] = set()
                    temp_included[letter].add(i)
                    # Remove this letter from excluded if it was there
                    if letter in temp_excluded:
                        temp_excluded.remove(letter)
                elif fb == 'x':
                    # Gray: letter is not in the word
                    # But only if it's not already confirmed to be in the word
                    if letter not in temp_known.values() and letter not in temp_included:
                        temp_excluded.add(letter)
            
            # Apply the temporary changes
            self.known_letters = temp_known
            self.excluded_letters = temp_excluded
            self.included_letters = temp_included
            
            return True
        except Exception as e:
            print(f"Error updating feedback: {e}")
            return False
    
    def filter_words(self):
        """Filter possible words based on current constraints"""
        new_possible = []
        
        for word in self.possible_words:
            valid = True
            
            # Check known letters (green)
            for pos, letter in self.known_letters.items():
                if word[pos] != letter:
                    valid = False
                    break
            
            if not valid:
                continue
                
            # Check excluded letters (gray)
            for letter in self.excluded_letters:
                if letter in word:
                    valid = False
                    break
            
            if not valid:
                continue
                
            # Check included but misplaced letters (yellow)
            for letter, wrong_positions in self.included_letters.items():
                if letter not in word:
                    valid = False
                    break
                for pos in wrong_positions:
                    if word[pos] == letter:
                        valid = False
                        break
            
            if valid:
                new_possible.append(word)
        
        self.possible_words = new_possible
        return self.possible_words
    
    def evaluate(self,word1,word2):

        match = ""
        for count, value in enumerate(word1):
            if  word1[count:count+1] == word2[count:count+1]:
                word1 = word1[:count] + "-" + word1[count+1:]
                word2 = word2[:count] + "-" + word2[count+1:]
    
        for count, value in enumerate(word1):
            if  word1[count:count+1] == word2[count:count+1]:
                match = match +"2"
                word2 = word2[:count] + "-" + word2[count+1:]
            else:
                if  word1[count:count+1] in word2:
                    match = match +"1"
                    pos = word2.find(word1[count:count+1])
                    word2 = word2[:pos] + "-" + word2[pos+1:]
                else:
                   match = match + "0"
            #print("--",word1,word2,match)
        return match

    
    # Splits words_l in buckets with words having the same score eval(word,.)
    def count_in(self,word,words_l):
        buckets = [0] * 243
        for w in words_l:
            i = int(self.evaluate(word,w),3)
            buckets[i] += 1
            #print(w,int(eval(w,word),2))
        return(buckets)
    

    
    def calculate_word_score(self, word, possible_words):
        """Calculate the score for a word - lower is better"""
        # Calculate the sum of squares of matches
        matches = self.count_in(word, possible_words)
        return sum(x**2 for x in matches)
    
    def choose_best(self, words_list):
        """Choose the best word based on your algorithm"""
        if not words_list:
            return "No words available"
            
        best_word = words_list[0]
        best_score = self.calculate_word_score(best_word, words_list)
        
        for i, word in enumerate(words_list):
            score = self.calculate_word_score(word, words_list)
            
            if i % 100 == 0 and i > 0: 
                print(f"{i} {best_word} {best_score/len(words_list):5.2f}")
            
            if score < best_score:
                best_word = word
                best_score = score
        
        avg_remaining = best_score / len(words_list) if words_list else 0
        print(f"best = {best_word} - will leave in average {avg_remaining:5.2f} words remaining")
        return best_word, best_score
    
    def get_suggestions(self, count=10):
        """Get word suggestions ordered by score (lowest score first)"""
        if not self.possible_words:
            return ["No words match your criteria"]
        
        # Calculate scores for all possible words
        word_scores = []
        for word in self.possible_words:
            score = self.calculate_word_score(word, self.possible_words)
            word_scores.append((word, score))
        for word in self.guess_words:
            if word not in self.possible_words:
                score = self.calculate_word_score(word, self.possible_words)
                word_scores.append((word, score))
        
        # Sort by score (lowest first)
        word_scores.sort(key=lambda x: x[1])
        
        # Get the top N words
        Scores = [score for word, score in word_scores[:count]]
        suggestions = [word for word, score in word_scores[:count]]
        print("DEBUG ", suggestions, Scores, self.possible_words[:3])
        
        return suggestions
    
    def reset(self):
        """Reset all constraints"""
        self.possible_words = self.solution_words.copy()
        self.known_letters = {}
        self.excluded_letters = set()
        self.included_letters = {}
        self.guess_history = []
        self.current_guess = "tares"
        return True

class FeedbackButton(Button):
    def __init__(self, position, **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.feedback_state = 'x'  # x, y, g
        self.background_normal = ''
        self.update_color()
        
    def on_touch_down(self, touch):
        # More reliable touch handling
        if self.collide_point(*touch.pos):
            self.on_press()
            return True
        return super().on_touch_down(touch)
        
    def on_press(self):
        # Cycle through feedback states: x -> y -> g -> x
        if self.feedback_state == 'x':
            self.feedback_state = 'y'
        elif self.feedback_state == 'y':
            self.feedback_state = 'g'
        else:
            self.feedback_state = 'x'
        
        self.update_color()
    
    def update_color(self):
        if self.feedback_state == 'x':
            self.background_color = (0.5, 0.5, 0.5, 1)  # Gray
            self.text = 'X'
        elif self.feedback_state == 'y':
            self.background_color = (0.9, 0.9, 0.2, 1)  # Yellow
            self.text = 'Y'
        else:
            self.background_color = (0.2, 0.8, 0.2, 1)  # Green
            self.text = 'G'
    
    def reset(self):
        self.feedback_state = 'x'
        self.update_color()

class HistoryBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 1
        self.size_hint_y = None
        self.height = sp(40)
        
    def set_guess(self, word, feedback):
        """Set the word and feedback with colored letters"""
        self.clear_widgets()
        
        # Add word label
        word_label = Label(
            text=f"{word}:",
            size_hint_x=0.3,
            color=(0, 0, 0, 1),
            bold=True,
            font_size=sp(14)
        )
        self.add_widget(word_label)
        
        # Add colored letter labels
        for i, (letter, fb) in enumerate(zip(word, feedback)):
            color = (0, 0, 0, 1)  # Default black
            if fb == 'x':
                color = (0.5, 0.5, 0.5, 1)  # Gray
            elif fb == 'y':
                color = (0.9, 0.9, 0, 1)  # Yellow
            elif fb == 'g':
                color = (0, 0.8, 0, 1)  # Green
                
            letter_label = Label(
                text=letter,
                size_hint_x=0.14,
                color=color,
                bold=True,
                font_size=sp(12)
            )
            self.add_widget(letter_label)

class ClickableSuggestionLabel(Label):
    def __init__(self, app_instance, word, is_best=False, **kwargs):
        super().__init__(**kwargs)
        self.app_instance = app_instance
        self.word = word
        self.is_best = is_best
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app_instance.use_suggestion(self.word)
            return True
        return super().on_touch_down(touch)

class WordleHelperApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def debug_window_info(self, dt):
        print(f"Window after 0.1s - Size: {Window.size}, Fullscreen: {Window.fullscreen}")

    def fix_window_size(self, dt, attempt=1):
        """Fix window size with retry logic - enhanced version"""
        try:
            if attempt > 5:  # Increased max attempts
                print("Max fix attempts reached")
                return
                
            print(f"Window fix attempt {attempt}: {Window.size} vs {Window.system_size}")
            
            # More aggressive approach
            Window.fullscreen = 'auto'
            Window.borderless = True
            Window.size = Window.system_size
            
            # Android-specific fixes
            if sys.platform == 'android':
                try:
                    from android.runnable import run_on_ui_thread
                    from jnius import autoclass
                    
                    @run_on_ui_thread
                    def set_fullscreen_ui():
                        try:
                            PythonActivity = autoclass('org.kivy.android.PythonActivity')
                            activity = PythonActivity.mActivity
                            View = autoclass('android.view.View')
                            WindowManager = autoclass('android.view.WindowManager$LayoutParams')
                            
                            # Get the window
                            window = activity.getWindow()
                            
                            # Clear any force-not-fullscreen flags
                            window.clearFlags(WindowManager.FLAG_FORCE_NOT_FULLSCREEN)
                            
                            # Set fullscreen flags
                            flags = (
                                WindowManager.FLAG_FULLSCREEN |
                                WindowManager.FLAG_LAYOUT_NO_LIMITS |
                                WindowManager.FLAG_LAYOUT_IN_SCREEN |
                                WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS
                            )
                            window.addFlags(flags)
                            
                            # Set immersive mode
                            decor_view = window.getDecorView()
                            system_ui_flags = (
                                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
                                View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                                View.SYSTEM_UI_FLAG_FULLSCREEN |
                                View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                                View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
                                View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            )
                            decor_view.setSystemUiVisibility(system_ui_flags)
                            
                        except Exception as e:
                            print(f"UI thread error: {e}")
                    
                    set_fullscreen_ui()
                    
                except Exception as e:
                    print(f"Android import error: {e}")
            
            print(f"Window after fix: {Window.size}")
            
            # Schedule another attempt if still not right
            if (hasattr(Window, 'system_size') and 
                hasattr(Window, 'size') and 
                len(Window.size) > 1 and 
                len(Window.system_size) > 1 and
                Window.size[1] < Window.system_size[1]):
                
                Clock.schedule_once(lambda dt: self.fix_window_size(dt, attempt + 1), 0.5)
                    
        except Exception as e:
            print(f"Window fix error: {e}")
            if attempt < 5:
                Clock.schedule_once(lambda dt: self.fix_window_size(dt, attempt + 1), 0.5)        
    def on_window_resize(self, window, width, height):
        """Handle window resize events"""
        if sys.platform == 'android':
            print(f"Window resized to: {width}x{height}, system: {Window.system_size}")
            if height < Window.system_size[1]:
                # Window is smaller than system size, try to fix
                Clock.schedule_once(self.fix_window_size, 0.1)

    def build(self):
   
        if sys.platform == 'android':
             print(f"Initial Window size: {Window.size}")
             print(f"System size: {Window.system_size}")
             print(f"Fullscreen setting: {Window.fullscreen}")
             Clock.schedule_once(self.debug_window_info, 0.1)
             Clock.schedule_once(self.fix_window_size, 0.5)

        Window.bind(on_resize=self.on_window_resize)
        self.solver = WordleSolver()
        self.title = "Wordle Helper"
        self._processing = False  # Add this line
        
        # Set background color
        try:
            Window.clearcolor = (0.95, 0.95, 0.95, 1)
        except:
            pass
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title with adaptive font size
        title = Label(
            text="Wordle Helper", 
            size_hint_y=0.05, 
            font_size=sp(24),
            color=(0, 0, 0.5, 1),
            bold=True
        )
        layout.add_widget(title)
        
        # Step 1: Guess a word
        step1_label = Label(
            text="Step 1: Click on a suggested word below", 
            size_hint_y=0.04,
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            bold=True
        )
        layout.add_widget(step1_label)
        
        # Current guess display
        self.current_guess_label = Label(
            text=f"Current guess: TARES", 
            size_hint_y=0.05,
            font_size=sp(18),
            color=(0.2, 0.5, 0.2, 1),
            bold=True
        )
        layout.add_widget(self.current_guess_label)
        
        # Step 2: Copy the wordle evaluation
        step2_label = Label(
            text="Step 2: Set Wordle evaluation", 
            size_hint_y=0.04,
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            bold=True
        )
        layout.add_widget(step2_label)
        
        # Feedback buttons
  

        # ... your existing code ...
        
        # Replace your current feedback_layout code with this:
        anchor_layout = AnchorLayout(anchor_x='center', size_hint_y=0.12)
        feedback_layout = GridLayout(cols=5, size_hint=(None, 1), spacing=5)
        
        # Calculate total width: (5 buttons * 60sp) + (4 gaps * 5sp)
        feedback_layout.width = sp(60) * 5 + sp(5) * 4
        
        self.feedback_buttons = []
        for i in range(5):
            btn = FeedbackButton(
                position=i, 
                size_hint=(None, None), 
                size=(sp(60), sp(60)),
                color=(0, 0, 0, 1),
                font_size=sp(20)
            )
            self.feedback_buttons.append(btn)
            feedback_layout.add_widget(btn)
        
        anchor_layout.add_widget(feedback_layout)
        layout.add_widget(anchor_layout)  # ✅ This will be centered
                
        # Feedback legend
    
        legend_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=0.04, 
            spacing=5,
            pos_hint={'center_x': 0.5}  # ✅ Center horizontally
            )       
        legend_layout.add_widget(Label(
            text="X: Not in word", 
            size_hint_x=0.33, 
            color=(0.5, 0.5, 0.5, 1),
            font_size=sp(14)
        ))
        legend_layout.add_widget(Label(
            text="Y: Wrong position", 
            size_hint_x=0.34, 
            color=(0.8, 0.8, 0, 1),
            font_size=sp(14)
        ))
        legend_layout.add_widget(Label(
            text="G: Correct", 
            size_hint_x=0.33, 
            color=(0, 0.8, 0, 1),
            font_size=sp(14)
        ))
        layout.add_widget(legend_layout)
        
        # Step 3: Make a new suggestion
        step3_label = Label(
            text="Step 3: Process feedback and get new suggestions", 
            size_hint_y=0.04,
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            bold=True
        )
        layout.add_widget(step3_label)
        
        # Action buttons
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        
        self.suggest_btn = Button(
            text="Get Suggestions", 
            on_press=self.process_and_get_suggestions,
            background_color=(0.8, 0.5, 0, 1),
            font_size=sp(14)
        )
        action_layout.add_widget(self.suggest_btn)
        
        self.reset_btn = Button(
            text="Reset Solver", 
            on_press=self.reset_solver,
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=sp(14)
        )
        action_layout.add_widget(self.reset_btn)
        
        layout.add_widget(action_layout)
        
        # Suggestions area (single list)
        suggestions_label = Label(
            text="Guess Word Suggestions (Select):", 
            size_hint_y=0.04,
            color=(0, 0, 0.5, 1),
            bold=True,
            font_size=sp(16)
        )
        layout.add_widget(suggestions_label)
        
        scroll = ScrollView(size_hint_y=0.35)
        self.suggestions_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=1)
        self.suggestions_layout.bind(minimum_height=self.suggestions_layout.setter('height'))
        scroll.add_widget(self.suggestions_layout)
        layout.add_widget(scroll)
        
        # Show initial suggestions
        self.show_initial_suggestions()
        
        # Guess History at the bottom
        history_label = Label(
            text="Guess History:", 
            size_hint_y=0.10,
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            line_height=0.1,
            bold=True
        )
        layout.add_widget(history_label)
        
        # History scroll view
        self.history_scroll = ScrollView(size_hint_y=0.20)
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=1)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scroll.add_widget(self.history_layout)
        layout.add_widget(self.history_scroll)
        
        # Status label
        self.status_label = Label(
            text=f"Click on 'TARES' to start, then set feedback colors", 
            size_hint_y=0.04,
            color=(0.3, 0.3, 0.3, 1),
            font_size=sp(14)
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def on_start(self):
        """Handle window focus for proper fullscreen"""
        Window.bind(on_keyboard=self.on_keyboard)
        Window.bind(focus=self.on_window_focus)
        
        # Initial fix
        if sys.platform == 'android':
            Clock.schedule_once(self.fix_window_size, 0.5)
    
    def on_window_focus(self, window, has_focus):
        """Re-apply fullscreen when window gains focus"""
        if has_focus and sys.platform == 'android':
            print("Window gained focus, reapplying fullscreen")
            Clock.schedule_once(self.fix_window_size, 0.1)
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle back button to prevent app exit"""
        if key == 27:  # ESC key (back button)
            # Optional: Add your back button handling
            return True  # Prevent default behavior
        return False
      
    
    
    
    def show_initial_suggestions(self):
        """Show initial suggestions starting with 'TARES'"""
        self.suggestions_layout.clear_widgets()
        
        # Start with the best starting word
        initial_suggestions = [self.solver.best_starting_word]
        
        # Add some  suggestions from the default list
  
        initial_suggestions.extend(['rates','aloes','aeons'])
  
        
        # Display all suggestions in a single list
        for i, word in enumerate(initial_suggestions):
            if i == 0:  # Best word
                label = ClickableSuggestionLabel(
                    app_instance=self,
                    word=word,
                    is_best=True,
                    text=f"★ {word.upper()} ★ (Recommended)", 
                    size_hint_y=None, 
                    height=sp(40),
                    font_size=sp(18),
                    color=(0, 0.6, 0, 1),
                    bold=True
                )
                # Add special background for best word
                with label.canvas.before:
                    Color(0.9, 1, 0.9, 1)
                    Rectangle(pos=label.pos, size=(self.get_window_width(), sp(40)))
            else:
                label = ClickableSuggestionLabel(
                    app_instance=self,
                    word=word,
                    text=word.upper(), 
                    size_hint_y=None, 
                    height=sp(40),
                    font_size=sp(18),
                    color=(0, 0, 0, 1)
                )
                # Add background color for better visibility
                with label.canvas.before:
                    Color(0.85, 0.85, 0.85, 1)
                    Rectangle(pos=label.pos, size=(self.get_window_width(), sp(40)))
            
            self.suggestions_layout.add_widget(label)
    
    def get_window_width(self):
        """Get window width safely"""
        try:
            return Window.width
        except:
            return 400  # Default width
    
    def update_history_display(self):
        """Update the history display with all previous guesses"""
        self.history_layout.clear_widgets()
        
        for word, feedback in self.solver.guess_history:
            history_box = HistoryBox()
            history_box.set_guess(word, feedback)
            self.history_layout.add_widget(history_box)
            
        # Auto-scroll to bottom after layout updates
        Clock.schedule_once(lambda dt: self.scroll_history_to_bottom(), 0.1)

    def scroll_history_to_bottom(self):
        """Scroll the history scroll view to the bottom"""
        # Scroll to show the most recent guess
        # scroll_y = 0 = bottom, scroll_y = 1 = top
        self.history_scroll.scroll_y = 0
    
    def use_suggestion(self, word):
        """Use a suggestion word as the current guess"""
        self.solver.current_guess = word
        self.current_guess_label.text = f"Current guess: {word.upper()}"
        self.status_label.text = f"Selected: '{word.upper()}'. Set feedback colors and click 'Get Suggestions'."
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._process_scheduled = False
        self._processing = False

    def process_and_get_suggestions(self, instance):
        """Process the current guess with feedback and get new suggestions"""
        # Double protection: check both flags
        if self._process_scheduled or self._processing:
            print("DEBUG: Already processing or scheduled, skipping...")
            return
        
        self._process_scheduled = True
        self._processing = True
        Clock.schedule_once(lambda dt: self._actually_process_suggestions(instance), 0.05)
    
    def _actually_process_suggestions(self, instance):
        """The actual processing logic"""
        print(f"DEBUG: _actually_process_suggestions called with instance: {instance}")
        
        try:
            guess = self.solver.current_guess
            
            if not guess or len(guess) != 5:
                self.status_label.text = "Please select a word first"
                return
            
            # Get feedback from buttons
            feedback = ''.join(btn.feedback_state for btn in self.feedback_buttons)
            
            # Update solver
            success = self.solver.update_from_feedback(guess, feedback)
            if success:
                self.solver.filter_words()
                self.status_label.text = f"Processed feedback. {len(self.solver.possible_words)} possible words remain."
                # Update history display
                self.update_history_display()
                # Get and show new suggestions
                self.get_suggestions(None)
            else:
                self.status_label.text = "Error processing feedback. Please try again."
            
            # Reset feedback buttons
            for btn in self.feedback_buttons:
                btn.reset()
                
        except Exception as e:
            print(f"Error in _actually_process_suggestions: {e}")
            self.status_label.text = f"Error: {str(e)}"
            
        finally:
            # Always reset both flags
            self._process_scheduled = False
            self._processing = False
            print("DEBUG: All flags reset")
        
    def get_suggestions(self, instance):
        # Show calculating message
        self.suggestions_layout.clear_widgets()
        calculating_label = Label(
            text="Calculating suggestions...", 
            size_hint_y=None, 
            height=sp(40),
            font_size=sp(16),
            color=(0.5, 0.5, 0.5, 1)
        )
        self.suggestions_layout.add_widget(calculating_label)
        
        # Schedule the calculation to avoid UI freezing
        Clock.schedule_once(lambda dt: self.calculate_suggestions(), 0.1)
    
    def calculate_suggestions(self):
        suggestions = self.solver.get_suggestions(10)
        
        # Clear previous suggestions
        self.suggestions_layout.clear_widgets()
        
        if not suggestions:
            label = Label(
                text="No suggestions available", 
                size_hint_y=None, 
                height=sp(40),
                font_size=sp(16),
                color=(0.5, 0.5, 0.5, 1)
            )
            self.suggestions_layout.add_widget(label)
            return
        # Get possible words from solver
        possible_words = self.solver.possible_words if hasattr(self, 'solver') else []
        only_one = False
        if len(possible_words) == 1:
            suggestions = possible_words
            only_one = True
        # Display all suggestions in a single list
        for i, word in enumerate(suggestions):
            
           
            # Check if word is in possible_words
            is_possible = word in possible_words
            if i == 0:  # Best word
                self.use_suggestion(word)
                label = ClickableSuggestionLabel(
                    app_instance=self,
                    word=word,
                    is_best=True,
                    text=f"★ {word.upper()} ★ (Possible Solution)" if is_possible else f"★ {word.upper()} ★ (Best)", 
                    size_hint_y=None, 
                    height=sp(16),
                    font_size=sp(12),
                    color= (0, 0.6, 0, 1),  # Red if possible, else green
                    bold=True,
                    line_height=0.3
                )
                # Add special background for best word
                with label.canvas.before:
                    Color(0.9, 1, 0.9, 1)
                    Rectangle(pos=label.pos, size=(self.get_window_width(), sp(40)))
            else:
                label = ClickableSuggestionLabel(
                    app_instance=self,
                    word=word,
                    text=f"★ {word.upper()} ★ (Possible Solution)" if is_possible else word.upper(), 
                    size_hint_y=None, 
                    height=sp(16),
                    font_size=sp(12),
                    line_height=0.3,
                    color= (0, 0, 0, 1)  #  black
                )
                # Add background color for better visibility
                with label.canvas.before:
                    Color(0.85, 0.85, 0.85, 1)
                    Rectangle(pos=label.pos, size=(self.get_window_width(), sp(40)))
            
                
            self.suggestions_layout.add_widget(label)
        
        self.status_label.text = f"Found {len(suggestions)} suggestions. Click one to select it."
    
    def reset_solver(self, instance):
        success = self.solver.reset()
        if success:
            for btn in self.feedback_buttons:
                btn.reset()
            self.suggestions_layout.clear_widgets()
            self.history_layout.clear_widgets()
            # Add the initial best word back to history after reset
            # self.solver.guess_history.append((self.solver.best_starting_word.upper(), 'xxxxx'))
            self.update_history_display()
            # Show initial suggestions again
            self.show_initial_suggestions()
            # Reset current guess display
            self.current_guess_label.text = f"Current guess: TARES"
            self.status_label.text = "Solver reset. Click on 'TARES' to start."
        else:
            self.status_label.text = "Error resetting solver."

if __name__ == '__main__':
    if sys.platform == 'android':
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        except Exception as e:
            print("Permission request failed:", e)

        # Keep this as a backup fix
        Clock.schedule_once(lambda dt: setattr(Window, "fullscreen", "auto"), 1)

    WordleHelperApp().run()

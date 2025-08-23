from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.clock import Clock
import random
import os
import sys


# ANDROID FIX: Set configuration early
if sys.platform == 'android':
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'resizeable', True)
    Config.set('graphics', 'window_state', 'maximized')
    Config.set('graphics', 'borderless', '1')
else:
    from kivy.core.window import Window
    Window.size = (400, 700)

# Fix for Windows pen/touchscreen issue
if sys.platform == 'win32':
    Config.set('input', 'wm_pen', 'ignore')
    Config.set('input', 'wm_touch', 'mouse')
    Config.set('input', 'wm_pen', 'disable')

class WordleSolver:
    def __init__(self, word_file="words_choose.txt"):
        self.words = self.load_words(word_file)
        self.possible_words = self.words.copy()
        self.known_letters = {}  # position: letter
        self.excluded_letters = set()
        self.included_letters = {}  # letter: positions where it can't be
        self.best_starting_word = "roate"  # Best starting word
        self.guess_history = []  # Store history of guesses and feedback
        self.current_guess = "roate"  # Track the current guess
        
    def load_words(self, filename):
        words = []
        try:
            # Try to load from current directory first
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    for line in file:
                        word = line.strip().lower()
                        if len(word) == 5 and word.isalpha():
                            words.append(word)
                print(f"Loaded {len(words)} words from {filename}")
            else:
                # Try to load from assets directory (for Android)
                assets_path = os.path.join('assets', filename)
                if os.path.exists(assets_path):
                    with open(assets_path, 'r') as file:
                        for line in file:
                            word = line.strip().lower()
                            if len(word) == 5 and word.isalpha():
                                words.append(word)
                    print(f"Loaded {len(words)} words from {assets_path}")
                else:
                    print(f"File {filename} not found. Using default word list.")
                    words = self.get_default_words()
        except Exception as e:
            print(f"Error loading words: {e}. Using default word list.")
            words = self.get_default_words()
        return words
    
    def get_default_words(self):
        # Fallback word list if file is not found
        return [
            'roate', 'apple', 'brave', 'crane', 'dance', 'earth', 'flame', 'grape', 
            'house', 'image', 'jolly', 'knife', 'lemon', 'music', 'night', 'olive', 
            'peace', 'queen', 'river', 'smile', 'table', 'unity', 'vivid', 'water', 
            'xenon', 'yacht', 'zebra', 'actor', 'badge', 'crisp', 'dwarf', 'elbow', 
            'frost', 'ghost', 'index', 'jumpy', 'kneel', 'latch', 'mango', 'noble', 
            'optic', 'piano', 'quilt', 'robin', 'shelf', 'tiger', 'ultra', 'vocal', 
            'wrist', 'xerox', 'youth', 'zippy', 'audio', 'baker', 'candy', 'diary',
            'eagle', 'fairy', 'giant', 'happy', 'ivory', 'jelly', 'karma', 'lucky',
            'magic', 'nymph', 'olive', 'puzzle', 'quick', 'raven', 'sweet', 'tango',
            'umber', 'vapor', 'whale', 'xylem', 'yearn', 'zesty', 'abide', 'blaze',
            'chime', 'drake', 'elope', 'flint', 'globe', 'hinge', 'inbox', 'joust',
            'koala', 'lumen', 'mirth', 'nexus', 'otter', 'prism', 'quark', 'rinse',
            'slate', 'trope', 'usher', 'vixen', 'waltz', 'xenon', 'yodel', 'zonal'
        ]
    
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
    
    def count_in(self, word, words_list):
        """Count how many words in the list match the pattern of the given word"""
        counts = []
        for w in words_list:
            for i in range(5):
                if word[i] == w[i]:
                    counts.append(1)
                else:
                    counts.append(0)
        return counts
    
    def calculate_word_score(self, word, words_list):
        """Calculate the score for a word - lower is better"""
        # Calculate the sum of squares of matches
        matches = self.count_in(word, words_list)
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
    
    def get_suggestions(self, count=5):
        """Get word suggestions ordered by score (lowest score first)"""
        if not self.possible_words:
            return ["No words match your criteria"]
        
        # Calculate scores for all possible words
        word_scores = []
        for word in self.possible_words:
            score = self.calculate_word_score(word, self.possible_words)
            word_scores.append((word, score))
        
        # Sort by score (lowest first)
        word_scores.sort(key=lambda x: x[1])
        
        # Get the top N words
        suggestions = [word for word, score in word_scores[:count]]
        
        return suggestions
    
    def reset(self):
        """Reset all constraints"""
        self.possible_words = self.words.copy()
        self.known_letters = {}
        self.excluded_letters = set()
        self.included_letters = {}
        self.guess_history = []
        self.current_guess = "roate"
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
        self.spacing = 2
        self.size_hint_y = None
        self.height = sp(40)
        
    def set_guess(self, word, feedback):
        """Set the word and feedback colors"""
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
        
        # Add feedback boxes
        for i, fb in enumerate(feedback):
            color_box = BoxLayout(
                size_hint_x=0.14,
                size_hint_y=1
            )
            
            # Set background color based on feedback
            with color_box.canvas.before:
                if fb == 'x':
                    Color(0.5, 0.5, 0.5, 1)  # Gray
                elif fb == 'y':
                    Color(0.9, 0.9, 0.2, 1)  # Yellow
                else:  # 'g'
                    Color(0.2, 0.8, 0.2, 1)  # Green
                Rectangle(pos=color_box.pos, size=color_box.size)
            
            # Add letter in the box
            letter_label = Label(
                text=word[i],
                color=(0, 0, 0, 1),
                bold=True,
                font_size=sp(16)
            )
            color_box.add_widget(letter_label)
            self.add_widget(color_box)

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
    
    def on_start(self):
        """Called when the app starts - fix window size for Android"""
        try:
            from kivy.core.window import Window
    
            if sys.platform == 'android':
                # Force fullscreen mode only
                Window.fullscreen = 'auto'
    
                # Schedule a delayed resize to ensure it fills the screen
                Clock.schedule_once(self.fix_android_window, 0.5)
            else:
                # On desktop, you *can* use a fixed window size
                Window.size = (400, 700)
                Window.left = 0
                Window.top = 0
        except Exception as e:
            print(f"Window size error: {e}")
    
    def fix_android_window(self, dt):
        """Ensure Android window uses full screen"""
        try:
            from kivy.core.window import Window
            Window.fullscreen = 'auto'
            print("Android window forced to fullscreen:", Window.size)
        except Exception as e:
            print(f"Android window fix error: {e}")
 

    
    def build(self):

        self.solver = WordleSolver()
        self.title = "Wordle Helper"
        self._processing = False  # Add this line
        
        # Set background color
        try:
            from kivy.core.window import Window
            Window.clearcolor = (0.95, 0.95, 0.95, 1)
        except:
            pass
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title with adaptive font size
        title = Label(
            text="Wordle Solver", 
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
            text=f"Current guess: ROATE", 
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
        self.feedback_buttons = []
        feedback_layout = GridLayout(cols=5, size_hint_y=0.12, spacing=5)
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
        layout.add_widget(feedback_layout)
        
        # Feedback legend
        legend_layout = BoxLayout(orientation='horizontal', size_hint_y=0.04, spacing=5)
        legend_layout.add_widget(Label(
            text="X: Not in word", 
            size_hint_x=0.33, 
            color=(0.5, 0.5, 0.5, 1),
            font_size=sp(12)
        ))
        legend_layout.add_widget(Label(
            text="Y: Wrong position", 
            size_hint_x=0.34, 
            color=(0.8, 0.8, 0, 1),
            font_size=sp(12)
        ))
        legend_layout.add_widget(Label(
            text="G: Correct", 
            size_hint_x=0.33, 
            color=(0, 0.8, 0, 1),
            font_size=sp(12)
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
            text="Process & Find Suggestions", 
            on_press=self.process_and_get_suggestions,
            background_color=(0.8, 0.5, 0, 1),
            font_size=sp(16)
        )
        action_layout.add_widget(self.suggest_btn)
        
        self.reset_btn = Button(
            text="Reset Solver", 
            on_press=self.reset_solver,
            background_color=(0.8, 0.2, 0.2, 1),
            font_size=sp(16)
        )
        action_layout.add_widget(self.reset_btn)
        
        layout.add_widget(action_layout)
        
        # Suggestions area (single list)
        suggestions_label = Label(
            text="Word Suggestions:", 
            size_hint_y=0.04,
            color=(0, 0, 0.5, 1),
            bold=True,
            font_size=sp(16)
        )
        layout.add_widget(suggestions_label)
        
        scroll = ScrollView(size_hint_y=0.25)
        self.suggestions_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.suggestions_layout.bind(minimum_height=self.suggestions_layout.setter('height'))
        scroll.add_widget(self.suggestions_layout)
        layout.add_widget(scroll)
        
        # Show initial suggestions
        self.show_initial_suggestions()
        
        # Guess History at the bottom
        history_label = Label(
            text="Guess History:", 
            size_hint_y=0.04,
            font_size=sp(16),
            color=(0.3, 0.3, 0.3, 1),
            bold=True
        )
        layout.add_widget(history_label)
        
        # History scroll view
        self.history_scroll = ScrollView(size_hint_y=0.15)
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scroll.add_widget(self.history_layout)
        layout.add_widget(self.history_scroll)
        
        # Status label
        self.status_label = Label(
            text=f"Click on 'ROATE' to start, then set feedback colors", 
            size_hint_y=0.04,
            color=(0.3, 0.3, 0.3, 1),
            font_size=sp(14)
        )
        layout.add_widget(self.status_label)
        
        return layout
    
    def show_initial_suggestions(self):
        """Show initial suggestions starting with 'roate'"""
        self.suggestions_layout.clear_widgets()
        
        # Start with the best starting word
        initial_suggestions = [self.solver.best_starting_word]
        
        # Add some random suggestions from the default list
        other_words = [w for w in self.solver.words if w != self.solver.best_starting_word]
        random_sample = random.sample(other_words, min(4, len(other_words)))
        initial_suggestions.extend(random_sample)
        
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
            from kivy.core.window import Window
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
        self.status_label.text = f"Selected: '{word.upper()}'. Set feedback colors and click 'Process & Find Suggestions'."
    
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
        suggestions = self.solver.get_suggestions(5)
        
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
        
        # Display all suggestions in a single list
        for i, word in enumerate(suggestions):
            if i == 0:  # Best word
                label = ClickableSuggestionLabel(
                    app_instance=self,
                    word=word,
                    is_best=True,
                    text=f"★ {word.upper()} ★ (Best)", 
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
            self.current_guess_label.text = f"Current guess: ROATE"
            self.status_label.text = "Solver reset. Click on 'ROATE' to start."
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

        from kivy.core.window import Window
        # Just to be safe, schedule a fullscreen fix
        Clock.schedule_once(lambda dt: setattr(Window, "fullscreen", "auto"), 1)

    WordleHelperApp().run()

# Import necessary Kivy modules and other libraries
from kivy.config import Config  # Import Config from kivy.config
Config.set('graphics', 'fullscreen', 'auto')  # Set fullscreen mode to auto

from kivy.app import App 
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Line, Color, Rectangle, PushMatrix, PopMatrix, Rotate, RoundedRectangle 
from kivy.core.window import Window 
from kivy.clock import Clock 
from kivy.core.audio import SoundLoader 
from kivy.uix.label import Label 
from kivy.uix.popup import Popup  
from kivy.utils import get_color_from_hex  
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.button import Button  
from kivy.vector import Vector  
from kivy.logger import Logger
import math  
import random 
import time  
from kivy.properties import NumericProperty, StringProperty 
from kivy.uix.textinput import TextInput  
import json 
import logging  
import os 

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
logger = logging.getLogger(__name__)  # Create logger instance

# Define the file name for the hall of fame
HALL_OF_FAME_FILE = 'hall_of_fame.json'  # Define the hall of fame file

# MAIN SCREENS

# Define the main menu screen class
class MainMenu(Screen):  # Define MainMenu class inheriting from Screen
    def __init__(self, **kwargs):  # Initialize MainMenu
        super().__init__(**kwargs)  # Call the superclass initializer
        self.bg = MainMenuBackground()  # Create background widget
        self.add_widget(self.bg)  # Add background widget to screen

        button_color = get_color_from_hex("#333333")  # Define button color

        welcome_button = Label(  # Create welcome label
            text="Invasion: Antibody Odyssey",  # Set label text
            size_hint=(0.5, 0.2),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.8},  # Set position hint
            font_size=73,  # Set font size
            font_name='Nightcore Demo.ttf'  # Set font name
        )
        self.add_widget(welcome_button)  # Add welcome label to screen

        play_button = RoundedButton(  # Create play button
            text="Play",  # Set button text
            size_hint=(0.2, 0.075),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.6},  # Set position hint
            font_size=28,  # Set font size
            font_name='Nightcore Demo.ttf',  # Set font name
            background_color=button_color  # Set background color
        )
        play_button.bind(on_release=self.switch_to_game)  # Bind button release event to switch_to_game method
        self.add_widget(play_button)  # Add play button to screen

        hall_of_fame_button = RoundedButton(  # Create hall of fame button
            text="Hall of Fame",  # Set button text
            size_hint=(0.2, 0.075),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.45},  # Set position hint
            font_size=28,  # Set font size
            font_name='Nightcore Demo.ttf',  # Set font name
            background_color=button_color  # Set background color
        )
        hall_of_fame_button.bind(on_release=self.show_hall_of_fame)  # Bind button release event to show_hall_of_fame method
        self.add_widget(hall_of_fame_button)  # Add hall of fame button to screen

        help_button = RoundedButton(  # Create help button
            text="Help",  # Set button text
            size_hint=(0.2, 0.075),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.3},  # Set position hint
            font_size=28,  # Set font size
            font_name='Nightcore Demo.ttf',  # Set font name
            background_color=button_color  # Set background color
        )
        help_button.bind(on_release=self.show_help)  # Bind button release event to show_help method
        self.add_widget(help_button)  # Add help button to screen

        self.sound = SoundLoader.load("main_menu_music.mp3")  # Load main menu music

    def on_enter(self):  # Define on_enter method
        if self.sound:  # Check if sound is loaded
            self.sound.loop = True  # Set sound to loop
            self.sound.play()  # Play sound

    def on_leave(self):  # Define on_leave method
        if self.sound:  # Check if sound is loaded
            self.sound.stop()  # Stop sound

    def switch_to_game(self, instance):  # Define switch_to_game method
        self.manager.transition = FadeTransition()  # Set transition to FadeTransition
        self.manager.current = "game"  # Set current screen to game
        self.manager.get_screen('game').game_widget.reset_game()  # Reset game

    def show_hall_of_fame(self, instance):  # Define show_hall_of_fame method
        self.manager.transition = FadeTransition()  # Set transition to FadeTransition
        self.manager.current = "hall_of_fame"  # Set current screen to hall_of_fame

    def show_help(self, instance):  # Define show_help method
        help_text = (  # Define help text
            "Instructions:\n"
            "1. To complete the game you have to kill the viruses, by shooting them 10 times each.\n"
            "2. You have a maximum of 30 shots per level, if you run out of shots you lose.\n"
            "3. The less shots you use, the greater the score.\n"
            "4. You can choose your shots between 'w' projectile, 's' bombshell, and 'x' laser.\n"
            "5. You can move the antibody 'd' forward, and 'a' backwards.\n"
            "6. To incline the antibody and shoot, use the touchpad: the further the pointer, the greater the force of shooting.\n"
            "7. Be aware of the obstacles! Recognize them and learn how to avoid and exploit them in your favor.\n"
            "8. Have fun, but most importantly: complete your mission!"
        )
        popup = Popup(  # Create help popup
            title='Instructions',  # Set popup title
            content=Label(  # Create label for popup content
                text=help_text,  # Set label text
                font_name='friday.ttf',  # Set font name
                text_size=(730, None),  # Set text size
                halign='center',  # Set horizontal alignment
                valign='middle'  # Set vertical alignment
            ),
            size_hint=(None, None),  # Set size hint
            size=(800, 600)  # Set size
        )
        popup.open()  # Open popup

# Define the game screen class
class GameScreen(Screen):  # Define GameScreen class inheriting from Screen
    def __init__(self, **kwargs):  # Initialize GameScreen
        super().__init__(**kwargs)  # Call the superclass initializer
        self.game_widget = GameWidget()  # Create game widget
        self.add_widget(self.game_widget)  # Add game widget to screen
        Clock.schedule_once(self.set_manager, 0)  # Schedule set_manager method to be called once

    def set_manager(self, dt):  # Define set_manager method
        self.game_widget.manager = self.manager  # Set manager for game widget

    def on_enter(self):  # Define on_enter method
        self.game_widget.start_music()  # Start game music

    def on_leave(self):  # Define on_leave method
        self.game_widget.stop_music()  # Stop game music

# Define the hall of fame screen class
class HallOfFame(Screen):  # Define HallOfFame class inheriting from Screen
    def __init__(self, **kwargs):  # Initialize HallOfFame
        super().__init__(**kwargs)  # Call the superclass initializer
        with self.canvas:  # Add background image to canvas
            self.bg_rect = Rectangle(source='halloffame.png', pos=self.pos, size=Window.size)  # Set background image

        self.label = Label(  # Create label for hall of fame title
            text='Hall of Fame',  # Set label text
            font_size=45,  # Set font size
            pos_hint={'center_x': 0.5, 'top': 1},  # Set position hint
            size_hint=(1, None),  # Set size hint
            height=100,  # Set height
            font_name="Nightcore Demo.ttf"  # Set font name
        )
        self.add_widget(self.label)  # Add label to screen

        self.content_layout = BoxLayout(  # Create layout for content
            orientation='vertical',  # Set orientation
            padding=10,  # Set padding
            spacing=10,  # Set spacing
            size_hint=(1, 0.8),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Set position hint
        )

        with self.content_layout.canvas.before:  # Set background for names and scores
            Color(0, 0, 0, 0.5)  # Set color
            self.bg_rect = Rectangle(pos=self.content_layout.pos, size=self.content_layout.size)  # Set rectangle
            self.content_layout.bind(pos=self.update_bg_pos, size=self.update_bg_size)  # Bind position and size updates

        self.list_label = Label(  # Create label for hall of fame list
            text=self.get_hall_of_fame_text(),  # Set label text
            font_size=35,  # Set font size
            halign='center',  # Set horizontal alignment
            valign='middle',  # Set vertical alignment
            color=(1, 1, 1, 1),  # Set color
            text_size=(self.width - 20, None),  # Set text size
            font_name='TrueLies.ttf',  # Set font name
            line_height=2  # Set line height
        )
        self.list_label.bind(size=self.update_text_size)  # Bind size update
        self.content_layout.add_widget(self.list_label)  # Add list label to layout
        self.add_widget(self.content_layout)  # Add content layout to screen

    def update_bg_pos(self, instance, value):  # Define update_bg_pos method
        self.bg_rect.pos = value  # Update background position

    def update_bg_size(self, instance, value):  # Define update_bg_size method
        self.bg_rect.size = value  # Update background size

    def get_hall_of_fame_text(self):  # Define get_hall_of_fame_text method
        if os.path.exists(HALL_OF_FAME_FILE):  # Check if hall of fame file exists
            try:  # Try to read hall of fame file
                with open(HALL_OF_FAME_FILE, 'r') as f:  # Open hall of fame file
                    hall_of_fame = json.load(f)  # Load JSON data
            except json.JSONDecodeError:  # Handle JSON decode error
                hall_of_fame = []  # Set hall_of_fame to empty list
        else:  # If file does not exist
            hall_of_fame = []  # Set hall_of_fame to empty list

        text = ''  # Initialize text
        for i, entry in enumerate(hall_of_fame):  # Iterate over hall_of_fame entries
            text += f"{i + 1}. {entry['name']}: {entry['score']}\n"  # Add entry to text
        return text  # Return text

    def update_text_size(self, *args):  # Define update_text_size method
        self.list_label.text_size = self.list_label.size  # Update text size

    def on_pre_enter(self, *args):  # Define on_pre_enter method
        self.list_label.text = self.get_hall_of_fame_text()  # Refresh hall of fame list text

# Define the storyline screen class
class StorylineScreen(Screen):  # Define StorylineScreen class inheriting from Screen
    def __init__(self, **kwargs):  # Initialize StorylineScreen
        super().__init__(**kwargs)  # Call the superclass initializer
        self.images = ['image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png']  # List of images for the storyline
        self.current_image = 0  # Initialize current image index
        with self.canvas:  # Add background image to canvas
            self.bg = Rectangle(source=self.images[self.current_image], pos=self.pos, size=Window.size)  # Set background image

        self.skip_button = RoundedButton(  # Create skip button
            text="Skip",  # Set button text
            size_hint=(None, None),  # Set size hint
            size=(100, 50),  # Set size
            pos=(Window.width - 110, Window.height - 60),  # Set position
            font_size=28,  # Set font size
            background_color=(0.5, 0.5, 0.5, 0.8)  # Set background color
        )
        self.skip_button.bind(on_release=self.skip_storyline)  # Bind button release event to skip_storyline method
        self.add_widget(self.skip_button)  # Add skip button to screen

        Window.bind(on_key_down=self.on_key_down)  # Bind key down event
        Window.bind(on_resize=self._update_bg_size)  # Bind resize event
        self.bind(pos=self._update_bg_size, size=self._update_bg_size)  # Bind position and size updates

        self.sound = SoundLoader.load("storyline_music.mp3")  # Load storyline music

    def on_enter(self):  # Define on_enter method
        if self.sound:  # Check if sound is loaded
            self.sound.loop = True  # Set sound to loop
            self.sound.play()  # Play sound

    def on_leave(self):  # Define on_leave method
        if self.sound:  # Check if sound is loaded
            self.sound.stop()  # Stop sound

    def _update_bg_size(self, *args):  # Define _update_bg_size method
        self.bg.pos = self.pos  # Update background position
        self.bg.size = Window.size  # Update background size
        self.skip_button.pos = (Window.width - 110, Window.height - 60)  # Update skip button position

    def on_touch_down(self, touch):  # Define on_touch_down method
        self.next_image()  # Show next image
        return super().on_touch_down(touch)  # Call superclass method

    def on_key_down(self, window, key, *args):  # Define on_key_down method
        if key == 13:  # Check if key is Enter
            self.next_image()  # Show next image

    def next_image(self):  # Define next_image method
        self.current_image += 1  # Increment current image index
        if self.current_image < len(self.images):  # Check if there are more images
            self.bg.source = self.images[self.current_image]  # Update background image
        else:  # If no more images
            self.switch_to_menu()  # Switch to main menu

    def skip_storyline(self, instance):  # Define skip_storyline method
        self.switch_to_menu()  # Switch to main menu

    def switch_to_menu(self):  # Define switch_to_menu method
        self.manager.transition = FadeTransition()  # Set transition to FadeTransition
        self.manager.current = 'main_menu'  # Set current screen to main_menu

# Define the splash screen class
class SplashScreen(Screen):  # Define SplashScreen class inheriting from Screen
    def __init__(self, **kwargs):  # Initialize SplashScreen
        super().__init__(**kwargs)  # Call the superclass initializer
        with self.canvas:  # Add background image to canvas
            self.bg = Rectangle(source='splash bg.png', pos=self.pos, size=Window.size)  # Set background image
        Window.bind(on_resize=self._update_bg_size)  # Bind resize event

        splash_label = Label(  # Create welcome label
            text="Welcome to Invasion: Antibody Odyssey",  # Set label text
            size_hint=(0.5, 0.2),  # Set size hint
            pos_hint={'center_x': 0.5, 'center_y': 0.8},  # Set position hint
            font_size=120,  # Set font size
            font_name='Nightcore Demo.ttf'  # Set font name
        )
        self.add_widget(splash_label)  # Add welcome label to screen

        splash_image = Rectangle(source='game logo.png', pos=(Window.width / 2 - 250, Window.height / 2 - 300), size=(500, 500))  # Create splash image
        with self.canvas:  # Add splash image to canvas
            self.canvas.add(splash_image)  # Add splash image

        self.sound = SoundLoader.load("splash music.mp3")  # Load and play splash music
        if self.sound:  # Check if sound is loaded
            self.sound.loop = True  # Set sound to loop
            self.sound.play()  # Play sound

        Clock.schedule_once(self.switch_to_storyline, 5)  # Schedule switch to storyline screen after 5 seconds

    def _update_bg_size(self, *args):  # Define _update_bg_size method
        self.bg.size = Window.size  # Update background size

    def switch_to_storyline(self, dt):  # Define switch_to_storyline method
        if self.sound:  # Check if sound is loaded
            self.sound.stop()  # Stop sound
        self.manager.transition = FadeTransition()  # Set transition to FadeTransition
        self.manager.current = 'storyline'  # Set current screen to storyline

# WIDGETS AND GAME COMPONENTS

# Define the main menu background class
class MainMenuBackground(Widget):  # Define MainMenuBackground class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize MainMenuBackground
        super().__init__(**kwargs)  # Call the superclass initializer
        with self.canvas:  # Add background image to canvas
            self.bg_rect = Rectangle(source='alien homescreen bg.png', pos=self.pos, size=Window.size)  # Set background image
        Window.bind(on_resize=self._update_bg_size)  # Bind resize event

    def _update_bg_size(self, *args):  # Define _update_bg_size method
        self.bg_rect.size = Window.size  # Update background size

# Define the rounded button class
class RoundedButton(ButtonBehavior, Widget):  # Define RoundedButton class inheriting from ButtonBehavior and Widget
    def __init__(self, text='', font_size=14, font_name='Roboto', background_color=(0, 0, 0, 1), **kwargs):  # Initialize RoundedButton
        super().__init__(**kwargs)  # Call the superclass initializer
        self.text = text  # Set text
        self.font_size = font_size  # Set font size
        self.font_name = font_name  # Set font name
        self.background_color = background_color  # Set background color

        with self.canvas:  # Set background color and shape
            Color(*self.background_color)  # Set color
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(20, 20), (20, 20), (20, 20), (20, 20)])  # Set rectangle

        self.label = Label(text=self.text, font_size=self.font_size, font_name=self.font_name, color=(1, 1, 1, 1), size=self.size, pos=self.pos, halign='center', valign='middle')  # Add label
        self.label.bind(size=self.update_text, pos=self.update_text)  # Bind size and position updates

        self.bind(pos=self.update_rect, size=self.update_rect)  # Bind position and size updates

        self.add_widget(self.label)  # Add label to widget

    def update_rect(self, *args):  # Define update_rect method
        self.rect.pos = self.pos  # Update rectangle position
        self.rect.size = self.size  # Update rectangle size
        self.label.size = self.size  # Update label size
        self.label.pos = self.pos  # Update label position

    def update_text(self, *args):  # Define update_text method
        self.label.text_size = self.label.size  # Update text size

# Define the hall of fame popup class
class HallOfFamePopup(Popup):  # Define HallOfFamePopup class inheriting from Popup
    def __init__(self, score, **kwargs):  # Initialize HallOfFamePopup
        super().__init__(**kwargs)  # Call the superclass initializer
        self.title = 'Congratulations! You may now take your seat in the Hall of Fame.'  # Set popup title
        self.size_hint = (None, None)  # Set size hint
        self.size = (400, 300)  # Set size
        self.score = score  # Set score

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)  # Create content layout

        self.name_input = TextInput(hint_text='Enter your name', size_hint=(1, None), height=30, multiline=False, font_name='Nightcore Demo.ttf', font_size=16)  # Add name input
        save_button = Button(text='Save', size_hint=(1, None), height=40, font_name='Nightcore Demo.ttf', font_size=16)  # Create save button
        save_button.bind(on_release=self.save_score)  # Bind button release event to save_score method
        content.add_widget(self.name_input)  # Add name input to content layout
        content.add_widget(Label(text=f'Your final score: {self.score}', size_hint=(1, None), height=30))  # Add final score label to content layout
        content.add_widget(save_button)  # Add save button to content layout
        self.content = content  # Set popup content

    def save_score(self, instance):  # Define save_score method
        name = self.name_input.text.strip()  # Get name from input
        if not name:  # Check if name is empty
            name = 'Anonymous'  # Set default name
        new_entry = {'name': name, 'score': self.score}  # Create new entry

        if os.path.exists(HALL_OF_FAME_FILE):  # Check if hall of fame file exists
            try:  # Try to read hall of fame file
                with open(HALL_OF_FAME_FILE, 'r') as f:  # Open hall of fame file
                    hall_of_fame = json.load(f)  # Load JSON data
            except json.JSONDecodeError:  # Handle JSON decode error
                hall_of_fame = []  # Set hall_of_fame to empty list
        else:  # If file does not exist
            hall_of_fame = []  # Set hall_of_fame to empty list

        hall_of_fame.append(new_entry)  # Add new entry to hall_of_fame
        hall_of_fame.sort(key=lambda x: x['score'], reverse=True)  # Sort hall_of_fame by score
        hall_of_fame = hall_of_fame[:10]  # Limit hall_of_fame to top 10 entries

        with open(HALL_OF_FAME_FILE, 'w') as f:  # Write hall_of_fame to file
            json.dump(hall_of_fame, f, indent=4)  # Dump JSON data

        self.dismiss()  # Dismiss popup

# Define the pause menu popup class
class PauseMenuPopup(Popup):  # Define PauseMenuPopup class inheriting from Popup
    def __init__(self, game_widget, **kwargs):  # Initialize PauseMenuPopup
        super().__init__(**kwargs)  # Call the superclass initializer
        self.title = 'Pause'  # Set popup title
        self.size_hint = (None, None)  # Set size hint
        self.size = (400, 200)  # Set size
        self.game_widget = game_widget  # Set game widget

        content = BoxLayout(orientation='vertical', spacing=10, padding=20)  # Create content layout
        continue_button = Button(text='Continue', size_hint=(1, 0.5))  # Create continue button
        main_menu_button = Button(text='Main Menu', size_hint=(1, 0.5))  # Create main menu button

        continue_button.bind(on_release=self.continue_game)  # Bind button release event to continue_game method
        main_menu_button.bind(on_release=self.go_to_main_menu)  # Bind button release event to go_to_main_menu method

        content.add_widget(continue_button)  # Add continue button to content layout
        content.add_widget(main_menu_button)  # Add main menu button to content layout
        self.content = content  # Set popup content

    def continue_game(self, instance):  # Define continue_game method
        self.dismiss()  # Dismiss popup

    def go_to_main_menu(self, instance):  # Define go_to_main_menu method
        self.dismiss()  # Dismiss popup
        if self.game_widget.manager:  # Check if game widget has manager
            self.game_widget.manager.transition = FadeTransition()  # Set transition to FadeTransition
            self.game_widget.manager.current = 'main_menu'  # Set current screen to main_menu

# GAME COMPONENTS

# Define the target class
class Target(Widget):  # Define Target class inheriting from Widget
    life = NumericProperty(10)  # Define target life
    image_source = StringProperty("target_1.png")  # Define image source

    def __init__(self, image_source, **kwargs):  # Initialize Target
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (120, 120)  # Set size
        self.image_source = image_source  # Set image source
        self.x = random.uniform(Window.width * 2 / 3, Window.width - self.width)  # Set x position
        self.y = random.uniform(0, Window.height - self.height)  # Set y position
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source=self.image_source, pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_target_pos)  # Bind position update

        self.target_x = random.uniform(Window.width * 2 / 3, Window.width - self.width)  # Set target x position
        self.target_y = random.uniform(0, Window.height - self.height)  # Set target y position
        self.speed = 150  # Set speed

        self.move_event = Clock.schedule_interval(self.move_target, 1 / 60)  # Schedule move_target method

    def update_target_pos(self, *args):  # Define update_target_pos method
        self.image.pos = self.pos  # Update image position

    def move_target(self, dt):  # Define move_target method
        direction = Vector(self.target_x - self.x, self.target_y - self.y).normalize()  # Calculate direction
        new_pos = Vector(*self.pos) + direction * self.speed * dt  # Calculate new position

        while self.check_overlap(new_pos, self.size):  # Check if new position overlaps with other objects
            self.target_x = random.uniform(Window.width * 2 / 3, Window.width - self.width)  # Set new target x position
            self.target_y = random.uniform(0, Window.height - self.height)  # Set new target y position
            direction = Vector(self.target_x - self.x, self.target_y - self.y).normalize()  # Calculate new direction
            new_pos = Vector(*self.pos) + direction * self.speed * dt  # Calculate new position

        self.pos = new_pos  # Update position

        if Vector(self.target_x - self.x, self.target_y - self.y).length() < self.speed * dt:  # Check if target is reached
            self.target_x = random.uniform(Window.width * 2 / 3, Window.width - self.width)  # Set new target x position
            self.target_y = random.uniform(0, Window.height - self.height)  # Set new target y position

    def check_overlap(self, pos, size):  # Define check_overlap method
        if self.parent is None:  # Check if parent is None
            return False  # Return False
        radius = 20  # Set radius
        parent = self.parent  # Get parent
        for obstacle in getattr(parent, 'obstacles', []):  # Iterate over obstacles
            if Vector(pos).distance(Vector(obstacle.rectangle.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for mirror in getattr(parent, 'mirrors', []):  # Iterate over mirrors
            if Vector(pos).distance(Vector(mirror.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for elastonio in getattr(parent, 'elastonios', []):  # Iterate over elastonios
            if Vector(pos).distance(Vector(elastonio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for gravitonio in getattr(parent, 'gravitonios', []):  # Iterate over gravitonios
            if Vector(pos).distance(Vector(gravitonio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for perpetio in getattr(parent, 'perpetios', []):  # Iterate over perpetios
            if Vector(pos).distance(Vector(perpetio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for wormhole in getattr(parent, 'wormholes', []):  # Iterate over wormholes
            if Vector(pos).distance(Vector(wormhole.pos1)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
            if Vector(pos).distance(Vector(wormhole.pos2)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        return False  # Return False

    def hit(self):  # Define hit method
        self.life -= 1  # Decrease life
        if self.life <= 0:  # Check if life is zero
            self.level_up()  # Level up

    def level_up(self):  # Define level_up method
        self.move_event.cancel()  # Cancel move event
        App.get_running_app().root.current_screen.game_widget.level_up()  # Level up game widget

# Define the projectile class
class Projectile(Widget):  # Define Projectile class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize Projectile
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (50, 50)  # Set size
        self.velocity = Vector(0, 0)  # Set velocity
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source='projectile.png', pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_graphics)  # Bind position update
        self.bind(size=self.update_graphics)  # Bind size update

    def update_graphics(self, *args):  # Define update_graphics method
        self.image.pos = self.pos  # Update image position
        self.image.size = self.size  # Update image size

# Define the bombshell class
class Bombshell(Projectile):  # Define Bombshell class inheriting from Projectile
    mass = NumericProperty(1)  # Define mass
    speed = NumericProperty(0)  # Define speed
    time = NumericProperty(0)  # Define time
    angle = NumericProperty(0)  # Define angle
    velocity_x = NumericProperty(0)  # Define velocity_x
    velocity_y = NumericProperty(0)  # Define velocity_y

    def __init__(self, **kwargs):  # Initialize Bombshell
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (60, 60)  # Set size
        self.has_collided = False  # Set has_collided to False
        self.exploded = False  # Set exploded to False
        self.gravity = -98.1  # Set gravity
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source='bombshell.png', pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_graphics)  # Bind position update
        self.bind(size=self.update_graphics)  # Bind size update

    def trajectory(self, dt):  # Define trajectory method
        self.x += self.velocity_x * dt  # Update x position
        self.y += self.velocity_y * dt  # Update y position
        self.velocity_y += self.gravity * dt  # Update velocity_y

        if self.y <= 0:  # Check if y position is zero
            self.explode(0)  # Explode

    def explode(self, delay):  # Define explode method
        self.exploded = True  # Set exploded to True
        self.mass = 999  # Set mass to 999
        self.velocity_x = 0  # Set velocity_x to 0
        self.velocity_y = 0  # Set velocity_y to 0

        if self.parent:  # Check if parent is not None
            with self.parent.canvas:  # Add explosion image to canvas
                Color(1, 1, 1)  # Set color
                self.explosion_image = Rectangle(source='explosion.png', pos=(self.x - 50, self.y - 50), size=(200, 200))  # Set explosion image

            Clock.schedule_once(self.remove_explosion, 2)  # Schedule remove_explosion method

        self.pos = (50000, 50000)  # Set position out of screen

    def remove_explosion(self, dt):  # Define remove_explosion method
        if self.parent and self.explosion_image in self.parent.canvas.children:  # Check if explosion image is in canvas
            self.parent.canvas.remove(self.explosion_image)  # Remove explosion image from canvas

    def affect_trajectory(self, gravitonio):  # Define affect_trajectory method
        dx = gravitonio.center_x - self.center_x  # Calculate dx
        dy = gravitonio.center_y - self.center_y  # Calculate dy
        distance = math.sqrt(dx ** 2 + dy ** 2)  # Calculate distance
        influence_radius = 200  # Set influence radius
        if distance < influence_radius:  # Check if distance is less than influence radius
            force = 5000 / (distance ** 2)  # Calculate force
            if gravitonio.effect == "repel":  # Check if effect is repel
                force = -force  # Invert force
            angle = math.atan2(dy, dx)  # Calculate angle
            force_x = force * math.cos(angle)  # Calculate force_x
            force_y = force * math.sin(angle)  # Calculate force_y

            self.velocity_x += force_x  # Update velocity_x
            self.velocity_y += force_y  # Update velocity_y

# Define the laser class
class Laser(Widget):  # Define Laser class inheriting from Widget
    mass = NumericProperty(0.5)  # Define mass
    speed = NumericProperty(10)  # Define speed
    time = NumericProperty(0)  # Define time
    angle = NumericProperty(0)  # Define angle

    def __init__(self, **kwargs):  # Initialize Laser
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (40, 10)  # Set size
        self.length = 50  # Set length

        with self.canvas:  # Add laser to canvas
            self.color = Color(0, 1, 0)  # Set color
            self.laser = Line(points=[self.center_x, self.center_y, self.center_x + self.length, self.center_y], width=2)  # Set laser line

        self.bind(pos=self.update_laser_pos)  # Bind position update
        self.bind(angle=self.update_laser_pos)  # Bind angle update

    def update_laser_pos(self, *args):  # Define update_laser_pos method
        self.canvas.clear()  # Clear canvas
        with self.canvas:  # Add laser to canvas
            self.color = Color(0, 1, 0)  # Set color
            self.laser = Line(points=[self.center_x, self.center_y, self.center_x + self.length * math.cos(math.radians(self.angle)), self.center_y + self.length * math.sin(math.radians(self.angle))], width=2)  # Set laser line

    def trajectory(self):  # Define trajectory method
        self.x += self.speed * math.cos(math.radians(self.angle))  # Update x position
        self.y += self.speed * math.sin(math.radians(self.angle))  # Update y position
        self.time += 0.5  # Update time

# Define the mirror class
class MirrorBulletproof(Widget):  # Define MirrorBulletproof class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize MirrorBulletproof
        super().__init__(**kwargs)  # Call the superclass initializer
        self.angle = random.randint(0, 360)  # Set angle
        with self.canvas:  # Add mirror to canvas
            Color(0.68, 0.85, 0.9)  # Set color
            PushMatrix()  # Push matrix
            self.rotation = Rotate(angle=self.angle, origin=self.center)  # Set rotation
            self.mir = Rectangle(pos=self.pos, size=(10, 100))  # Set mirror
            PopMatrix()  # Pop matrix
            self.size = self.mir.size  # Set size

        self.bind(pos=self.update_mir_pos, size=self.update_mir_size)  # Bind position and size updates

    def update_mir_pos(self, *args):  # Define update_mir_pos method
        self.mir.pos = self.pos  # Update mirror position
        self.rotation.origin = self.center  # Update rotation origin

    def update_mir_size(self, *args):  # Define update_mir_size method
        self.mir.size = self.size  # Update mirror size

    def collide_with_laser(self, laser):  # Define collide_with_laser method
        return self.collide_widget(laser)  # Check collision with laser

    def reflect_laser(self, laser):  # Define reflect_laser method
        incoming_angle = math.radians(laser.angle)  # Calculate incoming angle
        mirror_angle = math.radians(self.angle)  # Calculate mirror angle

        reflected_angle = 2 * mirror_angle - incoming_angle  # Calculate reflected angle

        laser.angle = math.degrees(reflected_angle) % 360  # Update laser angle

# Define the elastonio class
class Elastonio(Widget):  # Define Elastonio class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize Elastonio
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (60, 100)  # Set size
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source='elastonio.png', pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_elastonio_pos)  # Bind position update

    def update_elastonio_pos(self, *args):  # Define update_elastonio_pos method
        self.image.pos = self.pos  # Update image position

    def collide_with_projectile(self, projectile):  # Define collide_with_projectile method
        return self.collide_widget(projectile)  # Check collision with projectile

    def collide_with_bombshell(self, bombshell):  # Define collide_with_bombshell method
        return self.collide_widget(bombshell)  # Check collision with bombshell

    def collide_with_laser(self, laser):  # Define collide_with_laser method
        return self.collide_widget(laser)  # Check collision with laser

# Define the perpetio class
class Perpetio(Widget):  # Define Perpetio class inheriting from Widget
    def __init__(self, image_source, **kwargs):  # Initialize Perpetio
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (150, 150)  # Set size
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source=image_source, pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_perpetio_pos)  # Bind position update

    def update_perpetio_pos(self, *args):  # Define update_perpetio_pos method
        self.image.pos = self.pos  # Update image position

# Define the obstacle class
class Obstacle:  # Define Obstacle class
    def __init__(self, rectangle, oscillation_amplitude, oscillation_speed):  # Initialize Obstacle
        self.rectangle = rectangle  # Set rectangle
        self.oscillation_amplitude = oscillation_amplitude  # Set oscillation amplitude
        self.oscillation_speed = oscillation_speed  # Set oscillation speed
        self.initial_pos = rectangle.pos  # Set initial position

# Define the gravitonio class
class Gravitonio(Widget):  # Define Gravitonio class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize Gravitonio
        super().__init__(**kwargs)  # Call the superclass initializer
        self.effect = random.choice(["attract", "repel"])  # Set effect
        self.size = (100, 100)  # Set size
        with self.canvas:  # Add image to canvas
            self.image = Rectangle(source='gravitonio.png', pos=self.pos, size=self.size)  # Set image
        self.bind(pos=self.update_gravitonio_pos)  # Bind position update

    def update_gravitonio_pos(self, *args):  # Define update_gravitonio_pos method
        self.image.pos = self.pos  # Update image position

    def affect_trajectory(self, obj):  # Define affect_trajectory method
        dx = self.center_x - obj.center_x  # Calculate dx
        dy = self.center_y - obj.center_y  # Calculate dy
        velocity_x, velocity_y = obj.velocity  # Get velocity

        distance = math.sqrt(dx ** 2 + dy ** 2)  # Calculate distance
        influence_radius = 200  # Set influence radius
        if distance < influence_radius:  # Check if distance is less than influence radius
            force = 5000 / (distance ** 2)  # Calculate force
            if self.effect == "repel":  # Check if effect is repel
                force = -force  # Invert force
            angle = math.atan2(dy, dx)  # Calculate angle
            velocity_x += force * math.cos(angle)  # Update velocity_x
            velocity_y += force * math.sin(angle)  # Update velocity_y

            obj.velocity = Vector(velocity_x, velocity_y)  # Set velocity

# Define the wormhole class
class Wormhole(Widget):  # Define Wormhole class inheriting from Widget
    def __init__(self, pos1, pos2, **kwargs):  # Initialize Wormhole
        super().__init__(**kwargs)  # Call the superclass initializer
        self.size = (100, 100)  # Set size
        self.pos1 = pos1  # Set pos1
        self.pos2 = pos2  # Set pos2
        with self.canvas:  # Add images to canvas
            self.image1 = Rectangle(source='wormhole.png', pos=self.pos1, size=self.size)  # Set image1
            self.image2 = Rectangle(source='wormhole.png', pos=self.pos2, size=self.size)  # Set image2
        self.bind(pos=self.update_wormhole_pos)  # Bind position update

    def update_wormhole_pos(self, *args):  # Define update_wormhole_pos method
        self.image1.pos = self.pos1  # Update image1 position
        self.image2.pos = self.pos2  # Update image2 position

    def transport(self, obj):  # Define transport method
        current_time = Clock.get_time()  # Get current time
        if hasattr(obj, 'last_transport_time'):  # Check if object has last_transport_time
            if current_time - obj.last_transport_time < 0.5:  # Check if transport cooldown is active
                return  # Return
        else:  # If object does not have last_transport_time
            obj.last_transport_time = 0  # Set last_transport_time to 0

        if self.collide_widget_with_circle(obj, self.image1):  # Check collision with image1
            offset = Vector(obj.center) - Vector(self.image1.pos) - Vector(self.size) / 2  # Calculate offset
            obj.center = Vector(self.image2.pos) + Vector(self.size) / 2 + offset  # Update object center
            obj.last_transport_time = current_time  # Update last_transport_time
        elif self.collide_widget_with_circle(obj, self.image2):  # Check collision with image2
            offset = Vector(obj.center) - Vector(self.image2.pos) - Vector(self.size) / 2  # Calculate offset
            obj.center = Vector(self.image1.pos) + Vector(self.size) / 2 + offset  # Update object center
            obj.last_transport_time = current_time  # Update last_transport_time

    def collide_widget_with_circle(self, obj, image):  # Define collide_widget_with_circle method
        radius = self.size[0] / 2  # Calculate radius
        center = Vector(image.pos) + Vector(radius, radius)  # Calculate center
        return Vector(obj.center).distance(center) <= radius  # Check collision with circular area

# MAIN WIDGET GAME

# Define the main game widget class
class GameWidget(Widget):  # Define GameWidget class inheriting from Widget
    def __init__(self, **kwargs):  # Initialize GameWidget
        super().__init__(**kwargs)  # Call the superclass initializer
        self.manager = None  # Initialize manager attribute
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)  # Request keyboard
        self._keyboard.bind(on_key_down=self._on_key_down)  # Bind key down event
        self._keyboard.bind(on_key_up=self._on_key_up)  # Bind key up event

        self.level = 1  # Initialize level
        self.max_level = 2  # Set max level
        self.target = None  # Initialize target

        with self.canvas:  # Add background and cannon image to canvas
            self.background = Rectangle(source=f"level_{self.level}_bg.png", pos=self.pos, size=Window.size)  # Set background image
            self.cannon_image = Rectangle(source="cannon anticorpo.png", pos=(20, 10), size=(250, 110))  # Set cannon image
            self.cannon_angle = 0  # Set cannon angle

        self.projectiles = []  # Initialize projectiles list
        self.lasers = []  # Initialize lasers list
        self.bombshells = []  # Initialize bombshells list
        self.obstacles = []  # Initialize obstacles list
        self.mirrors = []  # Initialize mirrors list
        self.elastonios = []  # Initialize elastonios list
        self.gravitonios = []  # Initialize gravitonios list
        self.perpetios = []  # Initialize perpetios list
        self.wormholes = []  # Initialize wormholes list
        self.pieces = []  # Initialize pieces list

        self.keysPressed = set()  # Initialize keysPressed set
        self.shooting_mode = 'projectile'  # Set shooting mode
        self.laser_on = False  # Set laser_on to False
        self.laser_start_time = None  # Initialize laser_start_time

        self.projectile_shoot_cooldown = 0.5  # Set projectile shoot cooldown
        self.bombshell_shoot_cooldown = 0.5  # Set bombshell shoot cooldown
        self.laser_shoot_cooldown = 0.5  # Set laser shoot cooldown
        self.last_projectile_shot_time = 0  # Initialize last projectile shot time
        self.last_bombshell_shot_time = 0  # Initialize last bombshell shot time
        self.last_shot_time = 0  # Initialize last shot time

        self.remaining_shots = 30  # Set remaining shots
        self.score = 0  # Initialize score

        self.score_label = Label(  # Create score label
            text=f"Score: {self.score}",  # Set label text
            font_size=24,  # Set font size
            color=(1, 1, 1, 1),  # Set color
            pos=(10, Window.height - 40),  # Set position
            size_hint=(None, None),  # Set size hint
            size=(200, 40),  # Set size
            font_name='TrueLies.ttf'  # Set font name
        )
        self.add_widget(self.score_label)  # Add score label to widget

        self.remaining_shots_label = Label(  # Create remaining shots label
            text=f"Shots Left: {self.remaining_shots}",  # Set label text
            font_size=24,  # Set font size
            color=(1, 1, 1, 1),  # Set color
            pos=(Window.width - 210, Window.height - 40),  # Set position
            size_hint=(None, None),  # Set size hint
            size=(200, 40),  # Set size
            font_name='TrueLies.ttf'  # Set font name
        )
        self.add_widget(self.remaining_shots_label)  # Add remaining shots label to widget

        self.create_obstacles()  # Create obstacles
        self.create_mirrors()  # Create mirrors
        self.create_elastonios()  # Create elastonios
        self.create_gravitonios()  # Create gravitonios
        self.create_perpetios()  # Create perpetios
        self.create_wormholes()  # Create wormholes

        self.target = Target(image_source=f"target_{self.level}.png")  # Create target
        self.add_widget(self.target)  # Add target to widget

        Clock.schedule_interval(self.move_step, 0)  # Schedule move_step method
        Clock.schedule_interval(self.update_projectiles, 1 / 60)  # Schedule update_projectiles method
        Clock.schedule_interval(self.update_lasers, 1 / 60)  # Schedule update_lasers method
        Clock.schedule_interval(self.update_bombshells, 1 / 60)  # Schedule update_bombshells method
        Clock.schedule_interval(self.update_pieces, 1 / 60)  # Schedule update_pieces method
        Clock.schedule_interval(self.update_obstacles, 1 / 60)  # Schedule update_obstacles method
        Clock.schedule_interval(self.update_score_label, 1 / 60)  # Schedule update_score_label method
        Clock.schedule_interval(self.update_remaining_shots_label, 1 / 60)  # Schedule update_remaining_shots_label method

        Window.bind(on_resize=self._update_bg_size)  # Bind resize event

    def start_music(self):  # Define start_music method
        if hasattr(self, 'sound') and self.sound:  # Check if sound attribute exists and is not None
            self.sound.stop()  # Stop sound
        self.sound = SoundLoader.load(f"level_{self.level}_music.mp3")  # Load level music
        if self.sound:  # Check if sound is loaded
            self.sound.loop = True  # Set sound to loop
            self.sound.play()  # Play sound

    def stop_music(self):  # Define stop_music method
        if hasattr(self, 'sound') and self.sound:  # Check if sound attribute exists and is not None
            self.sound.stop()  # Stop sound

        Window.bind(mouse_pos=self.update_cannon)  # Bind mouse position update
        Window.bind(on_resize=self._update_bg_size)  # Bind resize event

    def _update_bg_size(self, *args):  # Define _update_bg_size method
        self.background.size = Window.size  # Update background size
        self.score_label.pos = (10, Window.height - 40)  # Update score label position
        self.remaining_shots_label.pos = (Window.width - 210, Window.height - 40)  # Update remaining shots label position

    def update_score(self, points):  # Define update_score method
        self.score += points  # Update score

    def update_score_label(self, dt):  # Define update_score_label method
        self.score_label.text = f"Score: {self.score}"  # Update score label text

    def update_remaining_shots_label(self, dt):  # Define update_remaining_shots_label method
        self.remaining_shots_label.text = f"Shots Left: {self.remaining_shots}"  # Update remaining shots label text

    def decrement_shots(self):  # Define decrement_shots method
        self.remaining_shots -= 1  # Decrement remaining shots
        self.update_remaining_shots_label(0)  # Update remaining shots label
        if self.remaining_shots <= 0:  # Check if remaining shots are zero
            self.show_game_over_popup()  # Show game over popup

    def _on_keyboard_closed(self):  # Define _on_keyboard_closed method
        self._keyboard.unbind(on_key_down=self._on_key_down)  # Unbind key down event
        self._keyboard.unbind(on_key_up=self._on_key_up)  # Unbind key up event
        self._keyboard = None  # Set _keyboard to None

    def _on_key_down(self, keyboard, keycode, text, modifiers):  # Define _on_key_down method
        self.keysPressed.add(text)  # Add key to keysPressed
        if text == 'w':  # Check if key is 'w'
            self.shooting_mode = 'projectile'  # Set shooting mode to projectile
        elif text == 'x':  # Check if key is 'x'
            self.shooting_mode = 'laser'  # Set shooting mode to laser
        elif text == 's':  # Check if key is 's'
            self.shooting_mode = 'bombshell'  # Set shooting mode to bombshell
        elif text == 'esc':  # Check if key is 'esc'
            self.show_pause_menu()  # Show pause menu

    def show_pause_menu(self):  # Define show_pause_menu method
        pause_menu = PauseMenuPopup(game_widget=self)  # Create pause menu popup
        pause_menu.open()  # Open pause menu

    def _on_key_up(self, keyboard, keycode):  # Define _on_key_up method
        text = keycode[1]  # Get key text
        if text in self.keysPressed:  # Check if key is in keysPressed
            self.keysPressed.remove(text)  # Remove key from keysPressed

    def move_step(self, dt):  # Define move_step method
        currentx = self.cannon_image.pos[0]  # Get current x position
        currenty = self.cannon_image.pos[1]  # Get current y position

        step_size = 100 * dt  # Set step size

        if "a" in self.keysPressed:  # Check if 'a' key is pressed
            currentx -= step_size  # Move left
        if "d" in self.keysPressed:  # Check if 'd' key is pressed
            currentx += step_size  # Move right

        screen_width = Window.width  # Get screen width
        max_x = screen_width * 1 / 2 - self.cannon_image.size[0]  # Calculate max x position
        if currentx < 0:  # Check if current x is less than 0
            currentx = 0  # Set current x to 0
        elif currentx > max_x:  # Check if current x is greater than max x
            currentx = max_x  # Set current x to max x

        self.cannon_image.pos = (currentx, currenty)  # Update cannon position
        self.update_cannon(Window, Window.mouse_pos)  # Update cannon

    def update_cannon(self, window, mouse_pos):  # Define update_cannon method
        self.canvas.clear()  # Clear canvas
        with self.canvas:  # Add background and cannon image to canvas
            self.background = Rectangle(source=f"level_{self.level}_bg.png", pos=self.pos, size=Window.size)  # Set background image
            for obstacle in self.obstacles:  # Iterate over obstacles
                self.canvas.add(obstacle.rectangle)  # Add obstacle to canvas
            for mirror in self.mirrors:  # Iterate over mirrors
                self.canvas.add(mirror.mir)  # Add mirror to canvas
            for elastonio in self.elastonios:  # Iterate over elastonios
                self.canvas.add(elastonio.image)  # Add elastonio to canvas
            for perpetio in self.perpetios:  # Iterate over perpetios
                self.canvas.add(perpetio.image)  # Add perpetio to canvas
            for wormhole in self.wormholes:  # Iterate over wormholes
                self.canvas.add(wormhole.image1)  # Add wormhole image1 to canvas
                self.canvas.add(wormhole.image2)  # Add wormhole image2 to canvas
            for projectile in self.projectiles:  # Iterate over projectiles
                self.canvas.add(projectile.image)  # Add projectile to canvas
            for laser in self.lasers:  # Iterate over lasers
                self.canvas.add(laser.laser)  # Add laser to canvas
            for bombshell in self.bombshells:  # Iterate over bombshells
                self.canvas.add(bombshell.image)  # Add bombshell to canvas
            for piece in self.pieces:  # Iterate over pieces
                self.canvas.add(piece)  # Add piece to canvas
            for gravitonio in self.gravitonios:  # Iterate over gravitonios
                self.canvas.add(gravitonio.image)  # Add gravitonio to canvas
            self.canvas.add(self.target.image)  # Add target image to canvas
            self.canvas.add(self.score_label.canvas)  # Add score label to canvas
            self.canvas.add(self.remaining_shots_label.canvas)  # Add remaining shots label to canvas

            cannon_x = self.cannon_image.pos[0] + self.cannon_image.size[0] / 2  # Calculate cannon x position
            cannon_y = self.cannon_image.pos[1] + self.cannon_image.size[1] / 2  # Calculate cannon y position
            mouse_x, mouse_y = mouse_pos  # Get mouse position
            angle = math.atan2(mouse_y - cannon_y, mouse_x - cannon_x)  # Calculate angle
            self.cannon_angle = math.degrees(angle)  # Set cannon angle

            with self.canvas:  # Add rotated cannon image to canvas
                PushMatrix()  # Push matrix
                Rotate(angle=self.cannon_angle, origin=(cannon_x, cannon_y))  # Rotate
                self.cannon_image = Rectangle(source="cannon anticorpo.png", pos=self.cannon_image.pos, size=self.cannon_image.size)  # Set cannon image
                PopMatrix()  # Pop matrix

    def on_touch_down(self, touch):  # Define on_touch_down method
        if self.remaining_shots > 0:  # Check if remaining shots are greater than 0
            if self.shooting_mode == 'projectile':  # Check if shooting mode is projectile
                self.shoot_projectile(touch)  # Shoot projectile
            elif self.shooting_mode == 'laser':  # Check if shooting mode is laser
                self.shoot_laser(touch)  # Shoot laser
            elif self.shooting_mode == 'bombshell':  # Check if shooting mode is bombshell
                self.shoot_bombshell(touch)  # Shoot bombshell
            self.decrement_shots()  # Decrement remaining shots
        else:  # If no remaining shots
            self.show_game_over_popup()  # Show game over popup

    def on_touch_move(self, touch):  # Define on_touch_move method
        pass  # Pass

    def on_touch_up(self, touch):  # Define on_touch_up method
        pass  # Pass

    def shoot_projectile(self, touch):  # Define shoot_projectile method
        current_time = time.time()  # Get current time
        if current_time - self.last_projectile_shot_time >= self.projectile_shoot_cooldown:  # Check if cooldown is over
            cannon_x = self.cannon_image.pos[0] + self.cannon_image.size[0] / 2  # Calculate cannon x position
            cannon_y = self.cannon_image.pos[1] + self.cannon_image.size[1] / 2  # Calculate cannon y position
            mouse_x, mouse_y = touch.pos  # Get touch position
            angle = math.atan2(mouse_y - cannon_y, mouse_x - cannon_x)  # Calculate angle

            length = 100  # Set length
            barrel_end_x = cannon_x + length * math.cos(angle)  # Calculate barrel end x position
            barrel_end_y = cannon_y + length * math.sin(angle)  # Calculate barrel end y position

            distance = Vector(mouse_x - cannon_x, mouse_y - cannon_y).length()  # Calculate distance
            max_distance = 1000  # Set max distance
            force = min(distance / max_distance, 1) * 700  # Calculate force

            velocity_x = force * math.cos(angle)  # Calculate velocity_x
            velocity_y = force * math.sin(angle)  # Calculate velocity_y

            projectile = Projectile()  # Create projectile
            projectile.pos = (barrel_end_x - projectile.size[0] / 2, barrel_end_y - projectile.size[1] / 2)  # Set projectile position
            projectile.velocity = Vector(velocity_x, velocity_y)  # Set projectile velocity
            self.projectiles.append(projectile)  # Add projectile to list
            self.add_widget(projectile)  # Add projectile to widget
            self.last_projectile_shot_time = current_time  # Update last shot time

    def update_projectiles(self, dt):  # Define update_projectiles method
        gravity = Vector(0, -98.1)  # Set gravity
        new_projectiles = []  # Initialize new projectiles list
        projectiles_to_remove = []  # Initialize projectiles to remove list

        for projectile in self.projectiles:  # Iterate over projectiles
            projectile.velocity += gravity * dt  # Update velocity
            projectile.pos = Vector(*projectile.pos) + projectile.velocity * dt  # Update position

            for gravitonio in self.gravitonios:  # Iterate over gravitonios
                gravitonio.affect_trajectory(projectile)  # Affect projectile trajectory

            for elastonio in self.elastonios:  # Iterate over elastonios
                if elastonio.collide_with_projectile(projectile):  # Check collision with elastonio
                    projectile.velocity = -projectile.velocity  # Invert velocity
                    break  # Break loop

            for wormhole in self.wormholes:  # Iterate over wormholes
                wormhole.transport(projectile)  # Transport projectile

            if self.target.collide_widget(projectile):  # Check collision with target
                self.target.hit()  # Hit target
                self.update_score(10)  # Update score
                projectiles_to_remove.append(projectile)  # Add projectile to remove list
            elif projectile.y > 0:  # Check if projectile is in bounds
                new_projectiles.append(projectile)  # Add projectile to new projectiles list
            else:  # If projectile is out of bounds
                projectiles_to_remove.append(projectile)  # Add projectile to remove list

            for obstacle in self.obstacles:  # Iterate over obstacles
                if (obstacle.rectangle.pos[0] < projectile.x < obstacle.rectangle.pos[0] + obstacle.rectangle.size[0] and
                        obstacle.rectangle.pos[1] < projectile.y < obstacle.rectangle.pos[1] + obstacle.rectangle.size[1]):  # Check collision with obstacle
                    projectiles_to_remove.append(projectile)  # Add projectile to remove list
                    self.disintegrate_obstacle(obstacle.rectangle)  # Disintegrate obstacle
                    self.canvas.remove(obstacle.rectangle)  # Remove obstacle from canvas
                    self.obstacles.remove(obstacle)  # Remove obstacle from list
                    break  # Break loop

            for perpetio in self.perpetios:  # Iterate over perpetios
                if perpetio.collide_widget(projectile):  # Check collision with perpetio
                    projectiles_to_remove.append(projectile)  # Add projectile to remove list
                    break  # Break loop

            for mirror in self.mirrors:  # Iterate over mirrors
                if mirror.collide_widget(projectile):  # Check collision with mirror
                    projectiles_to_remove.append(projectile)  # Add projectile to remove list
                    break  # Break loop

        for projectile in projectiles_to_remove:  # Iterate over projectiles to remove
            self.remove_widget(projectile)  # Remove projectile from widget
            if projectile in new_projectiles:  # Check if projectile is in new projectiles list
                new_projectiles.remove(projectile)  # Remove projectile from list

        self.projectiles = new_projectiles  # Update projectiles list

    def shoot_bombshell(self, touch):  # Define shoot_bombshell method
        current_time = time.time()  # Get current time
        if current_time - self.last_bombshell_shot_time >= self.bombshell_shoot_cooldown:  # Check if cooldown is over
            cannon_x = self.cannon_image.pos[0] + self.cannon_image.size[0] / 2  # Calculate cannon x position
            cannon_y = self.cannon_image.pos[1] + self.cannon_image.size[1] / 2  # Calculate cannon y position
            mouse_x, mouse_y = touch.pos  # Get touch position
            angle = math.atan2(mouse_y - cannon_y, mouse_x - cannon_x)  # Calculate angle
            distance = Vector(mouse_x - cannon_x, mouse_y - cannon_y).length()  # Calculate distance

            max_distance = 1000  # Set max distance
            force = min(distance / max_distance, 1) * 450  # Calculate force

            velocity_x = force * math.cos(angle)  # Calculate velocity_x
            velocity_y = force * math.sin(angle)  # Calculate velocity_y

            bombshell = Bombshell()  # Create bombshell
            bombshell.angle = angle  # Set angle
            bombshell.speed = force  # Set speed
            bombshell.velocity_x = velocity_x  # Set velocity_x
            bombshell.velocity_y = velocity_y  # Set velocity_y
            bombshell.pos = [self.cannon_image.pos[0] + self.cannon_image.size[0] / 2 + 100 * math.cos(bombshell.angle) - bombshell.size[0] / 2,
                            self.cannon_image.pos[1] + self.cannon_image.size[1] / 2 + 100 * math.sin(bombshell.angle) - bombshell.size[1] / 2]  # Set position
            self.bombshells.append(bombshell)  # Add bombshell to list
            self.add_widget(bombshell)  # Add bombshell to widget
            self.last_bombshell_shot_time = current_time  # Update last shot time

    def update_bombshells(self, dt):  # Define update_bombshells method
        new_bombshells = []  # Initialize new bombshells list
        bombshells_to_remove = []  # Initialize bombshells to remove list

        for bombshell in self.bombshells:  # Iterate over bombshells
            if not bombshell.exploded:  # Check if bombshell has not exploded
                for gravitonio in self.gravitonios:  # Iterate over gravitonios
                    bombshell.affect_trajectory(gravitonio)  # Affect bombshell trajectory

                bombshell.trajectory(dt)  # Update trajectory
                bombshell.update_graphics()  # Update graphics

                for elastonio in self.elastonios:  # Iterate over elastonios
                    if elastonio.collide_with_bombshell(bombshell):  # Check collision with elastonio
                        bombshell.velocity_x = -bombshell.velocity_x  # Invert velocity_x
                        bombshell.velocity_y = -bombshell.velocity_y  # Invert velocity_y
                        break  # Break loop

                for wormhole in self.wormholes:  # Iterate over wormholes
                    wormhole.transport(bombshell)  # Transport bombshell

                if self.target.collide_widget(bombshell):  # Check collision with target
                    self.target.hit()  # Hit target
                    self.update_score(20)  # Update score
                    bombshells_to_remove.append(bombshell)  # Add bombshell to remove list
                elif bombshell.y <= 0:  # Check if bombshell is out of bounds
                    bombshell.explode(0)  # Explode bombshell
                    bombshells_to_remove.append(bombshell)  # Add bombshell to remove list
                else:  # If bombshell is in bounds
                    new_bombshells.append(bombshell)  # Add bombshell to new bombshells list

                for obstacle in self.obstacles:  # Iterate over obstacles
                    if (obstacle.rectangle.pos[0] < bombshell.x < obstacle.rectangle.pos[0] + obstacle.rectangle.size[0] and
                        obstacle.rectangle.pos[1] < bombshell.y < obstacle.rectangle.pos[1] + obstacle.rectangle.size[1]):  # Check collision with obstacle
                        self.disintegrate_obstacle(obstacle.rectangle)  # Disintegrate obstacle
                        self.canvas.remove(obstacle.rectangle)  # Remove obstacle from canvas
                        self.obstacles.remove(obstacle)  # Remove obstacle from list
                        break  # Break loop

                for perpetio in self.perpetios:  # Iterate over perpetios
                    if perpetio.collide_widget(bombshell):  # Check collision with perpetio
                        bombshell.explode(0)  # Explode bombshell
                        bombshells_to_remove.append(bombshell)  # Add bombshell to remove list
                        break  # Break loop

                for mirror in self.mirrors:  # Iterate over mirrors
                    if mirror.collide_widget(bombshell):  # Check collision with mirror
                        bombshell.explode(0)  # Explode bombshell
                        bombshells_to_remove.append(bombshell)  # Add bombshell to remove list
                        break  # Break loop

        for bombshell in bombshells_to_remove:  # Iterate over bombshells to remove
            if bombshell in self.bombshells:  # Check if bombshell is in bombshells list
                self.bombshells.remove(bombshell)  # Remove bombshell from list
            self.remove_widget(bombshell)  # Remove bombshell from widget

        self.bombshells = new_bombshells  # Update bombshells list

    def shoot_laser(self, touch):  # Define shoot_laser method
        current_time = time.time()  # Get current time
        if current_time - self.last_shot_time >= self.laser_shoot_cooldown:  # Check if cooldown is over
            laser = Laser()  # Create laser
            laser.angle = self.cannon_angle  # Set angle
            laser.pos = [self.cannon_image.pos[0] + self.cannon_image.size[0] / 2 + 100 * math.cos(math.radians(self.cannon_angle)) - laser.size[0] / 2,
                         self.cannon_image.pos[1] + self.cannon_image.size[1] / 2 + 100 * math.sin(math.radians(self.cannon_angle)) - laser.size[1] / 2]  # Set position
            self.lasers.append(laser)  # Add laser to list
            self.add_widget(laser)  # Add laser to widget
            self.last_shot_time = current_time  # Update last shot time

    def update_lasers(self, dt):  # Define update_lasers method
        lasers_to_remove = []  # Initialize lasers to remove list
        for laser in self.lasers:  # Iterate over lasers
            laser.trajectory()  # Update trajectory
            laser.update_laser_pos()  # Update laser position
            if laser.x > Window.width or laser.x < 0 or laser.y > Window.height or laser.y < 0:  # Check if laser is out of bounds
                lasers_to_remove.append(laser)  # Add laser to remove list
            else:  # If laser is in bounds
                for obstacle in self.obstacles:  # Iterate over obstacles
                    if (obstacle.rectangle.pos[0] < laser.x < obstacle.rectangle.pos[0] + obstacle.rectangle.size[0] and
                            obstacle.rectangle.pos[1] < laser.y < obstacle.rectangle.pos[1] + obstacle.rectangle.size[1]):  # Check collision with obstacle
                        lasers_to_remove.append(laser)  # Add laser to remove list
                        self.disintegrate_obstacle(obstacle.rectangle)  # Disintegrate obstacle
                        self.canvas.remove(obstacle.rectangle)  # Remove obstacle from canvas
                        self.obstacles.remove(obstacle)  # Remove obstacle from list
                        break  # Break loop
                for elastonio in self.elastonios:  # Iterate over elastonios
                    if elastonio.collide_with_laser(laser):  # Check collision with elastonio
                        lasers_to_remove.append(laser)  # Add laser to remove list
                        self.canvas.remove(elastonio.image)  # Remove elastonio from canvas
                        self.elastonios.remove(elastonio)  # Remove elastonio from list
                        break  # Break loop

                for wormhole in self.wormholes:  # Iterate over wormholes
                    wormhole.transport(laser)  # Transport laser

                if self.target.collide_widget(laser):  # Check collision with target
                    self.target.hit()  # Hit target
                    self.update_score(5)  # Update score
                    lasers_to_remove.append(laser)  # Add laser to remove list
                    break  # Break loop

                for perpetio in self.perpetios:  # Iterate over perpetios
                    if perpetio.collide_widget(laser):  # Check collision with perpetio
                        lasers_to_remove.append(laser)  # Add laser to remove list
                        break  # Break loop
                for mirror in self.mirrors:  # Iterate over mirrors
                    if mirror.collide_with_laser(laser):  # Check collision with mirror
                        mirror.reflect_laser(laser)  # Reflect laser

        for laser in lasers_to_remove:  # Iterate over lasers to remove
            if laser in self.lasers:  # Check if laser is in lasers list
                self.lasers.remove(laser)  # Remove laser from list
            self.remove_widget(laser)  # Remove laser from widget

    def update_pieces(self, dt):  # Define update_pieces method
        for piece in self.pieces:  # Iterate over pieces
            piece.pos = (piece.pos[0], piece.pos[1] - 2)  # Update position

    def disintegrate_obstacle(self, obstacle):  # Define disintegrate_obstacle method
        x, y = obstacle.pos  # Get obstacle position
        width, height = obstacle.size  # Get obstacle size
        num_pieces = 20  # Set number of pieces

        for _ in range(num_pieces):  # Iterate over number of pieces
            piece_x = random.randint(int(x), int(x + width))  # Calculate piece x position
            piece_y = random.randint(int(y), int(y + height))  # Calculate piece y position
            piece_size = (5, 5)  # Set piece size
            piece = Rectangle(pos=(piece_x, piece_y), size=piece_size, source="obstacle piece.png")  # Create piece
            self.pieces.append(piece)  # Add piece to list
            self.canvas.add(piece)  # Add piece to canvas

        Clock.schedule_once(lambda dt: self.remove_disintegration_pieces(), 0.5)  # Schedule removal of pieces

    def remove_disintegration_pieces(self, dt=None):  # Define remove_disintegration_pieces method
        for piece in self.pieces:  # Iterate over pieces
            if piece in self.canvas.children:  # Check if piece is in canvas
                self.canvas.remove(piece)  # Remove piece from canvas
        self.pieces.clear()  # Clear pieces list

    def create_obstacles(self):  # Define create_obstacles method
        try:  # Try to create obstacles
            obstacle_counts = [2, 4]  # Set obstacle counts
            num_obstacles = obstacle_counts[self.level - 1]  # Get number of obstacles
            for i in range(num_obstacles):  # Iterate over number of obstacles
                while True:  # Loop until obstacle is created
                    x_min = int(Window.width * 1 / 3)  # Set x min position
                    x_max = int(Window.width * 0.9)  # Set x max position
                    y_min = int(Window.height * 0.2)  # Set y min position
                    y_max = int(Window.height * 0.8)  # Set y max position

                    if x_max <= x_min:  # Check if x max is less than or equal to x min
                        x_max = x_min + 1  # Set x max
                    if y_max <= y_min:  # Check if y max is less than or equal to y min
                        y_max = y_min + 1  # Set y max

                    x_pos = random.randint(x_min, x_max - 1)  # Calculate x position
                    y_pos = random.randint(y_min, y_max - 1)  # Calculate y position

                    rectangle = Rectangle(source="obstacle.png", pos=(x_pos, y_pos), size=(50, 50))  # Create rectangle
                    if not self.check_overlap((x_pos, y_pos), rectangle.size):  # Check if no overlap
                        obstacle = Obstacle(rectangle, random.randint(5, 20), random.uniform(1, 3))  # Create obstacle
                        self.obstacles.append(obstacle)  # Add obstacle to list
                        self.canvas.add(obstacle.rectangle)  # Add obstacle to canvas
                        break  # Break loop
        except Exception as e:  # Handle exception
            logger.error(f'Error creating obstacles: {e}')  # Log error

    def create_mirrors(self):  # Define create_mirrors method
        mirror_counts = [1, 2]  # Set mirror counts
        num_mirrors = mirror_counts[self.level - 1]  # Get number of mirrors
        for i in range(num_mirrors):  # Iterate over number of mirrors
            while True:  # Loop until mirror is created
                x_min = int(Window.width * 1 / 3)  # Set x min position
                x_max = int(Window.width * 0.9)  # Set x max position
                y_min = int(Window.height * 0.1)  # Set y min position
                y_max = int(Window.height * 0.9)  # Set y max position

                if x_max <= x_min:  # Check if x max is less than or equal to x min
                    x_max = x_min + 1  # Set x max
                if y_max <= y_min:  # Check if y max is less than or equal to y min
                    y_max = y_min + 1  # Set y max

                x_pos = random.randint(x_min, x_max - 1)  # Calculate x position
                y_pos = random.randint(y_min, y_max - 1)  # Calculate y position

                mirror = MirrorBulletproof(pos=(x_pos, y_pos))  # Create mirror
                if not self.check_overlap((x_pos, y_pos), mirror.size):  # Check if no overlap
                    self.mirrors.append(mirror)  # Add mirror to list
                    self.add_widget(mirror)  # Add mirror to widget
                    break  # Break loop

    def create_elastonios(self):  # Define create_elastonios method
        try:  # Try to create elastonios
            elastonio_counts = [1, 2]  # Set elastonio counts
            num_elastonios = elastonio_counts[self.level - 1]  # Get number of elastonios
            for i in range(num_elastonios):  # Iterate over number of elastonios
                while True:  # Loop until elastonio is created
                    x_min = int(Window.width * 1 / 3)  # Set x min position
                    x_max = int(Window.width * 0.9)  # Set x max position
                    y_min = int(Window.height * 0.2)  # Set y min position
                    y_max = int(Window.height * 0.8)  # Set y max position

                    if x_max <= x_min:  # Check if x max is less than or equal to x min
                        x_max = x_min + 1  # Set x max
                    if y_max <= y_min:  # Check if y max is less than or equal to y min
                        y_max = y_min + 1  # Set y max

                    x_pos = random.randint(x_min, x_max - 1)  # Calculate x position
                    y_pos = random.randint(y_min, y_max - 1)  # Calculate y position

                    elastonio = Elastonio(pos=(x_pos, y_pos))  # Create elastonio
                    if not self.check_overlap((x_pos, y_pos), elastonio.size):  # Check if no overlap
                        self.elastonios.append(elastonio)  # Add elastonio to list
                        self.add_widget(elastonio)  # Add elastonio to widget
                        break  # Break loop
            logger.debug('Elastonios created successfully')  # Log success
        except Exception as e:  # Handle exception
            logger.error(f'Error creating elastonios: {e}')  # Log error

    def create_gravitonios(self):  # Define create_gravitonios method
        try:  # Try to create gravitonios
            gravitonio_counts = [1, 2]  # Set gravitonio counts
            num_gravitonios = gravitonio_counts[self.level - 1]  # Get number of gravitonios
            for i in range(num_gravitonios):  # Iterate over number of gravitonios
                while True:  # Loop until gravitonio is created
                    x_min = int(Window.width * 1 / 3)  # Set x min position
                    x_max = int(Window.width * 0.9)  # Set x max position
                    y_min = int(Window.height * 0.2)  # Set y min position
                    y_max = int(Window.height * 0.8)  # Set y max position

                    if x_max <= x_min:  # Check if x max is less than or equal to x min
                        x_max = x_min + 1  # Set x max
                    if y_max <= y_min:  # Check if y max is less than or equal to y min
                        y_max = y_min + 1  # Set y max

                    x_pos = random.randint(x_min, x_max - 1)  # Calculate x position
                    y_pos = random.randint(y_min, y_max - 1)  # Calculate y position

                    gravitonio = Gravitonio(pos=(x_pos, y_pos))  # Create gravitonio
                    if not self.check_overlap((x_pos, y_pos), gravitonio.size):  # Check if no overlap
                        self.gravitonios.append(gravitonio)  # Add gravitonio to list
                        self.add_widget(gravitonio)  # Add gravitonio to widget
                        break  # Break loop
            logger.debug('Gravitonios created successfully')  # Log success
        except Exception as e:  # Handle exception
            logger.error(f'Error creating gravitonios: {e}')  # Log error

    def create_perpetios(self):  # Define create_perpetios method
        try:  # Try to create perpetios
            logger.debug('Creating perpetios')  # Log creation
            perpetio_counts = [1, 2]  # Set perpetio counts
            num_perpetios = perpetio_counts[self.level - 1]  # Get number of perpetios
            created_perpetios = 0  # Initialize created perpetios
            max_attempts = 1000 * num_perpetios  # Set max attempts

            while created_perpetios < num_perpetios and max_attempts > 0:  # Loop until perpetios are created
                max_attempts -= 1  # Decrement max attempts
                x_min = int(Window.width * 1 / 3)  # Set x min position
                x_max = int(Window.width * 0.9)  # Set x max position
                y_min = int(Window.height * 0.2)  # Set y min position
                y_max = int(Window.height * 0.8)  # Set y max position

                if x_max <= x_min:  # Check if x max is less than or equal to x min
                    x_max = x_min + 1  # Set x max
                if y_max <= y_min:  # Check if y max is less than or equal to y min
                    y_max = y_min + 1  # Set y max

                x_pos = random.randint(x_min, x_max - 1)  # Calculate x position
                y_pos = random.randint(y_min, y_max - 1)  # Calculate y position

                perpetio = Perpetio(image_source="perpetio.png", pos=(x_pos, y_pos))  # Create perpetio
                if not self.check_overlap((x_pos, y_pos), perpetio.size):  # Check if no overlap
                    self.perpetios.append(perpetio)  # Add perpetio to list
                    self.add_widget(perpetio)  # Add perpetio to widget
                    created_perpetios += 1  # Increment created perpetios
                    logger.debug(f'Created perpetio at position ({x_pos}, {y_pos})')  # Log creation

            if created_perpetios == num_perpetios:  # Check if all perpetios are created
                logger.debug('Perpetios created successfully')  # Log success
            else:  # If not all perpetios are created
                logger.warning('Could not create the desired number of perpetios')  # Log warning

        except Exception as e:  # Handle exception
            logger.error(f'Error creating perpetios: {e}')  # Log error

    def create_wormholes(self):  # Define create_wormholes method
        try:  # Try to create wormholes
            logger.debug('Creating wormholes')  # Log creation
            num_wormholes = 1  # Set number of wormholes
            created_wormholes = 0  # Initialize created wormholes
            max_attempts = 1000 * num_wormholes  # Set max attempts

            while created_wormholes < num_wormholes and max_attempts > 0:  # Loop until wormholes are created
                max_attempts -= 1  # Decrement max attempts
                x1 = random.randint(int(Window.width * 1 / 3), int(Window.width * 0.9) - 1)  # Calculate x1 position
                y1 = random.randint(int(Window.height * 0.2), int(Window.height * 0.8) - 1)  # Calculate y1 position
                x2 = random.randint(int(Window.width * 1 / 3), int(Window.width * 0.9) - 1)  # Calculate x2 position
                y2 = random.randint(int(Window.height * 0.2), int(Window.height * 0.8) - 1)  # Calculate y2 position

                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # Calculate distance
                if distance >= 300 and not self.check_overlap((x1, y1), (50, 50)) and not self.check_overlap((x2, y2), (50, 50)):  # Check if no overlap
                    wormhole = Wormhole(pos1=(x1, y1), pos2=(x2, y2))  # Create wormhole
                    self.wormholes.append(wormhole)  # Add wormhole to list
                    self.canvas.add(wormhole.image1)  # Add wormhole image1 to canvas
                    self.canvas.add(wormhole.image2)  # Add wormhole image2 to canvas
                    created_wormholes += 1  # Increment created wormholes
                    logger.debug(f'Created wormhole from ({x1}, {y1}) to ({x2}, {y2})')  # Log creation

            if created_wormholes == num_wormholes:  # Check if all wormholes are created
                logger.debug('Wormholes created successfully')  # Log success
            else:  # If not all wormholes are created
                logger.warning('Could not create the desired number of wormholes')  # Log warning

        except Exception as e:  # Handle exception
            logger.error(f'Error creating wormholes: {e}')  # Log error

    def check_overlap(self, pos, size):  # Define check_overlap method
        radius = 150  # Set radius
        for obstacle in getattr(self, 'obstacles', []):  # Iterate over obstacles
            if Vector(pos).distance(Vector(obstacle.rectangle.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for mirror in getattr(self, 'mirrors', []):  # Iterate over mirrors
            if Vector(pos).distance(Vector(mirror.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for elastonio in getattr(self, 'elastonios', []):  # Iterate over elastonios
            if Vector(pos).distance(Vector(elastonio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for gravitonio in getattr(self, 'gravitonios', []):  # Iterate over gravitonios
            if Vector(pos).distance(Vector(gravitonio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for perpetio in getattr(self, 'perpetios', []):  # Iterate over perpetios
            if Vector(pos).distance(Vector(perpetio.pos)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        for wormhole in getattr(self, 'wormholes', []):  # Iterate over wormholes
            if Vector(pos).distance(Vector(wormhole.pos1)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
            if Vector(pos).distance(Vector(wormhole.pos2)) < radius + max(size[0], size[1]):  # Check distance
                return True  # Return True
        return False  # Return False

    def level_up(self):  # Define level_up method
        logger.debug('GameWidget: Level up triggered')  # Log level up
        if self.level < self.max_level:  # Check if level is less than max level
            self.level += 1  # Increment level
            self.clear_level()  # Clear level
            self.start_next_level()  # Start next level
        else:  # If level is equal to max level
            self.show_victory_popup()  # Show victory popup

    def start_next_level(self):  # Define start_next_level method
        if self.level > self.max_level:  # Check if level is greater than max level
            return  # Return

        logger.debug(f'Starting level {self.level}')  # Log level start
        try:  # Try to start next level
            self.clear_level()  # Clear level

            logger.debug('Creating obstacles')  # Log creation
            self.create_obstacles()  # Create obstacles
            logger.debug('Creating mirrors')  # Log creation
            self.create_mirrors()  # Create mirrors
            logger.debug('Creating elastonios')  # Log creation
            self.create_elastonios()  # Create elastonios
            logger.debug('Creating gravitonios')  # Log creation
            self.create_gravitonios()  # Create gravitonios
            logger.debug('Creating perpetios')  # Log creation
            self.create_perpetios()  # Create perpetios
            logger.debug('Creating wormholes')  # Log creation
            self.create_wormholes()  # Create wormholes

            logger.debug('Adding target')  # Log addition
            if self.target:  # Check if target exists
                if self.target in self.children:  # Check if target is in children
                    self.remove_widget(self.target)  # Remove target
            self.target = Target(image_source=f"target_{self.level}.png")  # Create target
            self.add_widget(self.target)  # Add target to widget

            self.show_level_popup()  # Show level popup

            logger.debug('Stopping previous music and starting new level music')  # Log music update
            self.stop_music()  # Stop music
            self.sound = SoundLoader.load(f"level_{self.level}_music.mp3")  # Load level music
            if self.sound:  # Check if sound is loaded
                self.sound.loop = True  # Set sound to loop
                self.sound.play()  # Play sound

            self.remaining_shots = 30  # Set remaining shots
            logger.debug(f'Level {self.level} started successfully')  # Log success

        except Exception as e:  # Handle exception
            logger.error(f'Error starting level {self.level}: {e}')  # Log error

    def safe_remove_widget(self, widget):  # Define safe_remove_widget method
        try:  # Try to remove widget
            self.remove_widget(widget)  # Remove widget
        except Exception as e:  # Handle exception
            Logger.error(f"Error removing widget: {e}")  # Log error

    def safe_remove_canvas(self, item):  # Define safe_remove_canvas method
        try:  # Try to remove canvas item
            self.canvas.remove(item)  # Remove canvas item
        except Exception as e:  # Handle exception
            Logger.error(f"Error removing canvas item: {e}")  # Log error

    def clear_level(self):  # Define clear_level method
        logger.debug('Clearing level')  # Log clearing

        for obstacle in self.obstacles:  # Iterate over obstacles
            if obstacle.rectangle in self.canvas.children:  # Check if obstacle is in canvas
                self.canvas.remove(obstacle.rectangle)  # Remove obstacle from canvas
        self.obstacles.clear()  # Clear obstacles list

        for mirror in self.mirrors:  # Iterate over mirrors
            if mirror in self.canvas.children:  # Check if mirror is in canvas
                self.remove_widget(mirror)  # Remove mirror from widget
        self.mirrors.clear()  # Clear mirrors list

        for elastonio in self.elastonios:  # Iterate over elastonios
            if elastonio in self.children:  # Check if elastonio is in children
                self.remove_widget(elastonio)  # Remove elastonio from widget
        self.elastonios.clear()  # Clear elastonios list

        for gravitonio in self.gravitonios:  # Iterate over gravitonios
            if gravitonio in self.children:  # Check if gravitonio is in children
                self.remove_widget(gravitonio)  # Remove gravitonio from widget
        self.gravitonios.clear()  # Clear gravitonios list

        for perpetio in self.perpetios:  # Iterate over perpetios
            if perpetio in self.children:  # Check if perpetio is in children
                self.remove_widget(perpetio)  # Remove perpetio from widget
        self.perpetios.clear()  # Clear perpetios list

        for wormhole in self.wormholes:  # Iterate over wormholes
            if wormhole.image1 in self.canvas.children:  # Check if wormhole image1 is in canvas
                self.canvas.remove(wormhole.image1)  # Remove wormhole image1 from canvas
            if wormhole.image2 in self.canvas.children:  # Check if wormhole image2 is in canvas
                self.canvas.remove(wormhole.image2)  # Remove wormhole image2 from canvas
        self.wormholes.clear()  # Clear wormholes list

        for projectile in self.projectiles:  # Iterate over projectiles
            if projectile in self.children:  # Check if projectile is in children
                self.remove_widget(projectile)  # Remove projectile from widget
        self.projectiles.clear()  # Clear projectiles list

        for laser in self.lasers:  # Iterate over lasers
            if laser in self.children:  # Check if laser is in children
                self.remove_widget(laser)  # Remove laser from widget
        self.lasers.clear()  # Clear lasers list

        for bombshell in self.bombshells:  # Iterate over bombshells
            if bombshell in self.children:  # Check if bombshell is in children
                self.remove_widget(bombshell)  # Remove bombshell from widget
        self.bombshells.clear()  # Clear bombshells list

        for piece in self.pieces:  # Iterate over pieces
            if piece in self.canvas.children:  # Check if piece is in canvas
                self.canvas.remove(piece)  # Remove piece from canvas
        self.pieces.clear()  # Clear pieces list

        if self.target:  # Check if target exists
            if self.target in self.children:  # Check if target is in children
                self.remove_widget(self.target)  # Remove target from widget
        self.target = None  # Set target to None

        if self.background in self.canvas.children:  # Check if background is in canvas
            self.canvas.remove(self.background)  # Remove background from canvas

        logger.debug('Level cleared')  # Log level cleared

    def show_level_popup(self):  # Define show_level_popup method
        popup = Popup(title=f'Level {self.level}', content=Label(text=f'Welcome to Level {self.level}'),
                      size_hint=(None, None), size=(400, 200))  # Create popup
        popup.open()  # Open popup
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)  # Schedule popup dismissal

    def show_victory_popup(self):  # Define show_victory_popup method
        score = self.calculate_score()  # Calculate score
        logger.debug(f'Victory! Score: {score}')  # Log victory
        popup = HallOfFamePopup(score=score)  # Create HallOfFamePopup
        popup.bind(on_dismiss=self.return_to_menu)  # Bind dismissal to return_to_menu
        popup.open()  # Open popup
        self.canvas.clear()  # Clear canvas
        with self.canvas:  # Add black rectangle to canvas
            Color(0, 0, 0, 1)  # Set color
            Rectangle(size=Window.size)  # Create rectangle

    def reset_game(self):  # Define reset_game method
        self.level = 1  # Reset level
        self.score = 0  # Reset score
        self.remaining_shots = 30  # Reset remaining shots
        self.clear_level()  # Clear level
        self.start_next_level()  # Start next level

    def show_game_over_popup(self):  # Define show_game_over_popup method
        popup = Popup(
            title='Game Over',
            content=Label(text=f'You have used all your shots. Your final score is {self.score}. Returning to main menu...'),
            size_hint=(None, None),
            size=(700, 300)
        )  # Create popup
        popup.open()  # Open popup
        Clock.schedule_once(self.return_to_menu, 3)  # Schedule return to menu

    def return_to_menu(self, dt=None):  # Define return_to_menu method
        if self.manager:  # Check if manager exists
            self.manager.transition = FadeTransition()  # Set transition
            self.manager.current = 'main_menu'  # Set current screen to main menu

    def update_obstacles(self, dt):  # Define update_obstacles method
        for obstacle in self.obstacles:  # Iterate over obstacles
            oscillation_x = obstacle.oscillation_amplitude * math.sin(Clock.get_time() * obstacle.oscillation_speed)  # Calculate oscillation x
            oscillation_y = obstacle.oscillation_amplitude * math.cos(Clock.get_time() * obstacle.oscillation_speed)  # Calculate oscillation y
            obstacle.rectangle.pos = (obstacle.initial_pos[0] + oscillation_x, obstacle.initial_pos[1] + oscillation_y)  # Update position

    def calculate_score(self):  # Define calculate_score method
        base_score = self.level * 100  # Calculate base score
        bonus = self.remaining_shots * 10  # Calculate bonus
        score = self.score  # Get score
        return base_score + bonus  # Return total score

    def show_pause_menu(self):  # Define show_pause_menu method
        pause_menu = PauseMenuPopup(game_widget=self)  # Create pause menu popup
        pause_menu.open()  # Open pause menu

# Define the main app class
class MyApp(App):  # Define MyApp class inheriting from App
    def build(self):  # Define build method
        Window.bind(on_key_down=self.on_keyboard)  # Bind keyboard event

        screen_manager = ScreenManager()  # Create screen manager
        splash_screen = SplashScreen(name='splash')  # Create splash screen
        storyline_screen = StorylineScreen(name="storyline")  # Create storyline screen
        main_menu_screen = MainMenu(name="main_menu")  # Create main menu screen
        game_screen = GameScreen(name="game")  # Create game screen
        hall_of_fame_screen = HallOfFame(name="hall_of_fame")  # Create hall of fame screen
        screen_manager.add_widget(splash_screen)  # Add splash screen to screen manager
        screen_manager.add_widget(storyline_screen)  # Add storyline screen to screen manager
        screen_manager.add_widget(main_menu_screen)  # Add main menu screen to screen manager
        screen_manager.add_widget(game_screen)  # Add game screen to screen manager
        screen_manager.add_widget(hall_of_fame_screen)  # Add hall of fame screen to screen manager
        return screen_manager  # Return screen manager

    def on_keyboard(self, window, key, *args):  # Define on_keyboard method
        if key == 27:  # Check if key is escape
            current_screen = self.root.current_screen  # Get current screen
            if isinstance(current_screen, GameScreen):  # Check if current screen is GameScreen
                current_screen.game_widget.show_pause_menu()  # Show pause menu
            elif isinstance(current_screen, MainMenu):  # Check if current screen is MainMenu
                self.show_exit_confirmation()  # Show exit confirmation
            elif isinstance(current_screen, HallOfFame):  # Check if current screen is HallOfFame
                self.show_return_to_menu_confirmation()  # Show return to menu confirmation

            return True  # Return True
        return False  # Return False

    def show_return_to_menu_confirmation(self):  # Define show_return_to_menu_confirmation method
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)  # Create content layout
        return_button = Button(text='Yes', size_hint=(1, 0.5))  # Create return button
        cancel_button = Button(text='No', size_hint=(1, 0.5))  # Create cancel button

        popup = Popup(title='Return to Menu?',
                    content=content,
                    size_hint=(None, None), size=(400, 200))  # Create popup

        return_button.bind(on_release=lambda x: self.return_to_menu(popup))  # Bind return button to return_to_menu
        cancel_button.bind(on_release=popup.dismiss)  # Bind cancel button to dismiss

        content.add_widget(return_button)  # Add return button to content
        content.add_widget(cancel_button)  # Add cancel button to content

        popup.open()  # Open popup

    def show_exit_confirmation(self):  # Define show_exit_confirmation method
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)  # Create content layout
        exit_button = Button(text='Exit', size_hint=(1, 0.5))  # Create exit button
        cancel_button = Button(text='Return to Menu', size_hint=(1, 0.5))  # Create cancel button

        popup = Popup(title='Close the Game?',
                      content=content,
                      size_hint=(None, None), size=(400, 200))  # Create popup

        exit_button.bind(on_release=lambda x: self.stop())  # Bind exit button to stop
        cancel_button.bind(on_release=popup.dismiss)  # Bind cancel button to dismiss

        content.add_widget(exit_button)  # Add exit button to content
        content.add_widget(cancel_button)  # Add cancel button to content

        popup.open()  # Open popup

    def return_to_menu(self, popup):  # Define return_to_menu method
        popup.dismiss()  # Dismiss popup
        self.root.transition = FadeTransition()  # Set transition
        self.root.current = 'main_menu'  # Set current screen to main menu

# Run the app
if __name__ == "__main__":  # Check if script is run directly
    MyApp().run()  # Run app

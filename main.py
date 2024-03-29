from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from quiz_screen import QuizScreen
from quiz_screen import ResultScreen
class CategorySelectionScreen(GridLayout):
    def __init__(self, **kwargs):
        super(CategorySelectionScreen, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10
        self.padding = [50, 50, 50, 50]
        self.size_hint = (0.8, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # ปุ่มสำหรับเลือกหมวดหมู่
        categories = ['Math', 'History', 'Physics', 'Geography', 'Literature', 'Science']
        for category in categories:
            btn = Button(text=category, size_hint_y=None, height=60, on_press=self.select_category)
            self.add_widget(btn)

    def select_category(self, instance):
        category = instance.text
        app = App.get_running_app()
        app.load_questions(category)
        app.screen_manager.current = 'quiz'

class CustomScreen(Screen):
    bg_color = ListProperty([0, 0, 0, 0]) 
class SettingsPopup(Popup):
    def __init__(self, **kwargs):
        super(SettingsPopup, self).__init__(**kwargs)
        self.title = 'Settings'
        self.size_hint = (None, None)
        self.size = (400, 400)

        layout = GridLayout(cols=2)

        # ตั้งค่าสี
        colors = [("White", [1, 1, 1, 1]), ("Red", [1, 0, 0, 1]), ("Green", [0, 1, 0, 1]), ("Blue", [0, 0, 1, 1]), ("Yellow", [1, 1, 0, 1])]
        for color_name, color_value in colors:
            btn = Button(text=color_name, on_press=lambda instance, c=color_value: self.change_bg_color(c))
            layout.add_widget(btn)

        # ตั้งค่าสไลเดอร์สำหรับปรับระดับเสียง
        volume_slider = Slider(min=0, max=1, value=0.5)
        volume_slider.bind(value=self.on_volume_change)
        layout.add_widget(volume_slider)  # สไลเดอร์ถูกเพิ่มลงใน layout
        mute_button = Button(text='Mute/Unmute', on_press=self.toggle_mute)
        layout.add_widget(mute_button)
        self.add_widget(layout)

    def toggle_mute(self, instance):
        # ส่งคำสั่งปิด/เปิดเสียงไปยังฟังก์ชัน mute_sound ของแอป
        App.get_running_app().mute_sound()    
    def on_volume_change(self, instance, value):
        App.get_running_app().change_volume(value)
    def change_bg_color(self, color):
        print("Changing color to:", color)  
        App.get_running_app().change_bg_color(color)
        self.dismiss()
class MainMenuScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        # Add background image
        self.add_widget(Image(source='image/QUizbacgroud.jpeg', keep_data=True))

        # Centered BoxLayout for buttons
        button_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button_layout.add_widget(Button(text='Start Quiz', on_press=self.start_quiz))
        button_layout.add_widget(Button(text='Settings', on_press=self.settings))
        button_layout.add_widget(Button(text='Quit', on_press=self.quit))
        self.add_widget(button_layout)

    def start_quiz(self, instance):
        App.get_running_app().screen_manager.current = 'category_selection'

    def settings(self, instance):
        settings_popup = SettingsPopup()
        settings_popup.open()

    def quit(self, instance):
        App.get_running_app().stop()

class QuizApp(App):
    def __init__(self, **kwargs):
        super(QuizApp, self).__init__(**kwargs)
        self.is_muted = False
        self.previous_volume = 0.5  # ตั้งค่าระดับเสียงเริ่มต้น
        self.sound = None
    def load_questions(self, category):
        # โหลดคำถามตามหมวดหมู่
        if category == 'Math':
            self.quiz_screen_instance.questions = self.math_questions
        elif category == 'History':
            self.quiz_screen_instance.questions = self.history_questions
        elif category == 'Physics':
            self.quiz_screen_instance.questions = self.physics_questions
        elif category == 'Geography':
            self.quiz_screen_instance.questions = self.geography_questions
        elif category == 'Literature':
            self.quiz_screen_instance.questions = self.literature_questions
        elif category == 'Science':
            self.quiz_screen_instance.questions = self.science_questions

        # รีเซ็ตและโหลดคำถาม
        self.quiz_screen_instance.current_question_index = 0
        self.quiz_screen_instance.load_question()
        
    def build(self):
        # คำถามสำหรับแต่ละหมวดหมู่
        self.math_questions = [
            {'question': '2+2?', 'answers': ['3', '4', '5'], 'correct': '4'},
            {'question': 'What is the square root of 16?', 'answers': ['3', '4', '5'], 'correct': '4'},
            {'question': 'What is 15 divided by 3?', 'answers': ['5', '6', '7'], 'correct': '5'},
            {'question': 'What is the result of 7 times 6?', 'answers': ['42', '48', '52'], 'correct': '42'},
            {'question': 'What is 50% of 100?', 'answers': ['50', '60', '40'], 'correct': '50'},
            {'question': 'What is the next prime number after 7?', 'answers': ['9', '11', '13'], 'correct': '11'},
            {'question': 'What is the value of x in the equation 3x + 2 = 11?', 'answers': ['2', '3', '4'], 'correct': '3'},
            {'question': 'What is the perimeter of a rectangle with a length of 10 and width of 5?', 'answers': ['30', '15', '25'], 'correct': '30'},
            {'question': 'What is the area of a circle with a radius of 7?', 'answers': ['154', '147', '138'], 'correct': '154'},
            {'question': 'How many sides does a hexagon have?', 'answers': ['5', '6', '7'], 'correct': '6'},
            {'question': 'What is the product of 12 and 8?', 'answers': ['96', '88', '100'], 'correct': '96'}

        ]

        self.history_questions = [
            {'question': 'Who was the first president of the USA?', 'answers': ['Washington', 'Lincoln', 'Jefferson'], 'correct': 'Washington'},
            {'question': 'In which year did World War II end?', 'answers': ['1945', '1946', '1944'], 'correct': '1945'},
            {'question': 'What was the name of the ship that sank after hitting an iceberg in 1912?', 'answers': ['Titanic', 'Britannic', 'Olympic'], 'correct': 'Titanic'},
            {'question': 'Who was known as the "Father of Modern Science"?', 'answers': ['Galileo Galilei', 'Isaac Newton', 'Albert Einstein'], 'correct': 'Galileo Galilei'},
            {'question': 'What ancient civilization built the Pyramids of Giza?', 'answers': ['Egyptians', 'Mayans', 'Aztecs'], 'correct': 'Egyptians'},
            {'question': 'Who wrote the Declaration of Independence?', 'answers': ['Thomas Jefferson', 'George Washington', 'John Adams'], 'correct': 'Thomas Jefferson'},
            {'question': 'Which empire was ruled by Alexander the Great?', 'answers': ['Roman', 'Persian', 'Macedonian'], 'correct': 'Macedonian'},
            {'question': 'In which year did the Berlin Wall fall?', 'answers': ['1989', '1991', '1987'], 'correct': '1989'},
            {'question': 'What was the main cause of the French Revolution?', 'answers': ['Economic Crisis', 'Religious Conflict', 'Foreign Invasion'], 'correct': 'Economic Crisis'},
            {'question': 'Who was the Egyptian queen famous for her beauty and affair with Mark Antony?', 'answers': ['Nefertiti', 'Cleopatra', 'Hatshepsut'], 'correct': 'Cleopatra'},
            {'question': 'What was the original name of New York City?', 'answers': ['New Amsterdam', 'New England', 'New Jersey'], 'correct': 'New Amsterdam'}

        ]

        self.physics_questions = [
            {'question': 'What is the speed of light?', 'answers': ['299792458 m/s', '150000000 m/s', 'None'], 'correct': '299792458 m/s'},
            {'question': 'What is the force that keeps us on the ground called?', 'answers': ['Gravity', 'Magnetism', 'Friction'], 'correct': 'Gravity'},
            {'question': 'Who discovered the law of universal gravitation?', 'answers': ['Isaac Newton', 'Albert Einstein', 'Galileo Galilei'], 'correct': 'Isaac Newton'},
            {'question': 'What is the smallest particle of an element called?', 'answers': ['Atom', 'Electron', 'Molecule'], 'correct': 'Atom'},
            {'question': 'What is the name of the fourth state of matter?', 'answers': ['Plasma', 'Gas', 'Liquid'], 'correct': 'Plasma'},
            {'question': 'What device is used to measure electric current?', 'answers': ['Ammeter', 'Voltmeter', 'Barometer'], 'correct': 'Ammeter'},
            {'question': 'What principle explains why ships float?', 'answers': ['Archimedes\' Principle', 'Newton\'s Third Law', 'Bernoulli\'s Principle'], 'correct': 'Archimedes\' Principle'},
            {'question': 'What particle is known as the "God Particle"?', 'answers': ['Electron', 'Neutron', 'Higgs Boson'], 'correct': 'Higgs Boson'},
            {'question': 'Who is the scientist famous for his theory of relativity?', 'answers': ['Isaac Newton', 'Albert Einstein', 'Niels Bohr'], 'correct': 'Albert Einstein'},
            {'question': 'What is the unit of frequency?', 'answers': ['Hertz', 'Watt', 'Newton'], 'correct': 'Hertz'},
            {'question': 'What phenomenon causes the Northern Lights?', 'answers': ['Solar Wind', 'Lunar Reflection', 'Earthquake'], 'correct': 'Solar Wind'}

        ]
        self.geography_questions = [
            {'question': 'What is the largest continent?', 'answers': ['Africa', 'Asia', 'Europe'], 'correct': 'Asia'},
            {'question': 'What river is the longest in the world?', 'answers': ['Nile', 'Amazon', 'Yangtze'], 'correct': 'Nile'},
            {'question': 'In which country is the Sahara Desert primarily located?', 'answers': ['Egypt', 'Morocco', 'Chad'], 'correct': 'Egypt'},
            {'question': 'Which is the smallest country in the world?', 'answers': ['Vatican City', 'Monaco', 'Nauru'], 'correct': 'Vatican City'},
            {'question': 'Which country has the most natural lakes?', 'answers': ['Canada', 'USA', 'Russia'], 'correct': 'Canada'},
            {'question': 'What is the capital city of Japan?', 'answers': ['Kyoto', 'Osaka', 'Tokyo'], 'correct': 'Tokyo'},
            {'question': 'Which river flows through Paris?', 'answers': ['Seine', 'Thames', 'Danube'], 'correct': 'Seine'},
            {'question': 'What is the highest mountain in the world?', 'answers': ['K2', 'Everest', 'Kilimanjaro'], 'correct': 'Everest'},
            {'question': 'Which country is known as the Land of the Rising Sun?', 'answers': ['China', 'Japan', 'Korea'], 'correct': 'Japan'},
            {'question': 'What is the longest river in Africa?', 'answers': ['Nile', 'Congo', 'Niger'], 'correct': 'Nile'}

        ]

        self.literature_questions = [
            {'question': 'Who wrote "Romeo and Juliet"?', 'answers': ['William Shakespeare', 'Charles Dickens', 'Leo Tolstoy'], 'correct': 'William Shakespeare'},
            {'question': 'What is the oldest known literary work?', 'answers': ['The Epic of Gilgamesh', 'The Iliad', 'Beowulf'], 'correct': 'The Epic of Gilgamesh'},
            {'question': 'In "Harry Potter", what is the name of Harry\'s owl?', 'answers': ['Hedwig', 'Errol', 'Crookshanks'], 'correct': 'Hedwig'},
            {'question': 'Who wrote "The Great Gatsby"?', 'answers': ['F. Scott Fitzgerald', 'Ernest Hemingway', 'John Steinbeck'], 'correct': 'F. Scott Fitzgerald'},
            {'question': 'What is the main theme of "To Kill a Mockingbird"?', 'answers': ['Racism', 'War', 'Love'], 'correct': 'Racism'},
            {'question': 'Who wrote "Pride and Prejudice"?', 'answers': ['Jane Austen', 'Emily Bronte', 'Virginia Woolf'], 'correct': 'Jane Austen'},
            {'question': 'Which novel features the character Atticus Finch?', 'answers': ['To Kill a Mockingbird', 'The Great Gatsby', '1984'], 'correct': 'To Kill a Mockingbird'},
            {'question': 'What is the longest epic poem in world literature?', 'answers': ['Mahabharata', 'Odyssey', 'Iliad'], 'correct': 'Mahabharata'},
            {'question': 'Who is the author of "The Hobbit"?', 'answers': ['J.R.R. Tolkien', 'C.S. Lewis', 'J.K. Rowling'], 'correct': 'J.R.R. Tolkien'},
            {'question': 'What is the main setting of the "Harry Potter" series?', 'answers': ['Hogwarts', 'Narnia', 'Middle Earth'], 'correct': 'Hogwarts'}

        ]

        self.science_questions = [
            {'question': 'What element does "O" represent on the periodic table?', 'answers': ['Oxygen', 'Osmium', 'Gold'], 'correct': 'Oxygen'},
            {'question': 'Who is known as the father of modern physics?', 'answers': ['Albert Einstein', 'Isaac Newton', 'Niels Bohr'], 'correct': 'Albert Einstein'},
            {'question': 'What is the powerhouse of the cell?', 'answers': ['Mitochondria', 'Nucleus', 'Ribosome'], 'correct': 'Mitochondria'},
            {'question': 'What is the study of fungi called?', 'answers': ['Mycology', 'Botany', 'Zoology'], 'correct': 'Mycology'},
            {'question': 'Which planet is known as the Red Planet?', 'answers': ['Mars', 'Jupiter', 'Saturn'], 'correct': 'Mars'}
        ]


        # โหลดเสียง
        self.sound = SoundLoader.load('music/intomusicquiz.mp3')
        if self.sound:
            self.sound.volume = self.previous_volume
            self.sound.play()

        # สร้าง ScreenManager และหน้าจอต่างๆ
        self.screen_manager = ScreenManager()
        self.main_menu_screen = CustomScreen(name='main_menu')
        self.main_menu_screen.add_widget(MainMenuScreen())

        # สร้างและเก็บอินสแตนซ์ของ QuizScreen
        self.quiz_screen_instance = QuizScreen()
        self.quiz_screen = CustomScreen(name='quiz')
        self.quiz_screen.add_widget(self.quiz_screen_instance)

        self.category_screen = CustomScreen(name='category_selection')
        self.category_screen.add_widget(CategorySelectionScreen())

        self.result_screen = CustomScreen(name='result')
        self.result_screen.add_widget(ResultScreen())

        # เพิ่มหน้าจอลงใน ScreenManager
        self.screen_manager.add_widget(self.main_menu_screen)
        self.screen_manager.add_widget(self.category_screen)
        self.screen_manager.add_widget(self.quiz_screen)
        self.screen_manager.add_widget(self.result_screen)

        return self.screen_manager

    def show_result(self, score, time):
        result_screen_widget = self.result_screen.children[0]
        result_screen_widget.update_results(score, time)
        self.screen_manager.current = 'result'
    def change_bg_color(self, color):
        print("Applying color:", color)
        for screen in self.screen_manager.screens:
            screen.bg_color = color     

    def change_volume(self, value):
        # ตั้งค่าระดับเสียงของเพลง
        if self.sound:
            self.sound.volume = value   
    def mute_sound(self):
        if self.sound:
            if not self.is_muted:
                self.previous_volume = self.sound.volume
                self.sound.volume = 0
                self.is_muted = True
            else:
                self.sound.volume = self.previous_volume
                self.is_muted = False            

if __name__ == '__main__':
    QuizApp().run()

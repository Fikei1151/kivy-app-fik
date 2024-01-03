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

class CategorySelectionScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(CategorySelectionScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Button(text='Math', on_press=self.select_category))
        self.add_widget(Button(text='History', on_press=self.select_category))
        self.add_widget(Button(text='Physics', on_press=self.select_category))

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

class QuizScreen(BoxLayout):
    question_label = ObjectProperty()
    result_label = ObjectProperty()
    answer_buttons = ListProperty()
    current_question_index = NumericProperty(0)
    score = NumericProperty(0)
    time_elapsed = NumericProperty(0)
    questions = ListProperty([
        {"question": "What is 2 + 2?", "answers": ["3", "4", "5"], "correct": "4"},
        {"question": "What is the capital of France?", "answers": ["Paris", "London", "Berlin"], "correct": "Paris"},
        {"question": "Who wrote 1984?", "answers": ["Orwell", "Shakespeare", "Tolkien"], "correct": "Orwell"},
        {"question": "Who is create Quiz app?", "answers": ["Fikree", "Fikree handsome", "Fikree handsome and so cool"], "correct": "Fikree handsome and so cool"}
    ])
    bg_color = ListProperty([0, 0, 0, 0])  # เพิ่ม property นี้
    def on_questions(self, instance, value):
        # รีเซ็ตคำถามเมื่อมีการเปลี่ยนแปลงรายการคำถาม
        self.current_question_index = 0
        self.load_question()
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.timer_event = Clock.schedule_interval(self.update_time, 1)
        self.load_question()  # Load the first question immediately

    def update_time(self, dt):
        self.time_elapsed += 1

    def on_current_question_index(self, instance, value):
        if value < len(self.questions):
            self.load_question()
        else:
            self.end_quiz()

    def load_question(self):
        question = self.questions[self.current_question_index]
        self.question_label.text = question['question']
        self.answer_buttons = question['answers']

    def check_answer(self, answer):
        # ตรวจสอบว่ายังอยู่ในขอบเขตของลิสต์คำถามหรือไม่
        if self.current_question_index < len(self.questions):
            correct_answer = self.questions[self.current_question_index]['correct']
            if answer == correct_answer:
                self.score += 1
                self.result_label.text = "Correct!"
            else:
                self.result_label.text = "Incorrect! Try again."

            # ขยับไปยังคำถามถัดไปหรือจบควิซ
            self.current_question_index += 1
            if self.current_question_index >= len(self.questions):
                self.end_quiz()
        else:
            self.end_quiz()
    def end_quiz(self):
        Clock.unschedule(self.timer_event)
        app = App.get_running_app()
        app.show_result(self.score, self.time_elapsed)


class ResultScreen(BoxLayout):
    score_label = ObjectProperty()
    time_label = ObjectProperty()
    bg_color = ListProperty([0, 0, 0, 0])
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
    def update_results(self, score, time):
        self.score_label.text = f"Score: {score}"
        self.time_label.text = f"Time: {time} seconds"

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

        # รีเซ็ตและโหลดคำถาม
        self.quiz_screen_instance.current_question_index = 0
        self.quiz_screen_instance.load_question()

    def build(self):
        # คำถามสำหรับแต่ละหมวดหมู่
        self.math_questions = [
            {'question': '2+2?', 'answers': ['3', '4', '5'], 'correct': '4'},
            # คำถามอื่นๆ
        ]
        self.history_questions = [
            {'question': 'Who was the first president of the USA?', 'answers': ['Washington', 'Lincoln', 'Jefferson'], 'correct': 'Washington'},
            # คำถามอื่นๆ
        ]
        self.physics_questions = [
            {'question': 'What is the speed of light?', 'answers': ['299792458 m/s', '150000000 m/s', 'None'], 'correct': '299792458 m/s'},
            # คำถามอื่นๆ
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

    # def play_sound(self, sound_file):
    #     self.sound = SoundLoader.load(sound_file)
    #     if self.sound:
    #         self.sound.volume = 0.5
    #         self.sound.loop = True
    #         self.sound.play()

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

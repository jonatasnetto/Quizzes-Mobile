from itertools import count
from random import choices
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from login_firebase import Accont
import json
import os
from kivy.properties import ObjectProperty
#Please before run, take a look the requirements file to check if all methods needed are installed.

#Loadind the questions and answers data from JSON files(db_questions.json,db_answers.json)
cwd=os.getcwd()
cwd2=os.getcwd()
js = '%s/%s' % (cwd,'db_questions.json')
js2 = '%s/%s' % (cwd2,'db_answers.json')
questions = {}
answers = {}
try:
    with open(js) as data_file:
        questions = json.load(data_file)
    with open(js2) as data_file2:
        answers = json.load(data_file2)
except IOError as e:
    print (e)
    print ('IOError: Unable to open database *.json. Terminating execution.')

#ScreenManager function to manages the Screems
class Manager(ScreenManager):
    pass

#Login class to manages the Screems
class LoginScreen(MDScreen):
    def on_pre_enter(self, *args):
        Main.count = 0
        Main.score = 0
        Main.choices.clear()
        try:
            self.ids.text_email.text = ""
            self.ids.text_password.text = ""
        except:
            pass

    def try_sign_in(self, *args):
        Clock.schedule_once(self.start_sign_in, .1)

    def start_sign_in(self, *args):
        email = self.ids.text_email.text
        password = self.ids.text_password.text

        #Check user access on firebase account
        if accont.sign_in(email, password):
            self.ids.error_login.text = ""
            MDApp.get_running_app().root.current = "home_page"
        else:
            if email and password:
                self.ids.text_password.text = ""
                self.ids.text_email.focus = True
            elif email and not password:
                self.ids.text_password.focus = True
            elif password and not email:
                self.ids.text_password.text = ""
                self.ids.text_email.focus = True
            else:
                self.ids.text_email.focus = True
            self.ids.error_login.text = "Invalid data! Try again!"

#Homepage class with the functions
class HomePage(MDScreen):

    def callback(self):
        MDApp.get_running_app().root.current = "login"

    def get_start(self):
        Main.count = 0
        Main.score = 0
        Main.choices.clear()
        MDApp.get_running_app().root.current = "quizzes"

#ResetPassword class with the functions
class ResetPassword(MDScreen):
    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

    def on_pre_enter(self, *args):
        self.ids.text_redefined.theme_text_color = "Primary"
        self.ids.text_redefined.text = "Send E-mail to reset password."
        self.ids.email_confirm.text = ""

    def send_email_confirm(self):
        email = self.ids.email_confirm.text

        if accont.reset_password(email):
            self.ids.text_redefined.text = "Email successfully sent"
            self.ids.text_redefined.theme_text_color = "Custom"
            self.ids.text_redefined.text_color = (0, 1, 0, 1)
        else:
            self.ids.text_redefined.text = "Failed to send email"
            self.ids.text_redefined.theme_text_color = "Custom"
            self.ids.text_redefined.text_color = (1, 0, 0, 1)

        Clock.schedule_once(self.callback, 2)

#Register class with the functions
class Register(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.email_register.text = ""
        self.ids.password_register.text = ""
        self.ids.password_register_confirm.text = ""
        self.ids.label_register.text = "Enter your data"
        self.ids.label_register.theme_text_color = "Primary"

    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

    def validate_info(self):
        email = self.ids.email_register.text
        password = self.ids.password_register.text
        password_confirm = self.ids.password_register_confirm.text

        if password == password_confirm and "@" in email and ".com" in email and len(password) >= 6:
            if accont.sing_up(email, password):
                self.ids.label_register.text = "Registration created successfully"
                self.ids.label_register.theme_text_color = "Custom"
                self.ids.label_register.text_color = (0, 1, 0, 1)
                Clock.schedule_once(self.callback, 2)
            else:
                self.ids.label_register.text = "failed to create record"
                self.ids.label_register.theme_text_color = "Custom"
                self.ids.label_register.text_color = (1, 0, 0, 1)
        else:
            if not email or "@" not in email or ".com" not in email:
                self.ids.email_register.focus = True
            elif len(password) < 6:
                self.ids.password_register_confirm.text = ""
                self.ids.password_register.text = ""
                self.ids.password_register.focus = True
            elif  len(password_confirm) < 6:
                self.ids.password_register_confirm.text = ""
                self.ids.password_register_confirm.focus = True
            elif password != password_confirm:
                if password:
                    self.ids.password_register.focus = True
                    self.ids.password_register_confirm.text = ""
                    self.ids.password_register.text = ""
                else:
                    self.ids.password_register_confirm.focus = True
                    self.ids.password_register_confirm.text = ""

#Quizzes class with the functions
class Quizzes(MDScreen):

    choice_a: ObjectProperty(None)
    choice_b: ObjectProperty(None)
    choice_c: ObjectProperty(None)
    choice_d: ObjectProperty(None)

    def on_pre_enter(self):
        self.ids.show_questions.text = f'{questions[str(0)]}'
   
    def check_choice(self, *args):
        self.ids.error_answer.text = ''

        if self.choice_a.active:
            Main.choices.append('A')
            if Main.choices[Main.count] == answers[str(Main.count)]:
                Main.score+=1
            Main.count += 1
            if Main.count<len(questions):
                self.ids.show_questions.text = f'{questions[str(Main.count)]}'
            self.choice_a.active = False
            if Main.count > len(questions)-1:
                self.choice_a.active = False
                MDApp.get_running_app().root.current = "result"
        elif self.choice_b.active:
            Main.choices.append('B')
            if Main.choices[Main.count] == answers[str(Main.count)]:
                Main.score+=1
            Main.count += 1
            if Main.count<len(questions):
                self.ids.show_questions.text = f'{questions[str(Main.count)]}'
            self.choice_b.active = False
            if Main.count > len(questions)-1:
                self.choice_b.active = False
                MDApp.get_running_app().root.current = "result"
        elif self.choice_c.active:
            Main.choices.append('C')
            if Main.choices[Main.count] == answers[str(Main.count)]:
                Main.score+=1
            Main.count += 1
            if Main.count<len(questions):
                self.ids.show_questions.text = f'{questions[str(Main.count)]}'
            self.choice_c.active = False
            if Main.count > len(questions)-1:
                self.choice_c.active = False
                MDApp.get_running_app().root.current = "result"
        elif self.choice_d.active:
            Main.choices.append('D')
            if Main.choices[Main.count] == answers[str(Main.count)]:
                Main.score+=1
            Main.count += 1
            if Main.count<len(questions):
                self.ids.show_questions.text = f'{questions[str(Main.count)]}'
            self.choice_d.active = False
            if Main.count > len(questions)-1:
                self.choice_d.active = False
                MDApp.get_running_app().root.current = "result"
        else:
            self.ids.error_answer.text = 'Not answer marked!'

    def callback(self):
        MDApp.get_running_app().root.current = "login"

#Result class with the functions
class Result(MDScreen):

    def on_pre_enter(self):
        self.ids.final_result.text = str(Main.score*10)+'%'
        if Main.score>=7:
            self.ids.result_icon.icon = "emoticon-outline"
            self.ids.congrats_sorry.text = "Congratulations!"
            self.ids.final_result.theme_text_color = "Secondary"
        else:
            self.ids.result_icon.icon = "emoticon-sad-outline"
            self.ids.congrats_sorry.text = "Better luck next time!"

    def try_again(self):
        MDApp.get_running_app().root.current = "quizzes"

    def callback(self, *args):
        MDApp.get_running_app().root.current = "login"

    def quit(self, *args):
        exit()

#Main class with the builder and global variables
class Main(MDApp):
    choices=[]
    count=0
    score=0

    #Standard screen size
    Window.size = (400, 600)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Manager()#main.kv

if __name__ == "__main__":
    accont = Accont()
    Main().run()
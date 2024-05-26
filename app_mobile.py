from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.font_definitions import theme_font_styles
from kivy.utils import get_color_from_hex
from kivymd.uix.menu import MDDropdownMenu
from kivy.base import runTouchApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.clock import Clock
from AI_center import *
from kivy.uix.checkbox import CheckBox
import firebase_admin
from firebase_admin import credentials, db

Window.size = (310, 580)
if not firebase_admin._apps:
    # Инициализация приложения Firebase
    cred = credentials.Certificate("FireBaseKey/englishapp-92af3-firebase-adminsdk-srxgg-74b6ccf882.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://englishapp-92af3-default-rtdb.firebaseio.com/'
    })


class Slope(MDApp):
    current_question_index = 1
    answer_number = None
    # Получаем цвет из шестнадцатеричного кода
    blue_color = get_color_from_hex("#0000CD")
    black_color = get_color_from_hex("#000000")

    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("App_screens/main.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/login.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/signup.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/education_plan.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/weakly_plan.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/feedback.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/start_use.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/questionnaire_test.kv"))
        screen_manager.add_widget(Builder.load_file("App_screens/profile.kv"))

        # Установка синего цвета для MDLabel с именем "label_or"
        login_screen = screen_manager.get_screen("login")
        label_or = login_screen.ids.label_or
        label_or.color = get_color_from_hex("#0000FF")  # синий цвет в формате шестнадцатеричного кода

        return screen_manager

    def get_plan_e(self):
        give_common_plan()
        file_path = "StructurePrompts/education_plan.json"
        # Читаем содержимое файла JSON
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Извлекаем данные из card1
        card1_data = data.get("Card 1")
        if card1_data:
            # Получаем number_day и advice из card1
            number_day = card1_data.get("number_day")
            advice = card1_data.get("advice")
            # Отображаем полученные данные
            print("Number Day (Card 1):", number_day)
            print("Advice (Card 1):", advice)
            self.root.get_screen("weakly_plan").ids.DayLabel.text = number_day
            self.root.get_screen("weakly_plan").ids.plan_label.text = advice
        else:
            print("Card 1 data not found in the file")



    def on_right_arrow_press_plan(self):
        file_path = "StructurePrompts/education_plan.json"
        # Получаем текущий номер карты
        current_card_number = getattr(self, "current_card_number", 1)
        # Читаем содержимое файла JSON
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Формируем ключ для текущей карты
        current_card_key = f"Card {current_card_number}"

        # Проверяем, есть ли следующая карта в файле JSON
        if f"Card {current_card_number + 1}" in data:
            # Если следующая карта есть, увеличиваем номер текущей карты
            self.current_card_number = current_card_number + 1
            # Извлекаем данные из следующей карты
            next_card_data = data[f"Card {self.current_card_number}"]
            # Получаем number_day и advice из следующей карты
            next_number_day = next_card_data["number_day"]
            next_advice = next_card_data["advice"]
            # Отображаем полученные данные
            print("Number Day:", next_number_day)
            print("Advice:", next_advice)
            self.root.get_screen("weakly_plan").ids.DayLabel.text = next_number_day
            self.root.get_screen("weakly_plan").ids.plan_label.text = next_advice
            self.root.get_screen("weakly_plan").ids.cardleft.opacity = 1
            self.root.get_screen("weakly_plan").ids.cardleft.disabled = False
        else:
            print("No next card available")
            self.root.get_screen("weakly_plan").ids.cardright.opacity = 0
            self.root.get_screen("weakly_plan").ids.cardright.disabled = True

    def on_left_arrow_press_plan(self):
        file_path = "StructurePrompts/education_plan.json"
        # Получаем текущий номер карты
        current_card_number = getattr(self, "current_card_number", 1)
        # Читаем содержимое файла JSON
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Формируем ключ для текущей карты
        current_card_key = f"Card {current_card_number}"

        # Проверяем, есть ли следующая карта в файле JSON
        if f"Card {current_card_number - 1}" in data:
            # Если следующая карта есть, увеличиваем номер текущей карты
            self.current_card_number = current_card_number - 1
            # Извлекаем данные из следующей карты
            next_card_data = data[f"Card {self.current_card_number}"]
            # Получаем number_day и advice из следующей карты
            next_number_day = next_card_data["number_day"]
            next_advice = next_card_data["advice"]
            # Отображаем полученные данные
            print("Number Day:", next_number_day)
            print("Advice:", next_advice)
            self.root.get_screen("weakly_plan").ids.DayLabel.text = next_number_day
            self.root.get_screen("weakly_plan").ids.plan_label.text = next_advice
            self.root.get_screen("weakly_plan").ids.cardleft.opacity = 1
            self.root.get_screen("weakly_plan").ids.cardleft.disabled = False
            self.root.get_screen("weakly_plan").ids.cardright.opacity = 1
            self.root.get_screen("weakly_plan").ids.cardright.disabled = False
        else:
            print("No next card available")
            self.root.get_screen("weakly_plan").ids.cardleft.opacity = 0
            self.root.get_screen("weakly_plan").ids.cardleft.disabled = True
            # self.root.get_screen("weakly_plan").ids.cardright.opacity = 1
            # self.root.get_screen("weakly_plan").ids.cardrigth.disabled = False
    def get_new_question(self):
        folder_path = "Login_data"
        files = os.listdir(folder_path)
        for file_name in files:
            if file_name.endswith("login_data.json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    get_email = data['email']
                    print(get_email)
                    get_question(get_email)

    def on_button_press(self, button_text):
        print(f"Pressed button text: {button_text}")
        question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
        print(question)

    import json

    def on_checkbox_press_q(self, checkbox_id):
        print(f"Нажал {checkbox_id}")
        file_path = "StructurePrompts/qa.json"

        # Пытаемся прочитать текущее содержимое файла
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            # Если файл еще не существует, создаем пустую структуру
            data = {"skill": "", "days": 0, "hours": 0}

        if checkbox_id == 1:
            print("Listening")
            # Записываем навык в структуру
            data["skill"] = "Listening"
            self.root.get_screen("education_plan").ids.checkButton1.color = self.blue_color
            self.root.get_screen("education_plan").ids.checkButton2.color = self.black_color
            self.root.get_screen("education_plan").ids.checkButton3.color = self.black_color
        elif checkbox_id == 2:
            print("Writing")
            data["skill"] = "Writing"
            self.root.get_screen("education_plan").ids.checkButton1.color = self.black_color
            self.root.get_screen("education_plan").ids.checkButton2.color = self.blue_color
            self.root.get_screen("education_plan").ids.checkButton3.color = self.black_color
        elif checkbox_id == 3:
            print("Speaking")
            data["skill"] = "Speaking"
            self.root.get_screen("education_plan").ids.checkButton1.color = self.black_color
            self.root.get_screen("education_plan").ids.checkButton2.color = self.black_color
            self.root.get_screen("education_plan").ids.checkButton3.color = self.blue_color
        elif 4 <= checkbox_id <= 10:
            # Обновляем дни
            days = checkbox_id - 3
            print(f"{days} days")
            # Устанавливаем цвета для всех кнопок
            for i in range(1, 7):
                button_name = f"checkButtond{i}"
                if i == days:
                    # Если номер кнопки совпадает с номером часа, устанавливаем синий цвет
                    self.root.get_screen("education_plan").ids[button_name].color = self.blue_color
                else:
                    # Иначе устанавливаем черный цвет
                    self.root.get_screen("education_plan").ids[button_name].color = self.black_color
            data["days"] = f"{days} days"
        elif 11 <= checkbox_id <= 14:
            # Обновляем часы
            hours = checkbox_id - 10
            print(f"{hours} hours")

            # Устанавливаем цвета для всех кнопок
            for i in range(1, 5):
                button_name = f"checkButtonh{i}"
                if i == hours:
                    # Если номер кнопки совпадает с номером часа, устанавливаем синий цвет
                    self.root.get_screen("education_plan").ids[button_name].color = self.blue_color
                else:
                    # Иначе устанавливаем черный цвет
                    self.root.get_screen("education_plan").ids[button_name].color = self.black_color

            data["hours"] = f"{hours} hours"

        # Записываем обновленные данные в файл
        with open(file_path, 'w') as file:
            json.dump(data, file)



    def on_checkbox_press(self, checkbox_id):
        print(f"Нажал {checkbox_id}")
        if checkbox_id == 1:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.blue_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
            button_text1 = self.root.get_screen("questionnaire_test").ids.checkButton1.text
            print(f"Text from MDTextButton: {button_text1}")
            question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
            print(question)
            # Определяем путь к файлу и создаем его, если он не существует
            folder_path_2 = "answers_from_users"
            file_name_2 = "answers.json"
            file_path_2 = os.path.join(folder_path_2, file_name_2)
            if not os.path.exists(folder_path_2):
                os.makedirs(folder_path_2)
            # Если файл уже существует, загружаем данные из него
            if os.path.exists(file_path_2):
                with open(file_path_2, 'r', encoding='utf-8') as file_2:
                    questionnaire_data = json.load(file_2)
            else:
                questionnaire_data = {}
            # Находим номер карточки по номеру вопроса
            question_number = int(question.split('.')[0])
            card_key = f"card {question_number}"
            # Обновляем вопрос в существующей карточке, если она существует
            if card_key in questionnaire_data:
                questionnaire_data[card_key]["question"] = question
                questionnaire_data[card_key]["answer"] = button_text1
                # Сохраняем обновленные данные в файл JSON
                with open(file_path_2, 'w', encoding='utf-8') as file_2:
                    json.dump(questionnaire_data, file_2, ensure_ascii=False, indent=4)
        if checkbox_id == 2:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.blue_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
            button_text2 = self.root.get_screen("questionnaire_test").ids.checkButton2.text
            print(f"Text from MDTextButton: {button_text2}")
            question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
            print(question)
            # Определяем путь к файлу и создаем его, если он не существует
            folder_path_2 = "answers_from_users"
            file_name_2 = "answers.json"
            file_path_2 = os.path.join(folder_path_2, file_name_2)
            if not os.path.exists(folder_path_2):
                os.makedirs(folder_path_2)
            # Если файл уже существует, загружаем данные из него
            if os.path.exists(file_path_2):
                with open(file_path_2, 'r', encoding='utf-8') as file_2:
                    questionnaire_data = json.load(file_2)
            else:
                questionnaire_data = {}
            # Находим номер карточки по номеру вопроса
            question_number = int(question.split('.')[0])
            card_key = f"card {question_number}"
            if card_key in questionnaire_data:
                questionnaire_data[card_key]["question"] = question
                questionnaire_data[card_key]["answer"] = button_text2
                # Сохраняем обновленные данные в файл JSON
                with open(file_path_2, 'w', encoding='utf-8') as file_2:
                    json.dump(questionnaire_data, file_2, ensure_ascii=False, indent=4)
        if checkbox_id == 3:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.blue_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
            button_text3 = self.root.get_screen("questionnaire_test").ids.checkButton3.text
            print(f"Text from MDTextButton: {button_text3}")
            question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
            print(question)
            # Определяем путь к файлу и создаем его, если он не существует
            folder_path_2 = "answers_from_users"
            file_name_2 = "answers.json"
            file_path_2 = os.path.join(folder_path_2, file_name_2)
            if not os.path.exists(folder_path_2):
                os.makedirs(folder_path_2)
            # Если файл уже существует, загружаем данные из него
            if os.path.exists(file_path_2):
                with open(file_path_2, 'r', encoding='utf-8') as file_2:
                    questionnaire_data = json.load(file_2)
            else:
                questionnaire_data = {}
            # Находим номер карточки по номеру вопроса
            question_number = int(question.split('.')[0])
            card_key = f"card {question_number}"
            if card_key in questionnaire_data:
                questionnaire_data[card_key]["question"] = question
                questionnaire_data[card_key]["answer"] = button_text3
                # Сохраняем обновленные данные в файл JSON
                with open(file_path_2, 'w', encoding='utf-8') as file_2:
                    json.dump(questionnaire_data, file_2, ensure_ascii=False, indent=4)
        if checkbox_id == 4:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.blue_color
            button_text4 = self.root.get_screen("questionnaire_test").ids.checkButton4.text
            print(f"Text from MDTextButton: {button_text4}")
            question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
            print(question)
            # Определяем путь к файлу и создаем его, если он не существует
            folder_path_2 = "answers_from_users"
            file_name_2 = "answers.json"
            file_path_2 = os.path.join(folder_path_2, file_name_2)
            if not os.path.exists(folder_path_2):
                os.makedirs(folder_path_2)
            # Если файл уже существует, загружаем данные из него
            if os.path.exists(file_path_2):
                with open(file_path_2, 'r', encoding='utf-8') as file_2:
                    questionnaire_data = json.load(file_2)
            else:
                questionnaire_data = {}
            # Находим номер карточки по номеру вопроса
            question_number = int(question.split('.')[0])
            card_key = f"card {question_number}"
            if card_key in questionnaire_data:
                questionnaire_data[card_key]["question"] = question
                questionnaire_data[card_key]["answer"] = button_text4
                # Сохраняем обновленные данные в файл JSON
                with open(file_path_2, 'w', encoding='utf-8') as file_2:
                    json.dump(questionnaire_data, file_2, ensure_ascii=False, indent=4)

    # def on_checkbox_press(self, checkbox_instance, checkbox_state):
    #     if checkbox_state == 'down':
    #         # checkbox_id = checkbox_instance.ids.text
    #         checkbox_id = self.root.get_screen("questionnaire_test").ids.checkbox_instance.text
    #         print(f"Pressed checkbox ID: {checkbox_id}")
    #         print(f"Checkbox state: {checkbox_state}")
    #         print(f"Checkbox is checked. Extracting text from MDTextButton...")
    #         button_text = checkbox_instance.parent.ids.checkButton4.text  # Извлечение текста из MDTextButton
    #         print(f"Text from MDTextButton: {button_text}")

    def visionable(self):
        self.root.get_screen("start_use").ids.wait.opacity = 1

    def load_questionnaire(self):
        self.visionable()
        empty_qa()
        self.get_new_question()
        folder_path = "StructurePrompts"
        files = os.listdir(folder_path)
        folder_path_1 = "answers_from_users"
        file_name = "answers.json"
        file_path_1 = os.path.join(folder_path_1, file_name)

        # Создаем структуру данных для ответов
        questionnaire_data = {}
        for i in range(1, 26):
            card_key = f"card {i}"
            questionnaire_data[card_key] = {
                "question": "",
                "answer": ""
            }
        # Записываем данные в файл, перезаписывая его содержимое
        with open(file_path_1, 'w', encoding='utf-8') as file:
            json.dump(questionnaire_data, file, ensure_ascii=False, indent=4)

        for file_name in files:
            if file_name.endswith("_questionPrompt.json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    first_question = data[0]['1 Question']
                    print(first_question)
                    self.root.get_screen("questionnaire_test").ids.questionLabel.text = first_question
                    first_question_options = data[0].get('1 Options', {})
                    print(first_question_options)
                    for i, (option_key, option_text) in enumerate(first_question_options.items()):
                        button_id = f"checkButton{i + 1}"
                        button_text = option_text
                        self.root.get_screen("questionnaire_test").ids[button_id].text = button_text

    def load_question_and_answers(self, question_index):
        self.root.get_screen("questionnaire_test").ids.checkbox1.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox2.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox3.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox4.active = False

        folder_path = "StructurePrompts"
        files = os.listdir(folder_path)
        for file_name in files:
            if file_name.endswith("_questionPrompt.json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    question = data[question_index - 1][f"{question_index} Question"]
                    print(question)
                    self.root.get_screen("questionnaire_test").ids.questionLabel.text = question
                    options = data[question_index - 1].get(f"{question_index} Options", {})
                    print(options)
                    for i, (option_key, option_text) in enumerate(options.items()):
                        button_id = f"checkButton{i + 1}"
                        button_text = option_text
                        self.root.get_screen("questionnaire_test").ids[button_id].text = button_text

    def on_right_arrow_press(self):
        # Увеличиваем текущий индекс вопроса на 1
        self.root.get_screen("questionnaire_test").ids.checkbox1.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox2.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox3.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox4.active = False
        self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
        question_screen = self.root.get_screen("questionnaire_test")
        question_screen.ids.result_label1.opacity = 0
        question_screen.ids.result_label.opacity = 0
        self.current_question_index += 1
        # Загружаем вопрос и ответы для нового индекса
        self.load_question_and_answers(self.current_question_index)
        question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
        question_number = int(question.split('.')[0])
        folder_path_1 = "answers_from_users"
        file_name = "answers.json"
        file_path_1 = os.path.join(folder_path_1, file_name)
        # Извлекаем первую цифру из строки question
        # Получаем текст из label
        text = self.root.get_screen("questionnaire_test").ids.questionLabel.text
        # Разделяем текст по точке и берем первый элемент
        first_digit = int(text.split('.')[0].strip())
        print('firs_digit', first_digit)
        # Формируем ключ карточки
        card_key_to_search = f"card {first_digit}"
        # Загружаем данные из JSON-файла
        with open(file_path_1, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Извлекаем данные карточки по ключу из JSON
        card_data_to_search = data.get(card_key_to_search)
        print(' card_data_to_search', card_data_to_search)
        # Создаем словарь для сопоставления буквы ответа с числовым значением
        letter_to_number = {"A": 1, "B": 2, "C": 3, "D": 4}
        # Проверяем, существуют ли данные карточки
        if card_data_to_search:
            # Извлекаем ответ из данных карточки
            answer = card_data_to_search.get("answer")
            # Проверяем, не является ли ответ пустым

            # Делаем что-то с полученным ответом
            print('answer', answer)

            if answer.startswith(("A)", "B)", "C)", "D)")):
                # Извлекаем буквенное обозначение ответа
                letter = answer.strip()[0]
                # Получаем числовое значение ответа из словаря
                answer_number = letter_to_number.get(letter)
                print("eihiehjifjiefjf", answer_number)
                self.answer_number = answer_number
                print("eihiehjifjiefjfjfjfjfjfj", self.answer_number)
                # Устанавливаем активность чекбокса в соответствии с ответом
        if self.answer_number == 1:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
        if self.answer_number == 2:
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
        if self.answer_number == 3:
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
        if self.answer_number == 4:
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color

        if question_number == 2:
            self.root.get_screen("questionnaire_test").ids.cardleft.opacity = 1
            self.root.get_screen("questionnaire_test").ids.cardleft.disabled = False
        elif question_number == 25:
            self.root.get_screen("questionnaire_test").ids.cardright.opacity = 0
            self.root.get_screen("questionnaire_test").ids.cardright.disabled = True
            self.root.get_screen("questionnaire_test").ids.check.disabled = False
            self.root.get_screen("questionnaire_test").ids.check.opacity = 1
        if not answer:
            print("Answer is empty.")
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color

    def on_left_arrow_press(self):
        self.root.get_screen("questionnaire_test").ids.checkbox1.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox2.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox3.active = False
        self.root.get_screen("questionnaire_test").ids.checkbox4.active = False
        self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
        self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
        question_screen = self.root.get_screen("questionnaire_test")
        question_screen.ids.result_label1.opacity = 0
        question_screen.ids.result_label.opacity = 0
        # Уменьшаем текущий индекс вопроса на 1
        self.current_question_index -= 1

        self.load_question_and_answers(self.current_question_index)
        question = self.root.get_screen("questionnaire_test").ids.questionLabel.text
        question_number = int(question.split('.')[0])
        folder_path_1 = "answers_from_users"
        file_name = "answers.json"
        file_path_1 = os.path.join(folder_path_1, file_name)
        # Извлекаем первую цифру из строки question
        # Получаем текст из label
        text = self.root.get_screen("questionnaire_test").ids.questionLabel.text
        # Разделяем текст по точке и берем первый элемент
        first_digit = int(text.split('.')[0].strip())
        print('firs_digit', first_digit)
        # Формируем ключ карточки
        card_key_to_search = f"card {first_digit}"
        # Загружаем данные из JSON-файла
        with open(file_path_1, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # Извлекаем данные карточки по ключу из JSON
        card_data_to_search = data.get(card_key_to_search)
        print(' card_data_to_search', card_data_to_search)
        # Создаем словарь для сопоставления буквы ответа с числовым значением
        letter_to_number = {"A": 1, "B": 2, "C": 3, "D": 4}
        # Проверяем, существуют ли данные карточки
        if card_data_to_search:
            # Извлекаем ответ из данных карточки
            answer = card_data_to_search.get("answer")
            # Проверяем, не является ли ответ пустым

            # Делаем что-то с полученным ответом
            print('answer', answer)

            if answer.startswith(("A)", "B)", "C)", "D)")):
                # Извлекаем буквенное обозначение ответа
                letter = answer.strip()[0]
                # Получаем числовое значение ответа из словаря
                answer_number = letter_to_number.get(letter)
                print("eihiehjifjiefjf", answer_number)
                self.answer_number = answer_number
                print("eihiehjifjiefjfjfjfjfjfj", self.answer_number)
                # Устанавливаем активность чекбокса в соответствии с ответом
        if self.answer_number == 1:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
        if self.answer_number == 2:
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
        if self.answer_number == 3:
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
        if self.answer_number == 4:
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.blue_color
        else:
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color
        if question_number == 1:
            self.root.get_screen("questionnaire_test").ids.cardleft.opacity = 0
            self.root.get_screen("questionnaire_test").ids.cardleft.disabled = True
        elif question_number != 25:
            self.root.get_screen("questionnaire_test").ids.cardright.opacity = 1
            self.root.get_screen("questionnaire_test").ids.cardright.disabled = False
            self.root.get_screen("questionnaire_test").ids.check.disabled = True
            self.root.get_screen("questionnaire_test").ids.check.opacity = 0
        if not answer:
            print("Answer is empty.")
            self.root.get_screen("questionnaire_test").ids.checkButton1.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton2.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton3.color = self.black_color
            self.root.get_screen("questionnaire_test").ids.checkButton4.color = self.black_color


    def get_evaluation(self):
        file_path = "StructurePrompts/evaluation.json"

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Извлекаем текст из поля 'level' и 'recommendation'
        level_text = data.get('level', '')
        recommendation_text = data.get('recommendation', '')

        print("Текст из поля 'level':", level_text)
        print("Текст из поля 'recommendation':", recommendation_text)
        level = "[u]" + level_text + "[/u]"
        rec = "[u]" + recommendation_text + "[/u]"
        self.root.get_screen("feedback").ids.level.text = level
        self.root.get_screen("feedback").ids.recommendations.text = rec

    def check_question_answered(self):
        get_level_english()
        folder_path_1 = "answers_from_users"
        file_name = "answers.json"
        file_path_1 = os.path.join(folder_path_1, file_name)
        with open(file_path_1, 'r', encoding='utf-8') as file:
            data = json.load(file)

        unanswered_questions = []
        for i in range(1, 26):
            card_key = f"card {i}"
            card_data = data.get(card_key)
            if not card_data or not card_data.get("question") or not card_data.get("answer"):
                unanswered_questions.append(i)

        if unanswered_questions:
            print("Неотвеченные вопросы:", unanswered_questions)
            # Переход на страницу "feedback"
            color1 = (1, 0, 0, 1)  # Красный цвет текста

            # Устанавливаем текст и цвет сообщения
            question_screen = self.root.get_screen("questionnaire_test")
            question_screen.ids.result_label1.text = ', '.join(map(str, unanswered_questions))
            question_screen.ids.result_label.color = color1
            question_screen.ids.result_label1.color = color1
            question_screen.ids.result_label1.opacity = 1
            question_screen.ids.result_label.opacity = 1

        else:
            print("Все вопросы отвечены.")
            self.root.current = 'feedback'
            self.get_evaluation()

    def get_name_from_firebase(self):
        with open('Login_data/login_data.json', 'r') as file:
            data = json.load(file)

        # Извлекаем email и имя из JSON данных
        email = data.get('email')

        # Проверяем, что email не равен None
        if email is not None:
            # Получаем ссылку на базу данных Firebase
            ref = db.reference('/users')

            # Извлекаем имя пользователя по email из базы данных Firebase
            user_data = ref.order_by_child('email').equal_to(email).get()

            # Проверяем, был ли найден пользователь с таким email
            if user_data:
                # Получаем имя пользователя из данных пользователя
                user_name = next(iter(user_data.values()))['user_name']
                signup_screen = self.root.get_screen("profile")
                signup_screen.ids.profile_name.text = 'Hello ' + user_name
        else:
            print("Email отсутствует или равен None.")

    def redirect_to_login(self, dt):
        self.root.current = "login"

    def redirect_to_start_use(self, dt):
        self.root.current = "start_use"

    # def check_box(self, instance, value):
    #     if value:
    #         print("Checkbox is active")
    #     else:
    #         print("Checkbox is inactive")

    def save_login_data_to_json(self, email, password):
        # Создаем словарь с данными
        data = {'email': email, 'password': password}
        # Путь к JSON-файлу
        json_file_path = "Login_data/login_data.json"
        # Записываем данные в JSON-файл
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file)

    def load_login_data_from_json(self):
        # Путь к JSON-файлу
        json_file_path = "Login_data/login_data.json"
        try:
            # Пытаемся загрузить данные из JSON-файла
            with open(json_file_path, 'r') as json_file:
                login_data = json.load(json_file)
        except FileNotFoundError:
            # Если файл не найден, возвращаем пустой словарь
            login_data = {}
        return login_data

    def login(self):
        email = self.root.get_screen("login").ids.email_input.text
        password = self.root.get_screen("login").ids.password_input.text
        # login_user(email,password)
        remember_checkbox = self.root.get_screen("login").ids.remember_checkbox
        remember = remember_checkbox.active
        # print(remember)

        if not email or not password:
            message = "Please fill in all fields"
            color = (1, 0, 0, 1)  # Красный цвет текста
        else:
            # Вызываем функцию для регистрации пользователя
            result = login_user(email, password)
            if result == "Login successful":
                message = "Login successful"
                color = (0, 0.25, 0, 1)  # Зелёный цвет текста (темный)
                if remember:
                    self.save_login_data_to_json(email, password)
                else:
                    # Если флажок не активен, сохраняем None вместо данных
                    self.save_login_data_to_json(None, None)
                # Перенаправляем на страницу login
                Clock.schedule_once(self.redirect_to_start_use, 1)

            elif result == "User not found":
                message = "User not found!"
                color = (1, 0, 0, 1)  # Красный цвет текста
            elif result == "Incorrect password":
                message = "Incorrect password"
                color = (1, 0, 0, 1)  # Красный цвет текста
            else:
                message = "Unknown error occurred!"
                color = (1, 0, 0, 1)  # Красный цвет текста

        # Устанавливаем текст и цвет сообщения
        signup_screen = self.root.get_screen("login")
        signup_screen.ids.result_label.text = message
        signup_screen.ids.result_label.color = color

    def signup(self):
        email = self.root.get_screen("signup").ids.email_input.text
        name = self.root.get_screen("signup").ids.name_input.text
        password = self.root.get_screen("signup").ids.password_input.text

        # print(email,name,password)
        # print(register_user(email,name,password))
        # Проверяем, заполнены ли все поля
        if not email or not name or not password:
            message = "Please fill in all fields"
            color = (1, 0, 0, 1)  # Красный цвет текста
        else:
            # Вызываем функцию для регистрации пользователя
            result = register_user(name, email, password)
            if result == "User added":
                message = f"User {name} added successfully!"
                color = (0, 0.25, 0, 1)  # Зелёный цвет текста (темный)

                # Перенаправляем на страницу login
                Clock.schedule_once(self.redirect_to_login, 4)

            elif result == "User exist":
                message = "User already exists!"
                color = (1, 0, 0, 1)  # Красный цвет текста
            else:
                message = "Unknown error occurred!"
                color = (1, 0, 0, 1)  # Красный цвет текста

            # Очищаем текстовые поля после регистрации
            self.root.get_screen("signup").ids.email_input.text = ""
            self.root.get_screen("signup").ids.name_input.text = ""
            self.root.get_screen("signup").ids.password_input.text = ""

        # Устанавливаем текст и цвет сообщения
        signup_screen = self.root.get_screen("signup")
        signup_screen.ids.result_label.text = message
        signup_screen.ids.result_label.color = color

    def on_start(self):
        label_or = self.root.get_screen("login").ids.label_or
        label_or.color = (0, 0, 1, 1)
        login_data = self.load_login_data_from_json()
        self.get_name_from_firebase()
        email = login_data.get('email')
        password = login_data.get('password')
        if email is not None and password is not None:
            # Если данные есть, перенаправляем на страницу start_use
            self.root.current = 'start_use'
        else:
            # Если данных нет, перенаправляем на страницу main
            self.root.current = 'main'


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="Fonts/Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="Fonts/Poppins-SemiBold.ttf")

Slope().run()

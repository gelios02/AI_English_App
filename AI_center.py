import firebase_admin
from firebase_admin import credentials, db
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import openai
# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение ключа API из переменной окружения
api_key = os.getenv('OPENAI_API_KEY')

# Инициализация клиента OpenAI с использованием ключа API
openai.api_key = api_key

# Создание клиента
client = openai
# Инициализация приложения Firebase
cred = credentials.Certificate("FireBaseKey/englishapp-92af3-firebase-adminsdk-srxgg-74b6ccf882.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://englishapp-92af3-default-rtdb.firebaseio.com/'
})


def register_user(user_name, email, password):
    email_id = email.replace('@', '_').replace('.', ':')

    # Проверяем, существует ли уже пользователь с таким email
    users_ref = db.reference('users')
    if users_ref.child(email_id).get():
        return "User exist"

    # Создаем нового пользователя в базе данных Firebase
    new_user = {
        'user_name': user_name,
        'email': email,
        'password': password
    }
    users_ref.child(email_id).set(new_user)
    return "User added"


def login_user(email, password):
    email_id = email.replace('@', '_').replace('.', ':')

    # Проверяем, существует ли пользователь с таким email
    users_ref = db.reference('users')
    user_data = users_ref.child(email_id).get()
    if not user_data:
        return "User not found"

    # Проверяем правильность введенного пароля
    if user_data['password'] == password:
        return "Login successful"
    else:
        return "Incorrect password"


def get_question(email):
    # Очищаем существующий вопрос, если он есть
    users_ref = db.reference('users')
    email_id = email.replace('@', '_').replace('.', ':')
    if users_ref.child(email_id).child('questionPrompt').get():
        users_ref.child(email_id).child('questionPrompt').delete()

    # Запрашиваем вопрос у OpenAI
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": """Generate a test of 25 questions for me to assess my English grammar proficiency with 
             four possible answers and send it to me.All questions should start with the number dot, for example, 
             like this 1. The answers in the text should be short, no more than 4 words. 
             The answer options should be of this structure
             A)
             B)
             C)
             D)"""},
        ]
    )

    # Получаем ответ от OpenAI
    chat_response = completion.choices[0].message.content

    # Разбиваем ответ на блоки вопросов и ответов
    question_blocks = chat_response.strip().split('\n\n')
    # Формируем текст вопросов и вариантов ответов
    questions_text = ""
    question_num = 1
    for block in question_blocks:
        # Проверяем, начинается ли блок с цифры
        if block[0].isdigit():
            # Добавляем вопрос в текст
            questions_text += f"{block}\n"
            question_num += 1
    print(questions_text)
    # Записываем данные в базу данных Firebase
    users_ref.child(email_id).update({'questionPrompt': questions_text})

    # Парсинг каждого блока вопроса и ответа
    questions_answers = []
    question_num = 1
    for i, block in enumerate(question_blocks, 1):
        # Проверяем, является ли блок вопросом (начинается с цифры)
        if block[0].isdigit():
            lines = block.strip().split('\n')
            question = lines[0]
            options = {f'Option {chr(ord("a") + j)}': option.strip() for j, option in enumerate(lines[1:], 0)}
            questions_answers.append({f'{question_num} Question': f'{question}', f'{question_num} Options': options})
            question_num += 1

    # Создаем папку для хранения файлов, если она еще не существует
    if not os.path.exists('StructurePrompts'):
        os.makedirs('StructurePrompts')

    directory = 'StructurePrompts'
    files_to_remove = []

    # Перебираем все файлы в папке
    for filename in os.listdir(directory):
        # Проверяем, что файл имеет нужную структуру имени
        if filename.endswith('_questionPrompt.json'):
            # Получаем email из имени файла
            file_email = filename.split('_')[0]
            if file_email != email:
                # Добавляем файл в список на удаление
                files_to_remove.append(filename)

    # Удаляем все файлы, кроме тех, что в списке на удаление
    for filename in files_to_remove:
        file_path = os.path.join(directory, filename)
        os.remove(file_path)

    # Путь к файлу JSON
    json_file_path = f'StructurePrompts/{email}_questionPrompt.json'

    # Записываем данные в файл
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(questions_answers, f, ensure_ascii=False, indent=4)

    readiness = 'Ready'
    return readiness


def get_level_english():
    folder_path_1 = "answers_from_users"
    file_name = "answers.json"
    file_path_1 = os.path.join(folder_path_1, file_name)

    # Создаем пустую строку для хранения всех вопросов и ответов
    all_questions_and_answers = ""

    # Загружаем данные из файла JSON
    with open(file_path_1, 'r', encoding='utf-8') as file:
        data = json.load(file)

        # Перебираем данные для каждой карточки и формируем строку "вопрос - ответ"
        for card_key, card_data in data.items():
            question = card_data.get("question")
            answer = card_data.get("answer")
            # Формируем строку "вопрос - ответ" и добавляем ее к уже существующей строке
            all_questions_and_answers += f"{question} - {answer}\n"

    # Выводим все вопросы и ответы
    print("Все вопросы и ответы:")
    print(all_questions_and_answers)
    # Запрашиваем вопрос у OpenAI
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": """Based on the questions and my answers, evaluate my English level. Under the number 
             1. write me the English level in one word Beginner or Elementary or Pre-Intermediate or Intermediate or 
             Upper Intermediate or Advanced or Proficiency.
             And under the number 2. write me in one very short sentence in solid text 
             recommendations for improving my English
             Here is my test:""" + all_questions_and_answers},
        ]
    )
    # Получаем ответ от OpenAI
    chat_response = completion.choices[0].message.content
    print(chat_response)
    # Разделить ответ на строки
    lines = chat_response.split('\n')

    # Создать словарь для хранения данных
    evaluation_data = {}

    # Обработать каждую строку
    for line in lines:
        # Разделить строку по точке и пробелу
        parts = line.split('. ')
        # Получить номер и текст
        number = parts[0]
        text = parts[1]
        # Исключить цифры и точки из текста
        text = text.replace(number + '. ', '')
        # Добавить данные в словарь
        if number == '1':
            evaluation_data['level'] = text
        elif number == '2':
            evaluation_data['recommendation'] = text

    # Записать данные в JSON файл
    file_path = "StructurePrompts/evaluation.json"
    with open(file_path, 'w') as file:
        json.dump(evaluation_data, file, ensure_ascii=False, indent=4)

    print("Данные успешно записаны в файл evaluation.json.")


def parse_weekly_plan(text):
    cards = {}
    current_day = None
    current_advice = []
    card_number = 1
    for line in text.split('\n'):
        # Проверяем, является ли строка заголовком нового дня
        if line.startswith("Day"):
            # Если это новый день, сохраняем предыдущий
            if current_day is not None:
                # Добавляем текущую карту в словарь карт
                cards[f"Card {card_number}"] = {"number_day": current_day, "advice": '\n'.join(current_advice)}
                card_number += 1
                current_advice = []  # Очищаем рекомендации для нового дня
            # Извлекаем номер дня
            current_day = line.strip()
        # Проверяем, является ли строка частью рекомендаций для текущего дня
        elif current_day is not None:
            # Иначе добавляем текст в рекомендации для текущего дня
            current_advice.append(line.strip())
    # Сохраняем последний день
    if current_day is not None:
        # Добавляем последнюю карту в словарь карт
        cards[f"Card {card_number}"] = {"number_day": current_day, "advice": '\n'.join(current_advice)}
    return cards


def give_common_plan():
    # Здесь можете добавить код для получения общего плана из базы данных
    file_path = "StructurePrompts/qa.json"
    file_path1 = "StructurePrompts/evaluation.json"

    # Пытаемся прочитать содержимое файла JSON
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Извлекаем данные из файла и присваиваем переменным
    skill = data["skill"]
    days = data["days"]
    hours = data["hours"]

    # Выводим извлеченные данные
    print("Skill:", skill)
    print("Days:", days)
    print("Hours:", hours)

    with open(file_path1, 'r') as file:
        data1 = json.load(file)

    level = data1["level"]
    print("Level:", level)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"""Give me an English language learning plan for one week.I want to improve my {skill}. 
              My level is {level}.
              I can only devote {days} a week for {hours} a day. Write a plan by the numbers of the days.
              Form a plan based on my English level and how many days and hours I can devote.
              Form a plan with this structure  
              Day 1:  
              1. 
              2. 
              3.     
              4.
              Do not write anything other than this structure"""},
        ]
    )
    # Получаем ответ от OpenAI
    chat_response = completion.choices[0].message.content
    print(chat_response)
    # Разбиваем текст на блоки для каждого дня
    cards = parse_weekly_plan(chat_response)

    # Записываем данные в файл JSON
    with open("StructurePrompts/education_plan.json", "w") as file:
        json.dump(cards, file)


def empty_qa():
    file_path = "StructurePrompts/qa.json"

    # Пытаемся прочитать текущее содержимое файла
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Если файл еще не существует, создаем пустую структуру
        data = {"skill": "", "days": 0, "hours": 0}

    data["skill"] = 0
    data["days"] = 0
    data["hours"] = 0

    # Записываем обновленные данные в файл
    with open(file_path, 'w') as file:
        json.dump(data, file)

# empty_qa()
# get_level_english()
#     # Пример использования функций
#     user_name = "John"
#     email = "Globally@example.com"
#     password = "password123"
#
#     # print(register_user(email, email, password))
#     print(get_question(email))
#     # print(send_answer(email, "My answer"))
#     # print(give_common_plan(email))
#     # print(login_user("Globally@example.com","password123" ))

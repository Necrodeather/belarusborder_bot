from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from email.mime.text import MIMEText
from time import sleep
from winsound import Beep
from os import system
import json
import smtplib


with open("autorization.json", "r") as json_email:
    auto = json.load(json_email)


def send_email(message):

    sender = auto["Email_login"]
    password = auto["Email_password"]
    send = auto["to_Send"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = '[WARNING] Найдена бронь!'

        server.sendmail(sender, send, msg.as_string())
        return print("Оповещение успешно отправлено!")
    except Exception as _ex:
        return print(f"{_ex}\nПроверьте правильность написания логина и пароля!")


# Текст
category = 'Категория Транспортного средства\n1.Легковой автомобиль\n2.Грузовой автомобиль\n3.Автобус\n4.Легковой/пассажирский микроавтобус\n5.Мотоцикл'
сheckpoint = 'Пункт пропуска\n1.Урбаны\n2.Бенякони\n3.Каменный Лог\n4.Котловка\n5.Григоровщина'
text_choice = 'Выберите стиль работы:\n1.Автоматический\n2.Определенное время'
timing = '\n00-01 01-02 02-03 03-04 04-05 05-06\n06-07 07-08 08-09 09-10 10-11 11-12\n12-13 13-14 14-15 15-16 16-17 17-18\n18-19 19-20 20-21 21-22 22-23 23-00'
InputError = 'Ошибка ввода данных при выборе категории ТС и пункта пропуска!'
# Массив
tonws = ['Урбаны', 'Бенякони', 'Каменный Лог', 'Котловка', 'Григоровщина']
# Драйвер
options = Options()
useragent = UserAgent()
options.set_preference("general.useragent.override", useragent.random)
driver = webdriver.Firefox(options=options)
########################Ввод данных#############################################


def input_category():
    try:
        print(category)
        input_checkbox_one = int(input('Укажите цифрой данную категорию: '))
        print(сheckpoint)
        input_checkbox_two = int(
            input('Укахите цифрой данный пункт пропуска: '))
        return input_checkbox_one, input_checkbox_two,
    except ValueError:
        system('cls')
        print("Неправильное значение, введите заново")
        input_category()


def input_times():
    print(f'Выберите время бронирования из перечисленного: {timing}')
    input_time = input("Время: ")
    return input_time


def input_dates():
    try:
        input_day = int(input("Введите день: "))
        input_mouth = int(input("Введите месяц: "))
        input_year = int(input("Введите год: "))

        input_date = str(input_day) + '.' + \
            str(input_mouth) + '.' + str(input_year)
        return input_date
    except ValueError:
        system('cls')
        print("Неправильное значение, введите заново")
        input_dates()


def input_choice():
    print(text_choice)
    try:
        input_choice = int(input('Укажите цифрой определенный пункт: '))
    except ValueError:
        print("Неправильное значение, введите заново")
        input_times()

    if input_choice == 1:
        input_time = None
        return input_time
    elif input_choice == 2:
        input_time = input_times()
        return input_time
    else:
        print("Неправильное значение, введите заново")


def reboot():
    print('Продолжить поиск?\n1.Да\n2.Нет')
    reloading = int(input())
    if reloading == 1:
        main()
    elif reloading == 2:
        quit()
######################Кнопки################################################


def checkbox_click(i):
    checkbox = driver.find_elements(By.CLASS_NAME, ("label"))
    checkbox[i-1].click()


def btn_next_id_click():
    btn_next_id = driver.find_element(By.ID, ("next"))
    btn_next_id.click()


def btn_next_class_click():
    btn_next_class = driver.find_element(By.CLASS_NAME, ("next"))
    btn_next_class.click()


def slice(test):
    slice_text = test.text
    slice_text = slice_text[:5]
    return slice_text


def nav_btn():
    nav_btn_click = driver.find_element(By.CLASS_NAME, ("nav-btn"))
    nav_btn_click.click()

###########################Авторизация##################################


def autorization():

    with open("autorization.json", "r") as json_auto:
        auto = json.load(json_auto)

    inputElement = driver.find_elements(By.CLASS_NAME, ('input100'))
    inputElement[0].send_keys(auto["Login"])
    inputElement[0].send_keys(Keys.ENTER)
    sleep(3)
    inputElement[1].send_keys(auto["Password"])
    inputElement[1].send_keys(Keys.ENTER)
    sleep(5)

    retry_autorization()


def retry_autorization():
    try:
        timeout = driver.find_element(By.CLASS_NAME, ('activationInfo'))
        if timeout.text == "Время сессии истекло\nДля продолжения старого бронирования либо для создания нового повторно войдите в систему":
            btn_activation = driver.find_element(By.CLASS_NAME, ('activation'))
            btn_activation.click()
            autorization()
        else:
            pass
    except NoSuchElementException:
        pass
# Прохождение первого и второго этапа бронирования


class belarusborder_bot(object):

    def __init__(self, webdriver, number_check_one, number_check_two):
        self.webdriver = webdriver
        self.number_check_one = number_check_one
        self.number_check_two = number_check_two

    def first_queue(self):
        self.first_start()
        self.one_point()
        self.two_point()

    def first_start(self):
        self.webdriver.get("https://belarusborder.by")
        nav_btn()
        autorization()

    def one_point(self):
        self.webdriver.get("https://belarusborder.by/book")
        checkbox_click(self.number_check_one)
        btn_next_id_click()

    def two_point(self):
        checkbox_click(self.number_check_two)
        btn_next_class_click()

# Прохождение основного этапа для ловли брони.


class bot_step(object):

    def __init__(self, webdriver, date, town, time=None):
        self.webdriver = webdriver
        self.date = date
        self.time = time
        self.check_time = None
        self.check_control = None
        self.town = town

    def second_queue(self):
        self.start()
        self.refresh_side()

    def start(self):
        self.webdriver.refresh()
        self.webdriver.get(
            f"https://belarusborder.by/book/time?date={self.date}")

    def refresh_side(self):
        while True:
            sleep(1)
            self.webdriver.refresh()
            self.cycle_fisrt_time()

    def cycle_fisrt_time(self):

        self.check_time = self.webdriver.find_elements(By.CLASS_NAME, (
            "intervalAvailable"))
        if self.time == None:
            self.first_choice()
        else:
            for time in self.check_time:

                if slice(time) == self.time:
                    time.click()
                else:
                    continue
            self.cycle_two_time()

    def first_choice(self):
        url = self.webdriver.current_url
        date = url[-10:].replace("=", "")
        try:
            self.check_time[0].click()
            check_time = self.check_time[0].text
            for sound in range(1):
                Beep(440, 250)
                sleep(0.25)
                system('cls')
                print('Найдена бронь!')

            btn_next_id_click()

            for sound in range(10):
                Beep(440, 250)
                sleep(0.25)
                system('cls')
                print('Найдена бронь!')
            send_email(
                f'Найдена бронь на аккаунте: {auto["Login"]}\nДата: {date}\nПункт: {self.town}\nВремя: {check_time[:5]}\nURL: {url}')
            self.webdriver.implicitly_wait(5)
            self.info = self.webdriver.find_elements(
                By.CLASS_NAME, ('form-control'))
            self.info[-1].send_keys(f'{self.town} {check_time[:5]} {date[:5]}')
            input('После ввода данных нажмите Enter...')
            json_email.close()
            self.webdriver.close()
            reboot()
        except IndexError:
            return False

    def cycle_two_time(self):
        try:
            url = self.webdriver.current_url
            date = url[-10:].replace("=", "")
            self.check_time = self.webdriver.find_elements(By.CLASS_NAME, (
                "intervalAvailable"))
            self.check_control = self.webdriver.find_element(By.CLASS_NAME, (
                "intervalSelected"))
            if slice(self.check_control) == self.time:
                check_time = self.check_control.text
                for sound in range(1):
                    Beep(440, 250)
                    sleep(0.25)
                    system('cls')
                    print('Найдена бронь!')

                btn_next_id_click()

                for sound in range(10):
                    Beep(440, 250)
                    sleep(0.25)
                    system('cls')
                    print('Найдена бронь!')
                send_email(
                    f'Найдена бронь на аккаунте: {auto["Login"]}\nДата: {date}\nПункт: {self.town}\nВремя: {check_time[:5]}\nURL: {url}')
                self.webdriver.implicitly_wait(5)
                self.info = self.webdriver.find_elements(
                    By.CLASS_NAME, ('form-control'))
                self.info[-1].send_keys(
                    f'{self.town} {check_time[:5]} {date[:5]}')
                input('После ввода данных нажмите Enter...')
                json_email.close()
                self.webdriver.close()
                reboot()

        except NoSuchElementException:
            return False


def main():
    input_checkbox_one, input_checkbox_two = input_category()
    town = tonws[input_checkbox_two - 1]
    input_date = input_dates()
    first_step = belarusborder_bot(
        driver, input_checkbox_one, input_checkbox_two)
    second_step = bot_step(driver, input_date, town, input_choice())
    first_step.first_queue()
    second_step.second_queue()


if __name__ == '__main__':
    main()

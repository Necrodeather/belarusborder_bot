from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from time import sleep
from winsound import Beep
from os import system
import json

# Текст
category = 'Категория Транспортного средства\n1.Легковой автомобиль\n2.Грузовой автомобиль\n3.Автобус\n4.Легковой/пассажирский микроавтобус\n5.Мотоцикл'
сheckpoint = 'Пункт пропуска\n1.Урбаны\n2.Бенякони\n3.Каменный Лог\n4.Котловка\n5.Григоровщина'
timing = '\n00-01 01-02 02-03 03-04 04-05 05-06\n06-07 07-08 08-09 09-10 10-11 11-12\n12-13 13-14 14-15 15-16 16-17 17-18\n18-19 19-20 20-21 21-22 22-23 23-00'
InputError = 'Ошибка ввода данных при выборе категории ТС и пункта пропуска!'
# Драйвер
driver = webdriver.Firefox()
########################Ввод данных#############################################
def input_dates():
    try:
        print(category)
        input_checkbox_one = int(input('Укажите цифрой данную категорию: '))
        print(сheckpoint)
        input_checkbox_two = int(
            input('Укахите цифрой данный пункт пропуска: '))

        input_day = int(input("Введите день: "))
        input_mouth = int(input("Введите месяц: "))
        input_year = int(input("Введите год: "))

        input_date = str(input_day) + '.' + \
            str(input_mouth) + '.' + str(input_year)
        print('Выберите время бронирования из перечисленного: '+timing)
        input_time = input("Время: ")

        return input_checkbox_one, input_checkbox_two, input_date, input_time
    except ValueError:
        system('cls')
        print("Неправильное значение, введите заново")
        main()

######################Кнопки################################################
def checkbox_click(i):
    checkbox = driver.find_elements_by_class_name("label")
    checkbox[i-1].click()

def btn_next_id_click():
    btn_next_id = driver.find_element_by_id("next")
    btn_next_id.click()

def btn_next_class_click():
    btn_next_class = driver.find_element_by_class_name("next")
    btn_next_class.click()

def slice(test):
    slice_text = test.text
    slice_text = slice_text[:5]
    return slice_text

def nav_btn():
    nav_btn_click = driver.find_element_by_class_name("nav-btn")
    nav_btn_click.click()

###########################Авторизация##################################
def autorization():

    with open("autorization.json", "r") as json_auto:
        auto = json.load(json_auto)

    inputElement = driver.find_elements_by_class_name('input100')
    inputElement[0].send_keys(auto["Login"])
    inputElement[0].send_keys(Keys.ENTER)
    sleep(3)
    inputElement[1].send_keys(auto["Password"])
    inputElement[1].send_keys(Keys.ENTER)
    sleep(5)
    #inputbutton = driver.find_element_by_class_name('login100-form-btn')
    #inputbutton.click()
    sleep(10)
    json_auto.close()

    retry_autorization()

def retry_autorization():
    try:
        timeout = driver.find_element_by_class_name('activationInfo')
        if timeout.text == "Время сессии истекло\nДля продолжения старого бронирования либо для создания нового повторно войдите в систему":
            btn_activation = driver.find_element_by_class_name('activation')
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

    def __init__(self, webdriver, date, time):
        self.webdriver = webdriver
        self.date = date
        self.time = time
        self.check_time = None
        self.check_control = None

    def second_queue(self):
        self.start()
        self.cycle_fisrt_time()
        self.cycle_two_time()

    def start(self):
        self.webdriver.refresh()
        self.webdriver.get(
            "https://belarusborder.by/book/time?date=" + self.date)

    def cycle_fisrt_time(self):

        self.check_time = self.webdriver.find_elements_by_class_name(
            "intervalAvailable")

        for time in self.check_time:

            if slice(time) == self.time:
                time.click()
            else:
                continue

    def cycle_two_time(self):
        try:
            self.check_time = self.webdriver.find_elements_by_class_name(
                "intervalAvailable")
            self.check_control = self.webdriver.find_element_by_class_name(
                "intervalSelected")
            if slice(self.check_control) == self.time:
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
                sleep(7200)

        except NoSuchElementException:
            try:
                while True:
                    sleep(1)
                    system('cls')
                    self.webdriver.refresh()
                    bot_step.cycle_fisrt_time(self)
                    bot_step.cycle_two_time(self)
            except RecursionError:
                pass
        except TimeoutException:
            pass

def main():
    input_checkbox_one, input_checkbox_two, input_date, input_time = input_dates()
    first_step = belarusborder_bot(
        driver, input_checkbox_one, input_checkbox_two)
    second_step = bot_step(driver, input_date, input_time)
    first_step.first_queue()
    second_step.second_queue()

if __name__ == '__main__':
    main()
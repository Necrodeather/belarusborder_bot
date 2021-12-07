from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep
from winsound import Beep
from os import system

# Текст
category = 'Категория Транспортного средства\n1.Легковой автомобиль\n2.Грузовой автомобиль\n3.Автобус\n4.Легковой/пассажирский микроавтобус\n5.Мотоцикл'
сheckpoint = 'Пункт пропуска\n1.Брест\n2.Урбаны\n3.Бенякони\n4.Котловка\n5.Григоровщина'
timing = '\n00-01 01-02 02-03 03-04 04-05 05-06\n06-07 07-08 08-09 09-10 10-11 11-12\n12-13 13-14 14-15 15-16 16-17 17-18\n18-19 19-20 20-21 21-22 22-23 23-00'
InputError = 'Ошибка ввода данных при выборе категории ТС и пункта пропуска!'
# Отключение логов драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# Драйвер
driver = webdriver.Chrome(options=options)

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
#################################################################################
# Кнопки


def checkbox_click(i):
    checkbox = driver.find_elements_by_class_name("label")
    checkbox[i-1].click()


def btn_next_id_click():
    btn_next_id = driver.find_element_by_id("next")
    try:
        btn_next_id.click()
    except ElementClickInterceptedException:
        btn_next_id_click()


def btn_next_class_click():
    btn_next_class = driver.find_element_by_class_name("next")
    btn_next_class.click()


def slice(test):
    slice_text = test.text
    slice_text = slice_text[:5]
    return slice_text


def captcha():
    capt = driver.find_element_by_tag_name('iframe')
    print(capt.text)
    capt.click()


# Авторизация
def autorization():
    inputElement = driver.find_elements_by_class_name('input100')
    print(len(inputElement))
    inputElement[0].send_keys('')#Логин
    inputElement[0].send_keys(Keys.ENTER)
    inputElement[1].send_keys('')#Пароль
    inputElement[1].send_keys(Keys.ENTER)
    inputbutton = driver.find_element_by_class_name('login100-form-btn')
    inputbutton.click()

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
        try:
            self.webdriver.get("https://belarusborder.by/book")
        except WebDriverException:
            quit()

    def one_point(self):
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

        try:
            self.check_time = self.webdriver.find_elements_by_class_name(
                "intervalAvailable")
        except WebDriverException:
            quit()

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
                for sound in range(5):
                    Beep(440, 250)
                    sleep(0.25)
                    system('cls')
                    print('Найдена бронь!')
                
                captcha()
                btn_next_id_click()
                autorization()
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
                    self.webdriver.refresh()
                    bot_step.cycle_fisrt_time(self)
                    bot_step.cycle_two_time(self)
            except RecursionError:
                pass

###################Осталось написать автоматическую авторизацию##########################################

def main():
    input_checkbox_one, input_checkbox_two, input_date, input_time = input_dates()
    first_step = belarusborder_bot(
        driver, input_checkbox_one, input_checkbox_two)
    second_step = bot_step(driver, input_date, input_time)
    first_step.first_queue()
    second_step.second_queue()


if __name__ == '__main__':
    main()

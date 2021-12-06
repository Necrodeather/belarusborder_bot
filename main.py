from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from winsound import Beep
from os import system

#Текст
category = 'Категория Транспортного средства\n1.Легковой автомобиль\n2.Грузовой автомобиль\n3.Автобус\n4.Легковой/пассажирский микроавтобус\n5.Мотоцикл'
сheckpoint  = 'Пункт пропуска\n1.Брест\n2.Урбаны\n3.Бенякони\n4.Котловка\n5.Григоровщина'
timing = '\n00-01 01-02 02-03 03-04 04-05 05-06\n06-07 07-08 08-09 09-10 10-11 11-12\n12-13 13-14 14-15 15-16 16-17 17-18\n18-19 19-20 20-21 21-22 22-23 23-00'
InputError = 'Ошибка ввода данных!'
#Отключение логов драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#Драйвер
driver = webdriver.Chrome(options=options)

#########################Исключения############################################
def input_errors(ico,ict,id,im,iy):
        if len(str(ico)) and len(str(ict)) == 1:
                pass
        elif len(str(id)) and len(str(im)) == 2 and len(str(iy)) == 4:
                pass
        else:   #WTF????!!!
                driver.close
                system('cls')
                print(InputError)
                main()
########################Ввод данных#############################################
def input_dates():
        try:
                print(category)
                input_checkbox_one = int(input('Укажите цифрой данную категорию: '))
                print(сheckpoint)
                input_checkbox_two = int(input('Укахите цифрой данный пункт пропуска: '))

                input_day = int(input("Введите день: "))
                input_mouth = int(input("Введите месяц: "))
                input_year = int(input("Введите год: "))
                input_errors(input_checkbox_one, input_checkbox_two, input_day, input_mouth, input_year)
                input_date = str(input_day) + '.' + str(input_mouth) + '.' + str(input_year)
                print('Выберите время бронирования из перечисленного: '+timing)
                input_time = input("Время: ")

                return input_checkbox_one, input_checkbox_two, input_date, input_time
        except ValueError:
                system('cls')
                print("Неправильное значение, введите заново")
                input_dates()

#################################################################################
#Кнопки
def checkbox_click(i):
        try:
                checkbox = driver.find_elements_by_class_name("label")
                checkbox[i-1].click()
        except IndexError:
                system('cls')
                print(InputError)
                input_dates()

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
#Прохождение первого и второго этапа бронирования
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
                self.webdriver.get("https://belarusborder.by/book")

        def one_point(self):               
                checkbox_click(self.number_check_one)
                btn_next_id_click()

        def two_point(self):
                checkbox_click(self.number_check_two)
                btn_next_class_click()

#Прохождение основного этапа для ловли брони.
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
                self.webdriver.get("https://belarusborder.by/book/time?date=" + self.date)

        def cycle_fisrt_time(self):
                self.check_time = self.webdriver.find_elements_by_class_name("intervalAvailable")
                for time in self.check_time:
                        
                        if slice(time) == self.time:
                                time.click()
                        else:        
                                continue

        def cycle_two_time(self):
                try:
                        self.check_time = self.webdriver.find_elements_by_class_name("intervalAvailable")
                        self.check_control = self.webdriver.find_element_by_class_name("intervalSelected")
                        if slice(self.check_control) == self.time:

                                for sound in range(60):
                                        Beep(440, 250)
                                        sleep(0.25)
                                        system('cls')
                                        print('Найдена бронь!')

                                input("Пройдите капчу и нажмите Enter")                                       
                                btn_next_id_click()

                except NoSuchElementException:
                        while True:
                                self.webdriver.refresh()
                                bot_step.cycle_fisrt_time(self)
                                bot_step.cycle_two_time(self)

###################Осталось написать автоматическую авторизацию##########################################

def main():
        input_checkbox_one, input_checkbox_two, input_date, input_time = input_dates()
        first_step = belarusborder_bot(driver, input_checkbox_one, input_checkbox_two)
        second_step = bot_step(driver, input_date, input_time)
        first_step.first_queue()
        second_step.second_queue()
        rebooting()

def rebooting():
        reboot = int(input('Продолжить работу?\n1.Да\n2.Нет\n: '))
        match reboot:
                case 1: 
                        main()
                case 2:
                        quit()
                case _:
                        system('cls')
                        print('Неверное значение\n')
                        rebooting()        


if __name__ == '__main__':
        main()
from selenium import webdriver
from time import sleep

checkbox = driver.find_elements_by_class_name("label")
btn_next_id = driver.find_element_by_id("next")
btn_next_class = driver.find_element_by_class_name("next")

class belarusborder_bot(object):

        def __init__(self, driver, date, time, number_check_one, number_check_two):
                self.driver = driver
                self.date = date
                self.time = time
                self.number_check_one = number_check_one
                self.number_check_two = number_check_two

        def Queue(self):
                self.first_start()
                self.one_point()
                self.two_point()

        def first_start(self):
                self.driver.get("https://belarusborder.by/book")

        def one_point(self):               
                checkbox[self.number_check_one - 1].click()
                btn_next_id.click()

        def two_point(self):
                checkbox[self.number_check_two - 1].click()
                btn_next_class.click()

class bot_step(object):

        def __init__(self):
                pass

        
        date= driver.get("https://belarusborder.by/book/time?date=" + input_date)

        timer = input("На какое время: ")
        driver.refresh()
        times = driver.find_elements_by_class_name("intervalAvailable")
        for time in times:
                
                str_time = time.text
                str_time = str_time[:5]

                if str_time == timer:
                        time.click()
                        break
                else:        
                        continue

        test = driver.find_element_by_class_name("intervalSelected")
        str_test = test.text
        str_test = str_test[:5]

        if str_test == timer:
                print('true')
        input("(Пройдите капчу и нажмите Enter) ")
        btn_next_id.click()
        sleep(15)


input_date = input("Дата: ")
driver = webdriver.Firefox()

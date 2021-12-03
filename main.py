from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()
driver.get("https://belarusborder.by/book")

inp = driver.find_elements_by_class_name("label")
inp[3].click()

btn = driver.find_element_by_id("next")
btn.click()

inp = driver.find_elements_by_class_name("label")
inp[3].click()

btn = driver.find_element_by_class_name("next")
btn.click()

i = 0
times = driver.find_elements_by_class_name("intervalAvailable")
timer = input("На какое время: ")
for time in times:
        
        str_time = time.text
        str_time = str_time[:5]

        while str_time != timer:
                break
        else:
                i=+1

print(i)
times[i-1].click()
test = driver.find_element_by_class_name("intervalSelected")
str_test = test.text
str_test = str_test[:5]

if str_test == timer:
        print('true')

# dates = driver.find_elements_by_css_selector("td.day")
# old_dates = driver.find_elements_by_css_selector("td.old")
# disables_dates = driver.find_elements_by_css_selector("td.disabled")
# for data in dates:
#     for old_data in old_dates:
#         for disable_data in disables_dates:
#             if data != old_data and disable_data:
#                 print(data.__class__.text)
#             else:
#                 print('-')

sleep(15)
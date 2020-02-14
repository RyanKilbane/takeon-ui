from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import config_test
# from datetime import datetime

chromedriver_location = config_test.CHROME_DRIVER_LOCATION


# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# driver = webdriver.Chrome(chromedriver_location, options=option)
# The above commented code can make it to run in a single tab
driver = webdriver.Chrome(chromedriver_location)

# Dtime = datetime.now().strftime("%d:%m:%Y-%H:%M:%S")
# print(Dtime)

#
driver.get(config_test.UI_URL)
main_window = driver.current_window_handle



# Get the url of minikube flask url - Command in 

search_button = '/html/body/div[2]/main/form/fieldset/span/button'
second_search_button = '/html/body/section/div[2]/div/div/div/form/button'

driver.find_element_by_xpath(search_button).click()

reference_search = '//*[@id="reference"]'
driver.find_element_by_xpath(reference_search).send_keys(config_test.REFERENCE)

driver.find_element_by_xpath(second_search_button).click()

view_form_button = '//*[@id="search_results_body"]/tr[2]/td[1]/a/button'
driver.find_element_by_xpath(view_form_button).click()
# driver.implicitly_wait(10)
# time.sleep(10)


# Switch tab to the new tab, which we will assume is the next one on the right
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
driver.switch_to.window(driver.window_handles[1])
#driver.switch_to.window(main_window)

ids = driver.find_elements_by_xpath('//*[@id]')
# for ii in ids:
    # print (ii.get_attribute('id'))

# print(str(driver.window_handles))

edit_button = '//*[@id="editFormButton"]'
# element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(By.ID, "editFormButton"))
# element.click()
# driver.implicitly_wait(5)
driver.find_element_by_xpath(edit_button).click()

# Input data for testing
q1_input = '/html/body/div[3]/div/div[1]/form/div[1]/input'
driver.find_element_by_xpath(q1_input).clear()
driver.find_element_by_xpath(q1_input).send_keys('50')

q2_input = '/html/body/div[3]/div/div[1]/form/div[2]/input'
driver.find_element_by_xpath(q2_input).clear()
driver.find_element_by_xpath(q2_input).send_keys('60')

save_form_button = '//*[@id="saveFormButton"]'
driver.find_element_by_xpath(save_form_button).click()

# time.sleep(5)

# Close alert
#WebDriverWait(driver, 5).until(EC.alert_is_present()
alert_obj = driver.switch_to.alert
alert_obj.accept()

exit_button = '//*[@id="exitButton"]'
driver.find_element_by_xpath(exit_button).click()

# Close current tab
#driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

# Put focus on current window which will be the window opener
#driver.switch_to.window(main_window)

# Go back to previous tab
driver.switch_to.window(driver.window_handles[0])
driver.quit()

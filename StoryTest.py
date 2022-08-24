import unittest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")


class StoryTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")

    def test_SuggestionClassExample(self):
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="autocomplete"]'))) \
            .send_keys('Me')
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//div[contains(.,"Mexico")]'))) \
            .click()

    def test_DropDownExample(self):
        self.dropdown = WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="dropdown-class-example"]')))
        self.ddselect = Select(self.dropdown)
        self.ddselect.select_by_index(1)
        time.sleep(2)
        self.ddselect.select_by_index(2)
        time.sleep(2)

    def test_SwitchWindowExample(self):
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="openwindow"]'))) \
            .click()
        time.sleep(5)
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)
        try:
            time.sleep(5)
            WebDriverWait(self.driver, 5) \
                .until(expected_conditions.presence_of_element_located(
                (By.XPATH, '//div[@class="col-sm-9"]/h3[text()="30 day Money Back Guarantee"]')))
        except NoSuchElementException:
            self.assertEqual('Texto No Encontrado')

    def test_SwitchTabExample(self):
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '// *[ @ id = "opentab"]'))) \
            .click()
        time.sleep(2)
        window_after = self.driver.window_handles[1]
        window_before = self.driver.window_handles[0]
        self.driver.switch_to.window(window_after)
        element2 = WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/section[2]/div[2]/a')))
        actions = ActionChains(self.driver)
        actions.move_to_element(element2).perform()
        time.sleep(2)
        self.driver.switch_to.window(window_before)
        time.sleep(2)

    def test_SwitchToAlertExample(self):
        inputAlert = WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="name"]')))
        inputAlert.send_keys('Stori Card')
        time.sleep(2)
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="alertbtn"]'))) \
            .click()
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.alert_is_present())
        time.sleep(2)
        self.driver.switch_to.alert.accept()
        time.sleep(2)
        self.driver.switch_to.default_content()
        inputAlert.send_keys('Stori Card')
        time.sleep(2)
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.element_to_be_clickable((By.XPATH, '// *[ @ id = "confirmbtn"]'))) \
            .click()
        time.sleep(2)
        alert_text = self.driver.switch_to.alert.text
        assert alert_text == 'Hello Stori Card, Are you sure you want to confirm?'
        time.sleep(2)

    def test_WebTableExample(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table[name='courses'] > tbody >tr > td")
        count = 0
        for index, row in enumerate(rows):
            if row.text == "25":
                print("\n Title = " + rows[index - 1].text)
                count = count + 1
        print("\n Total = " + str(count))

    def test_WebTableFixedHeaderExample(self):
        rows = self.driver.find_elements(By.CSS_SELECTOR, "div.tableFixHead > table > tbody > tr > td")
        for index, row in enumerate(rows):
            if row.text == "Engineer":
                print("\n Engineer Name = " + rows[index - 1].text)

    def test_iframeExample(self):
        self.driver.switch_to.frame(0)
        element = WebDriverWait(self.driver, 5) \
            .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.list-column:nth-child(2) li:nth-child(2)')))
        print(element.text)

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

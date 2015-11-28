from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time

XSS_STRINGS = ['<image src="doesnotexist" onerror=alert("HACKED12345")></img>']

class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        time.sleep(5)
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_xss(self):
        for attackstring in XSS_STRINGS:
            self.selenium.get('%s%s' % (self.live_server_url, '/list/'))
            numbuttons = len(self.selenium.find_elements(By.XPATH, "//*[@onclick]"))
            for i in range(numbuttons):
                try:
                    alert = self.selenium.switch_to_alert()
                    alert.accept()
                except:
                    pass
                self.selenium.get('%s%s' % (self.live_server_url, '/list/'))
                buttons = self.selenium.find_elements(By.XPATH, "//*[@onclick]")
                txtfields = self.selenium.find_elements(By.XPATH, "//input[@type='text']") + \
                    self.selenium.find_elements(By.XPATH, "//textarea")
                numfields = len(txtfields)
                for field in txtfields:
                    field.send_keys(attackstring)
                buttons[i].click()
                try:
                    WebDriverWait(self.selenium, 1).until(EC.alert_is_present(),
                                                   'Timed out waiting for PA creation ' +
                                                   'confirmation popup to appear.')

                    alert = self.selenium.switch_to_alert()
                    alert.accept()
                    for j in range(numfields):
                        try:
                            alert = self.selenium.switch_to_alert()
                            alert.accept()
                        except:
                            pass
                        self.selenium.refresh()
                        self.selenium.get('%s%s' % (self.live_server_url, '/list/'))
                        buttons = self.selenium.find_elements(By.XPATH, "//*[@onclick]")
                        txtfields = self.selenium.find_elements(By.XPATH, "//input[@type='text']") + \
                            self.selenium.find_elements(By.XPATH, "//textarea")
                        txtfields[j].send_keys(attackstring)
                        buttons[i].click()
                        try:
                            WebDriverWait(self.selenium, 1).until(EC.alert_is_present(),
                                                           'Timed out waiting for PA creation ' +
                                                           'confirmation popup to appear.')

                            alert = self.selenium.switch_to_alert()
                            if alert.text == "HACKED12345":
                                alert.accept()
                                print "VULNERABILITY FOUND"
                                print "To attack string:", attackstring
                                print "On button of type:", buttons[i].tag_name, "  At point:", buttons[i].location, "  Showing text (if any):", buttons[i].text
                                print "On textfield of type:", txtfields[j].tag_name, "  At point:", txtfields[j].location, "  Showing text (if any):", txtfields[j].text
                                print
                            else:
                                alert.accept()
                        except TimeoutException:
                            pass
                except TimeoutException:
                    print "no alert"
                    print
                self.selenium.refresh()

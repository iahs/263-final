from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import json
import os

with open('attackstrings.txt') as f:
    XSS_STRINGS = f.read().splitlines()



class MySeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.refresh()
        time.sleep(5)
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def clear_alert(self):
        try:
            alert = self.selenium.switch_to_alert()
            alert.accept()
        except:
            pass

    def test_xss(self):

        with open('temp.json', 'r') as infile:
            data = json.load(infile)
        os.remove('temp.json')

        for url in data['url']:
            if url != '/':
                url = '/' + url + '/'
            for attackstring in XSS_STRINGS:
                print "On URL:", url, "  Testing attack string:", attackstring
                print
                if data['query'] is not None:
                    for query in data['query']:
                        self.clear_alert()
                        self.selenium.get('%s%s' % (self.live_server_url, '/' + url + '/?' + query + '=' + attackstring))
                        try:
                            WebDriverWait(self.selenium, 1).until(EC.alert_is_present(),
                                                           'Timed out waiting for PA creation ' +
                                                           'confirmation popup to appear.')

                            alert = self.selenium.switch_to_alert()
                            if alert.text == "XSS":
                                alert.accept()
                                print "VULNERABILITY FOUND"
                                print "To attack string:", attackstring
                                print "On query string:",  query
                                print "On URL:", url
                                print
                            else:
                                alert.accept()
                        except TimeoutException:
                            pass
                        self.selenium.refresh()
                self.clear_alert()
                self.selenium.get('%s%s' % (self.live_server_url, url))
                numbuttons = len(self.selenium.find_elements(By.XPATH, "//*[@onclick]")) + len(self.selenium.find_elements(By.XPATH, "//*[@type='submit']"))
                for i in range(numbuttons):
                    self.clear_alert()
                    self.selenium.get('%s%s' % (self.live_server_url, url))
                    buttons = self.selenium.find_elements(By.XPATH, "//*[@onclick]") + \
                        self.selenium.find_elements(By.XPATH, "//*[@type='submit']")
                    txtfields = self.selenium.find_elements(By.XPATH, "//input[@type='text']") + \
                        self.selenium.find_elements(By.XPATH, "//textarea")
                    numfields = len(txtfields)
                    for field in txtfields:
                        field.send_keys(attackstring)
                    buttons[i].click()
                    if 'onclick=javascript:alert(String.fromCharCode(88,83,83))' in attackstring:
                        try:
                            vul = self.selenium.find_element(By.XPATH, '//*[@class="classhacked12345"]')
                            vul.click()
                        except:
                            pass
                    try:
                        WebDriverWait(self.selenium, 1).until(EC.alert_is_present(),
                                                       'Timed out waiting for PA creation ' +
                                                       'confirmation popup to appear.')

                        alert = self.selenium.switch_to_alert()
                        alert.accept()
                        for j in range(numfields):
                            self.clear_alert()
                            self.selenium.get('%s%s' % (self.live_server_url, url))
                            buttons = self.selenium.find_elements(By.XPATH, "//*[@onclick]") + \
                                self.selenium.find_elements(By.XPATH, "//*[@type='submit']")
                            txtfields = self.selenium.find_elements(By.XPATH, "//input[@type='text']") + \
                                self.selenium.find_elements(By.XPATH, "//textarea")
                            txtfields[j].send_keys(attackstring)
                            b_tn, b_l, b_t =  buttons[i].tag_name,  buttons[i].location,  buttons[i].text
                            t_tn, t_l, t_t = txtfields[j].tag_name, txtfields[j].location, txtfields[j].text
                            buttons[i].click()
                            if 'onclick=javascript:alert(String.fromCharCode(88,83,83))' in attackstring:
                                try:
                                    vul = self.selenium.find_element(By.XPATH, '//*[@class="classhacked12345"]')
                                    vul.click()
                                except:
                                    pass
                            try:
                                WebDriverWait(self.selenium, 1).until(EC.alert_is_present(),
                                                               'Timed out waiting for PA creation ' +
                                                               'confirmation popup to appear.')

                                alert = self.selenium.switch_to_alert()
                                if alert.text == "XSS":
                                    alert.accept()
                                    print "VULNERABILITY FOUND"
                                    print "To attack string:", attackstring
                                    print "On button of type:", b_tn, "  At point:", b_l, "  Showing text (if any):", b_t
                                    print "On textfield of type:", t_tn, "  At point:", t_l, "  Showing text (if any):", t_t
                                    print "On URL:", url
                                    print
                                else:
                                    alert.accept()
                            except TimeoutException:
                                pass
                    except TimeoutException:
                        #print "no alert"
                        #print
                        pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="XSS Penetration Tester")
    parser.add_argument('url', metavar="URL", type=str, nargs='+', help="URLs to attack")
    parser.add_argument('--query', dest='query', metavar="Query Strings", type=str, nargs='+', help="Query Strings to attack")
    args = parser.parse_args()
    url = args.url
    query = args.query

    argdict = {'url': url, 'query': query}

    with open('temp.json', 'w') as outfile:
        json.dump(argdict, outfile)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackmelists.settings")

    from django.core.management import execute_from_command_line


    execute_from_command_line(['manage.py', 'test', 'xss_test.MySeleniumTests.test_xss'])

    if os.path.isfile('temp.json'):
        os.remove('temp.json')

from django.test import TestCase, Client

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class HomePageTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, 'Django-Charting')
        self.assertContains(response, '<canvas', count=8)
        self.assertContains(response, 'new Chart(ctx, {', count=8)

    def test_home_async(self):
        response = self.client.get('/async/')
        self.assertContains(response, 'Django-Charting')
        self.assertContains(response, '<canvas', count=6)
        self.assertContains(response, 'new Chart(ctx, configuration);', count=6)


class SeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_home(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_class_name('chart')
        logs = self.selenium.get_log('browser')

        for log in logs:
            if 'favicon.ico' in log['message']:
                continue
            self.assertEquals(log['message'], '')

    def test_home_async(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/async/'))
        self.selenium.find_element_by_class_name('chart')
        logs = self.selenium.get_log('browser')

        for log in logs:
            if 'favicon.ico' in log['message']:
                continue
            self.assertEquals(log['message'], '')

import os

from django.test import TestCase, Client

from selenium.webdriver.chrome.webdriver import WebDriver


class HomePageTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, 'Django-JChart')
        self.assertContains(response, '<canvas', count=14)
        self.assertContains(response, 'new Chart(ctx, {', count=7)
        self.assertContains(response, 'new Chart(ctx, configuration', count=8)

if not os.environ.get('CI', False):
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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

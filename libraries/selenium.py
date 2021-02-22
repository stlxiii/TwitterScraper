import os, datetime, time, traceback
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys as keys
#from selenium.common.exceptions import StaleElementReferenceException


class _selenium(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.timeout = 5
        self.debug = False


    def click(self, locator, timeout=None):
        if timeout is None: timeout = self.timeout
        try:
            if self.wait(locator, timeout):
                e = self.get_first(locator)
                if e is not None:
                    self.driver.execute_script('arguments[0].click();', e)
                return True
            else:
                return False
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False
    

    def create_firefox(self, url='about:blank', maximize=False, minimize=False, headless=False):
        options = webdriver.firefox.options.Options()
        if headless: options.headless = True

        self.driver = webdriver.Firefox(options=options)
        self.driver.get('about:blank')
        if minimize: self.driver.minimize_window()
        if maximize: self.driver.maximize_window()
        self.driver.get(url)


    def delete_class(self, c):
        try:
            self.driver.execute_script('document.getElementsByClassName("{}")[0].remove();'.format(c))
        except: pass


    def enter_text(self, locator, *text):
        self.wait(locator)
        e = self.get_first(locator)
        e.send_keys(text)


    def exists(self, x):
        try:
            elems = self.driver.find_elements_by_xpath(x)
            if len(elems) == 0:
                if self.debug: print(f'Element {x} not found')
                return False
            else:
                if self.debug: print(f'Element {x} found!')
                return True
        except Exception as ex:
            if self.debug: traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False


    def find_elements_by_xpath(self, xpath) -> list:
        try:
            return self.driver.find_elements_by_xpath(xpath)
        except:
            return []


    def get_attribute(self, obj, xpath='.', attribute='value'):
        ''' if no xpath, returns the attribute for the object,
        otherwise looks up the first result of the xpath query and return its attribute'''
        if xpath == '.':
            try:
                return obj.get_attribute(attribute)
            except:
                return ''
        else:
            e = self.driver.get_first_element(obj, xpath)
            try:
                return e.get_attribute(attribute)
            except:
                return ''


    def get_all(self, locator):
        try:
            if self.exists(locator):
                return self.driver.find_elements_by_xpath(locator)
            else:
                return []
        except Exception as ex:
            return []


    def get_first(self, locator) -> WebElement:
        try:
            if self.exists(locator):
                return self.driver.find_elements_by_xpath(locator)[0]
        except Exception as ex:
            return None


    def go(self, url='about:blank'):
        self.driver.get(url)


    def get_text(self, xpath):
        e = self.get_first(xpath)
        try:
            t = ''
            t = e.text
        finally:
            return t
        

    def is_alive(self):
        am_alright = False
        try:
            for i in self.driver.find_elements_by_xpath('//*'):
                test = i
                break
            am_alright = True
        except Exception as fff:
            print(fff)
            am_alright = False
        finally:
            return am_alright


    def is_visible(self, xpath):
        '''Returns wheter the first found element for the specified xpath is visible or not'''
        well_is_it = False
        try:
            for i in self.driver.find_elements_by_xpath(xpath):
                if i.is_visible():
                    well_is_it = True
                else:
                    well_is_it = False
                break
        except:
            well_is_it = False
        finally:
            return well_is_it


    def quit(self):
        try    : self.driver.quit()
        except : pass


    def scroll_down(self, distance=None):
        '''if no distance (measured in pixels) is specified, will scroll down
           the entire length of the page.'''
        if distance is None:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
        else:
            self.driver.execute_script(f'window.scrollTo(0, {distance});') 


    def scroll_with_keypress(self, xpath, n=1, k=keys.END):
        e:WebElement = None
        try:
            if self.exists(xpath):
                e = self.driver.find_element_by_xpath(xpath)
                for i in range(n):
                    e.send_keys(k)

        except: pass


    def wait(self, xpath, timeout=None):
        if timeout is None: timeout = self.timeout
        maxwait = timeout * 2
        if maxwait <= 0: maxwait = 1
        for i in range(maxwait):
            try:
                e = self.driver.find_element_by_xpath(xpath)
                if e.is_displayed():
                    return True
            except: pass
            finally:
                time.sleep(0.5)
        print(f'Could not find element : {xpath}')
        return False


class _webelem(object):
    def __init__(self, element:WebElement) -> None:
        self.e = element
        self.error = None


    def click(self):
        try:
            self.e.click()
        except:
            try:
                self.driver.execute_script('arguments[0].click();', self.e)
            except:
                pass


    def get_attribute(self, attribute):
        try:
            return self.e.get_attribute(attribute)
        except Exception as ex:
            self.error = ex
            return ''


    def find_element_by_xpath(self, locator):
        try:
            return _webelem(self.e.find_element_by_xpath(locator))
        except Exception as ex:
            self.error = ex
            return None


    def get_innerHtml(self):
        return self.get_attribute('innerHTML')


    def get_outerHtml(self):
        return self.get_attribute('outerHTML')


    def get_text(self):
        self.error = None
        try:
            return self.e.text
        except Exception as ex:
            self.error = ex
            return ''
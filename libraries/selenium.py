import os, datetime, time, traceback
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys as keys
#from selenium.common.exceptions import StaleElementReferenceException


class _selenium(object):
    def __init__(self, driver=None, log=None):
        self.driver = driver
        self.timeout = 5

        if log is None:
            self.print = print
            self.debug = print
        else:
            self.print = log.print
            self.debug = log.debug


    def click(self, locator, timeout=None):
        self.debug(f'Clicking on {locator} with a timeout of {timeout}')
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
            self.debug(ex)
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
        self.debug(f'Deleting class {c}')
        try:
            self.driver.execute_script('document.getElementsByClassName("{}")[0].remove();'.format(c))
        except Exception as ex:
            self.debug(ex)


    def enter_text(self, locator, *text):
        self.wait(locator)
        e = self.get_first(locator)
        e.send_keys(text)


    def exists(self, x):
        try:
            elems = self.driver.find_elements_by_xpath(x)
            if len(elems) == 0:
                self.debug(f'Element {x} not found')
                self.debug(f'{x} does not exist')
                return False
            else:
                self.debug(f'Element {x} found!')
                self.debug(f'{x} exists')
                return True
        except Exception as ex:
            self.debug(f'{x} does not exist')
            self.debug(ex)
            return False


    def find_elements_by_xpath(self, xpath) -> list:
        self.debug(f'Looking for xpath {xpath}')
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
                x = self.driver.find_elements_by_xpath(locator)
                self.debug(f'found {len(x)} when looking for {locator}')
                return x
            else:
                self.debug(f'Found nothing when looking for {locator}')
                return []
        except Exception as ex:
            self.debug(f'error looking for {locator} : {ex}')
            return []


    def get_first(self, locator) -> WebElement:
        try:
            if self.exists(locator):
                x =  self.driver.find_elements_by_xpath(locator)[0]
                self.debug(f'found {len(x)} when looking for {locator}')
                return x
        except Exception as ex:
            self.debug(f'error looking for {locator} : {ex}')
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
            self.print(fff)
            am_alright = False
        finally:
            return am_alright


    def is_visible(self, xpath):
        '''Returns wheter the first found element for the specified xpath is visible or not'''
        self.debug(f'wondering if this is visible: {xpath}')
        well_is_it = False
        try:
            for i in self.driver.find_elements_by_xpath(xpath):
                if i.is_visible():
                    well_is_it = True
                else:
                    well_is_it = False
                break
        except Exception as ex:
            self.debug(f'An error occured trying to figure this out : {ex}')
            well_is_it = False
        finally:
            self.debug('It is visible: {xpath}')
            return well_is_it


    def quit(self):
        try    : self.driver.quit()
        except : pass


    def scroll_down(self, distance=None):
        self.debug('Scrolling down')
        '''if no distance (measured in pixels) is specified, will scroll down
           the entire length of the page.'''
        if distance is None:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
        else:
            self.driver.execute_script(f'window.scrollTo(0, {distance});') 


    def scroll_with_keypress(self, xpath, n=1, k=keys.END):
        self.debug('Scrolling down using key presses' )
        e:WebElement = None
        try:
            if self.exists(xpath):
                e = self.driver.find_element_by_xpath(xpath)
                for i in range(n):
                    e.send_keys(k)

        except: pass


    def wait(self, xpath, timeout=None):
        self.debug(f'waiting untils this is visible : {xpath}')
        if timeout is None: timeout = self.timeout
        maxwait = timeout * 2
        if maxwait <= 0: maxwait = 1
        for i in range(maxwait):
            try:
                e = self.driver.find_element_by_xpath(xpath)
                if e.is_displayed():
                    self.debug(f'Found {xpath}')
                    return True
            except: pass
            finally:
                time.sleep(0.5)
        self.print(f'Could not find element : {xpath}')
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
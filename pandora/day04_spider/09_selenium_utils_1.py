# coding=utf-8

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wwait
from selenium.webdriver.support import expected_conditions as EC


def wait_until(bc, locator, type=1):
    '''bc=driver,类似locator=(By.ID,'kw'),type{1:visible,2:clickable,3:frame switch}'''
    wait = wwait(bc, 10, 0.2)
    if type == 1:
        # 等待页面元素可见，返回该页面元素
        return wait.until(EC.visibility_of_element_located(locator))
    elif type == 2:
        # 等待页面元素可点击，返回该元素
        return wait.until(EC.element_to_be_clickable(locator))
    elif type == 3:
        # 通过定位frame 切换到这个frame
        return wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
    else:
        return None

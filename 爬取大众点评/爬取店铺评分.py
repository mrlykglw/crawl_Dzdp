
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
driver.maximize_window()
driver.get('https://www.dianping.com/shop/H58wRirFQyLQBnSI')
driver.implicitly_wait(5)
pingfen=driver.find_element(By.XPATH,'//div[@class="star-wrapper"]/div[2]')
pingfen=pingfen.text
print(pingfen)

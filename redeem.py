
# coding: utf-8

# In[26]:

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


# In[81]:

def page_waiter(driver, element, byEleType=By.NAME, msg=None):
    """
    byEleType: By.ID
    element: str element content
    """
    timeout = 20
    try:
        element_present = EC.presence_of_element_located((byEleType, element))
        WebDriverWait(driver, timeout).until(element_present)
        if msg:
            print msg
    except TimeoutException:
        print "Timed out waiting for page to load, NOT", msg

def driver_setup():
    # setup driver
    chromedriver = "./chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://www.mycokerewards.com/account/authenticate")

    # test load
    page_waiter(driver, "traditionalSignIn_emailAddress", msg="Ready to sign in...")
    return driver
        
def sign_in(driver, user_email, user_pwd):
    #sign in
    email = driver.find_element_by_name("traditionalSignIn_emailAddress")
    pwd = driver.find_element_by_name("traditionalSignIn_password")
    email.send_keys(user_email)
    pwd.send_keys(user_pwd)
    button = driver.find_element_by_name("traditionalSignIn_signInButton")\
    button.click()
    page_waiter(driver, "enterCodeField", msg="Ready to redeem...")
    
def redeem(driver, code, feedback, brand="regular"):

    # prepare feedback
    feedback={"redeem_error":None,
              "redeem_success":None,
              "current_point":None,
              "after_point":None}

    # enter code
    points = driver.find_element_by_xpath("//*[@id='h-profilePointAmount']/div")
    print "Current points {} with code {}...".format(points.text, code)
    feedback["current_point"] = points.text
    # code = "9x45mjm0l0n9hf"
    enter_code = driver.find_element_by_name("enterCodeField")
    enter_code.clear()
    enter_code.send_keys(code)
    enter_code.send_keys(Keys.RETURN)



    # fake click
    page_waiter(driver, "enterCodeErrorMessage", msg="Feedback collecting...")
    error = driver.find_element_by_class_name("enterCodeErrorMessage")
    if error.text:
        # error
        feedback["redeem_error"] = error.text
        print "Error!", error.text
        return False, feedback
    else:
        # correct code
        brand = driver.find_element_by_xpath("//*[@id='h-enterCode']/div[3]/div[2]/a[1]") # default: regular coke
        brand.click()
        page_waiter(driver, "enterCodeSuccessBox", msg="Redeem Succesfully! Totally points collecting...")
        success = driver.find_element_by_class_name("enterCodeSuccessBox")
        points = driver.find_element_by_xpath("//*[@id='h-profilePointAmount']/div")
        if success.text:
            feedback["redeem_success"] = success.text
            feedback["after_point"] = points.text
            print "Totally points", points.text
            return True, feedback
        else:
            raise ValueError("success.text None")

def driver_close(driver):
    driver.close()


# In[82]:

def driver_redeem(my_email, my_pwd, code):
    """
    Redeem on mycokerewards.com
    :param my_email: str
    :param my_pwd: str
    :param code: str
    :return: flag (bool), feedback (dict)
    """
    ### For TEST
    # my_email = ""
    # my_pwd = ""
    # code = "9x45mjm0l0n9hf"


    # set up a chrome driver
    driver = driver_setup()
    # sign in with email and pwd
    sign_in(driver, my_email, my_pwd)
    # redeem code online and return status and feedback
    flag, feedback = redeem(driver, code)
    # close the driver
    driver_close(driver)

    return flag, feedback


# In[83]:

# if __name__ == '__main__':
#     run()






import time

import Credentials
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from steem import Steem


website_next_counter = 1
user_steem_posting_key = Credentials.user_steemPostKey
user_name = Credentials.user_name
user_password = Credentials.user_password

steem = Steem(keys = user_steem_posting_key)

def get_my_following():
    followingCount = steem.get_follow_count(user_name)['following_count']
    return followingCount

Chrome = webdriver.Chrome()
Chrome.get("https://steemit.com/login.html")
assert "Login — Steemit" in Chrome.title
elem_username = Chrome.find_element_by_name("username")
elem_username.send_keys(user_name)
elem_password  = Chrome.find_element_by_name("password")
elem_password.send_keys(user_password)
elem_login = Chrome.find_element_by_class_name("button")
wait_ = WebDriverWait(Chrome, 3)
elem_login.click()
"""
Wait till the page load !!!

"""
wait_ = WebDriverWait(Chrome, 4)
time.sleep(5)
Chrome.get("https://steemit.com/@cheetah/followers")
assert "People following cheetah — Steemit" in Chrome.title

"""
Wait for the NEXT button to appear !!!

"""
wait_ = WebDriverWait(Chrome, 10)
time.sleep(8)
elem_next = Chrome.find_element_by_xpath("//*[@class='button tiny hollow float-right ']")
for i in range(website_next_counter):
    elem_next.click()
    wait_ = WebDriverWait(Chrome, 0.2)


def get_text_excluding_children(driver, element):
    return driver.execute_script("""
    return jQuery(arguments[0]).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    }).text();
    """, element)

before_following_count = get_my_following()
print(before_following_count)
f = open("Steemit_Followeing_List.txt", "w")
counter = 0
f.write("######Following######")

while counter <=1000:
    f.write("\n")
    f.write("Current Following Count: " + str(get_my_following()))
    elem_follow = Chrome.find_elements_by_xpath("//*[@class='button slim hollow secondary ']")
    print(get_my_following())
    i = 0
    for i in range(110):
            try:
                if elem_follow[i].text == "FOLLOW":
                    print(elem_follow[i].text)
                    elem_follow[i].click()
            except:
                print("Error")
            if i == 102:
                wait_ = WebDriverWait(Chrome, 4)
                time.sleep(6)
                elem2_next = Chrome.find_elements_by_xpath("//*[@class='button tiny hollow float-right ']")
                Chrome.execute_script("window.scroll(0,0)")
                elem_next.click()
                counter+=1

f.write("\nAmount of following BEFORE: "+ str(before_following_count))
f.write("\nAmount of following AFTER: " + str(get_my_following()))
f.write("\nYou got: " +  str(get_my_following()-before_following_count)+ " following")
f.write("\n"+str(website_next_counter+5)+ " times NEXT was pressed")
f.close()

print("Finished")
input("Enter any key to finish ...")

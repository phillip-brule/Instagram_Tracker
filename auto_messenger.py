from selenium import webdriver
from time import sleep
import yagmail


def sendEmail(recipient, subject, contents):
    try:
        yag = yagmail.SMTP(user='phillip.brule@gmail.com', password='Dovakin4~')
        yag.send(recipient, subject, contents)
    except:
        print("email did not send")

#to find xpath of element that you want to find use the developer tools, find the correct div, then right click and choose copy, then xpath
def run(username, pw, list_of_users, message):
    driver = webdriver.Chrome('D:\Phill\Documents\Instagram_App\chromedriver.exe')
    #recursive function. send path and count = how many times to try beofre giving up/ number of seconds allowed
    def clickXPath(xpath, count):
        if count < 1:
            raise ValueError("Instagram Path Error", xpath)
            return
        try:
            print(count)
            driver.find_element_by_xpath(xpath)\
                .click()
        except:
            sleep(1)
            clickXPath(xpath, count - 1)
        return

    def findUser(user):
        try:
            driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input')\
                .send_keys(user)
        except:
            raise ValueError("Instagram Path Error", '/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input')
        return

    def sendMessage(msg):
        try:
            driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')\
                    .send_keys(msg)
        except:
            raise ValueError("Instagram Path Error", '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        return        

    i = 0
    try:
        username = username
        driver.get('https://www.instagram.com/accounts/login/')
        sleep(1)
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        clickXPath('//button[@type="submit"]', 10)
        clickXPath('//*[@id="react-root"]/section/main/div/div/div/div/button', 10)
        clickXPath('/html/body/div[4]/div/div/div/div[3]/button[2]', 10)
        sleep(2)
        driver.get('https://www.instagram.com/direct/inbox/')

        users_not_messaged = []

        for user in list_of_users:
            clickXPath('//*[@id="react-root"]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button', 10)
            sleep(1)
            findUser(user)
            clickXPath('/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[3]/button/span', 10)
            sleep(1)
            clickXPath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button/div', 10)
            sleep(3)

            #getting user returned from searching for user
            x = driver.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/button/div/div[1]/div')
            found_user = x.text
            if found_user != user: 
                users_not_messaged.append(user)
            else:
                sendMessage(message)
                clickXPath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button', 10)
            i += 1
        
        sleep(10)
        return users_not_messaged
    except ValueError as ve:
        if ve.args[0] == "Instagram Path Error":
            contents = ["Hey future me, there was an instagram path error with the automatic follower tracker app.",
                        "The path was: ", ve.args[1], "Check it out and see what happend."]
            sendEmail("phillip.brule@gmail.com", "Instagram Auto Messenger Error", contents)
        return users_not_messaged.extend(list_of_users[i:])


#run("phillipbrule","Starwars4~", ["random"], "This is a test www.google.com")
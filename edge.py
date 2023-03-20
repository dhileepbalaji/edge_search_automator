from random import randint
from sys import platform
from time import sleep
from urllib import request
from libs.selenium import webdriver
from libs.selenium.webdriver.common.keys import Keys
from libs.selenium.webdriver.edge.service import Service
from libs.selenium.webdriver.common.by import By
# import edge options
from libs.selenium.webdriver.edge.options import Options as EdgeOptions

# Random Words Generation API
randomUrl = "https://random-word-api.vercel.app/api?words=100"
random_term = request.urlopen(randomUrl).read()
random_term = random_term.decode("utf-8")
# covert string list to python list
random_term = eval(random_term)


# random_term = ['a', 'b', 'c', 'd']


def search_bot(count, edgeOptions):
    if platform == "darwin":
        edgeService = Service('./drivers/mac/msedgedriver')

    elif platform == "win32":
        edgeService = Service('/drivers/win/msedgedriver.exe')

    browser = webdriver.Edge(service=edgeService, options=edgeOptions)
    for i in range(count):
        browser.get(f'https://www.bing.com/search?q={random_term[i]}')
        browser.set_page_load_timeout(5000)
        # get the search box and send random keys, *** Ahh : MS changes the id ***
        """"
        search_box = browser.find_element(By.ID, 'sb_form_q')
        search_box.clear()
        # send the random word to search box
        search_box.send_keys(random_term[i] + " " + Keys.RETURN)
        """
        sleep(2)

        # back to home
        browser.back()
    # close the browser
    browser.quit()


def main(userprofiledir, userprofilename):
    number_of_search_mobile = 30
    number_of_search_desktop = 40
    # In case we need to change user agent per request, we can use this module below
    """
    from fake_useragent import UserAgent
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    """

    # Ref : whatismybrowser.com/guides/the-latest-user-agent/edge
    mobileUserAgent = "Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.57 Mobile Safari/537.36 EdgA/110.0.1587.66"
    desktopUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44"

    # Desktop Search Options class object
    edgeOptions = EdgeOptions()
    # add arguments to Options
    edgeOptions.add_argument(
        f"userAgent={desktopUserAgent}"
    )
    # Set the profile paths below
    edgeOptions.add_argument(f"--user-data-dir={userprofiledir}")
    edgeOptions.add_argument(f"--profile-directory={userprofilename}")
    # do the search
    search_bot(number_of_search_desktop, edgeOptions)

    # Mobile Search Options class object
    edgeMobileOptions = EdgeOptions()
    mobile_emulation = {
        "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
        "userAgent": f"{mobileUserAgent}"
    }
    edgeMobileOptions.add_experimental_option("mobileEmulation", mobile_emulation)
    # Set the profile paths below
    edgeMobileOptions.add_argument(f"--user-data-dir={userprofiledir}")
    edgeMobileOptions.add_argument(f"--profile-directory={userprofilename}")

    # do the search
    search_bot(number_of_search_mobile, edgeMobileOptions)


if __name__ == "__main__":
    # Set the profile paths below
    userProfileFolder = "./userdata"
    userProfiles = ["Default", "Profile 1"]
    for userprofile in userProfiles:
        main(userProfileFolder, userprofile)

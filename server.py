# Unofficial LLAMA 2 API by Sean Lewis
# Uses Playwright

import time
import flask

from playwright.sync_api import sync_playwright

APP = flask.Flask(__name__)
PLAY = sync_playwright().start()
BROWSER = PLAY.chromium.launch(
    executable_path= ('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
    args=["--disable-dev-shm-usage", "--disable-blink-features=AutomationControlled"],
    headless=False,
)
PAGE = BROWSER.new_page()

def get_input_box():
    """Getting the input box"""
    return PAGE.query_selector("input[type='text'][class*='flex-grow block w-full rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:leading-6']")

def is_loading_response() -> bool:
    """Seeing if the LLAMA 2 message is different, if not, we're not loading"""
    page_elements = PAGE.query_selector_all("article[class*='pb-24']")
    last_element = page_elements.pop()
    before = last_element.inner_text()
    time.sleep(1.75)
    after = last_element.inner_text()
    return before != after

def send_message(message):
    """Sending the message"""
    box = PAGE.query_selector("input[type='text'][class*='flex-grow block w-full rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:leading-6']")
    box.click()
    box.fill(message)
    box.press("Enter")

not_started_counter = 0
skipq = False
def is_not_started() -> bool:
    
    global not_started_counter
    not_started_counter += 1
    if not_started_counter > 25:
        not_started_counter = 0
        global skipq
        skipq = True
        return False
    
    page_elements = PAGE.query_selector_all("article[class*='pb-24']")
    page_elements = page_elements[0].query_selector_all("div")
    before_children_amount = len(page_elements)
    time.sleep(1.75)
    page_elements = PAGE.query_selector_all("article[class*='pb-24']")
    page_elements = page_elements[0].query_selector_all("div")
    after_children_amount = len(page_elements)

    if (before_children_amount != after_children_amount):
        last_element = page_elements.pop()
        if last_element.inner_text() != "":
            return True
        else:
            return False
        
    #It could be the case that the AI started so fast our code didn't catch it, 
    #so we'll actually check if it is loading response just in case
    if is_loading_response():
        return False

    return True

def get_last_message():
    """Getting the latest message"""

    while is_not_started():
        time.sleep(1.55)
        print("Waiting for bot to start...")
    global not_started_counter
    not_started_counter = 0
    global skipq
    if skipq:
        skipq = False
        print("Reponse timed out.")
        return "Response timed out."

    #print("Loading response...")
    while is_loading_response():
        time.sleep(1.75)
        print("Waiting for response...")
    #print("Response loaded")

    page_elements = PAGE.query_selector_all("article[class*='pb-24']")
    page_elements = page_elements[0].query_selector_all("div")
    last_element = page_elements.pop()
    prev_element = last_element

    #Sometimes last element is empty div
    if last_element.inner_text() == "":
        last_element = page_elements.pop()

    #Sometimes last element is the question
    if last_element.inner_text().find("?") != -1 and len(last_element.inner_text()) < 200:
        last_element = prev_element
        
    print("Response:", last_element.inner_text())
    return last_element.inner_text()
    
@APP.route("/chat", methods=["GET"])
def chat():
    if "llama2.ai" not in PAGE.url:
        PAGE.goto("https://www.llama2.ai/")
    time.sleep(2)
    
    PAGE.query_selector("input[type='text'][class*='flex-grow block w-full rounded-l-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-gray-600 sm:leading-6']").click()

    message = flask.request.args.get("q")
    print("Sending message: ", message)
    send_message(message)
    #print("Retrieving response...")
    response = get_last_message()

    print("Response: ", response)
    return response

def start_browser():
    global PAGE,BROWSER,PLAY
    PAGE = BROWSER.new_page()

    APP.run(host='127.0.0.1', port=5041, threaded=False)

if __name__ == "__main__":
    start_browser()

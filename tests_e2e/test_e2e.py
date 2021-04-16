import pytest, os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from threading import Thread
from todo_app.trello_api_calls import create_trello_board, delete_trello_board,\
    fetch_all_cards
from todo_app.app import create_app

@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override = True)
    result = create_trello_board()
    os.environ['TRELLO_BOARD_NAME'] = result["name"]
    test_board_id = result["id"]
    print('Name of created board', os.environ['TRELLO_BOARD_NAME'])
    application = create_app()

    thread = Thread(target=lambda : application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    result = delete_trello_board(test_board_id)
    print('Status code for delete request', result.status_code)


@pytest.fixture(scope='module')
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver
    # with webdriver.Firefox() as driver:
    #     yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

def test_create_card(driver, test_app):
    driver.get('http://localhost:5000/')
    input_title = driver.find_element_by_id("title")
    input_title.send_keys('Creating new card')
    input_category = driver.find_element_by_id("status")
    select = Select(input_category)
    select.select_by_visible_text('To Do')
    button_to_click = driver.find_element_by_id("Add new card")
    button_to_click.click()
    assert (driver.page_source.find("Creating new card")) 

def test_mark_card_complete(driver, test_app):
    driver.get('http://localhost:5000/')
    button_to_click = driver.find_element_by_id("To Do Button 1")
    button_to_click.click()
    one_done_card = fetch_all_cards("Done")
    assert len(one_done_card) == 1
    assert one_done_card[0].title == "Creating new card"    
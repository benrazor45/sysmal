from selenium import webdriver


def get_chrome_driver() :

    options = webdriver.ChromeOptions()

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'


    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument("start-maximized")
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    options.add_argument(f"--user-agent={user_agent}")


    driver = webdriver.Chrome(options=options)

    return driver


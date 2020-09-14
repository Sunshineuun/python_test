from selenium import webdriver


def create_chrome_web_driver():
    """
    用于创建新的selenium驱动器 \n
    :return: 一个驱动器
    """
    options = webdriver.ChromeOptions()
    # 避免被识别为selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 禁止加载图片，但是貌似有必要加载图片
    prefs = {"profile.managed_default_content_settings.images": 2}
    # options.add_experimental_option("prefs", prefs)
    # 驱动器地址
    executable_path = 'C:\\chromedriver.exe'
    # 驱动器日志地址
    service_log_path = 'D:\\Temp\\chrome\\chromedriver.log'

    return webdriver.Chrome(
        executable_path=executable_path,
        chrome_options=options,
        service_log_path=service_log_path)
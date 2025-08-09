import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class TestSmoke:
    def setup_method(self, method):
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
            return True
        except NoSuchElementException:
            return False

    # 1. Ir a la página de inicio y verificar elementos clave
    def test_homepage_content(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        assert self.is_element_present(By.XPATH, "//img[@alt='Teton Chamber of Commerce Logo']")
        assert self.driver.find_element(By.XPATH, "//div[@id='content']/header/div/div[2]/h1").text == "Teton Idaho"
        assert self.driver.title == "Teton Idaho CoC"

    # 2. Navegación completa y validaciones de elementos en la página de inicio
    def test_navigation_and_join_link(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        assert self.is_element_present(By.CSS_SELECTOR, "nav ul li")
        assert self.is_element_present(By.XPATH, "//div[@id='content']/main/section[5]/div/p")
        assert self.is_element_present(By.XPATH, "//div[@id='content']/main/section[5]/div[2]/p")
        assert self.is_element_present(By.LINK_TEXT, "Join Us!")
        self.driver.find_element(By.LINK_TEXT, "Join Us!").click()
        assert "join.html" in self.driver.current_url

    # 3. Validar vista de tarjeta y lista del directorio
    def test_directory_views(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        self.driver.set_window_size(1151, 1040)
        self.driver.find_element(By.CSS_SELECTOR, "a[href*='directory.html']").click()
        assert "directory.html" in self.driver.current_url

        self.driver.find_element(By.ID, "directory-grid").click()
        assert self.is_element_present(By.XPATH, "//div[@id='directory-data']/section[9]")

        self.driver.find_element(By.ID, "directory-list").click()
        assert self.is_element_present(By.XPATH, "//div[@id='directory-data']/section[9]/p")

    # 4. Formulario de Join Page
    def test_join_form(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/join.html")
        assert self.is_element_present(By.NAME, "fname")
        # Simular el paso al siguiente paso con datos falsos
        self.driver.get("http://127.0.0.1:5500/teton/1.6/join-step2.html?fname=aaaaaaa&lname=aaaaaaaaaa&bizname=aaaaaaaaaaaa&biztitle=aaaaaaaaaaaa&submit=Next+Step")
        assert self.is_element_present(By.NAME, "email")

    # 5. Formulario de Admin con error de login
    def test_admin_login_error(self):
        self.driver.get("http://127.0.0.1:5500/teton/1.6/admin.html")
        assert self.is_element_present(By.ID, "username")
        self.driver.find_element(By.ID, "username").send_keys("asd")
        self.driver.find_element(By.ID, "password").send_keys("asd")
        self.driver.find_element(By.XPATH, "//input[@value='Login']").click()
        assert self.driver.find_element(By.XPATH, "//div[@id='content']/main/section/form/div/span").text == "Invalid username and password."

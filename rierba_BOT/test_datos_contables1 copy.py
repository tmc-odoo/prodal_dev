#GOLDIFLON
#Ya e trabajado con programadores en conjunto pa hacer algo yo te eseñare la metodologi para que cuando trabajes conmigo o con otro lo hagas de esa forma



#Importacion de bibloteclas


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openpyxl import load_workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import StaleElementReferenceException

print("Leyendo Credenciales ")
#Credecialess
user_pass = "admin"
a = 0




def Autobot():

    #Inicializando el diriver
    s = Service("geckodriver")


#PON EL CHOME DIRME EN UNA CARPETA ASI DEJA EL SERVICES ASI PORQUE CON EL PATH YA ESO ES VIEJO Y TE LO DICE AL EJECUTARLO
    driver = webdriver.Firefox(service=s)

    driver.get('https://rierba.odoo.com/web#action=465&model=product.template&view_type=kanban&cids=1&menu_id=294')
                


    print("Driver leido con exito")



    #Agregar hoja de excel. 







    filesheet = './rierba.xlsx'
    wb = load_workbook(filesheet)
    hojas = wb.get_sheet_names()
    print(hojas)
    nombres = wb.get_sheet_by_name('Sheet4')
    wb.close()
    

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#login'.replace(' ', '.'))))\
    .send_keys(user_pass )

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#password'.replace(' ', '.'))))\
    .send_keys(user_pass)

    time.sleep(1)

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button.btn btn-primary btn-block'.replace(' ', '.'))))\
    .click()

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.btn-primary'.replace(' ', '.'))))\
    .click()        

    time.sleep(2)

    for i in range (44,90):
        cat, nombre, marca , ref = nombres[f'A{i}:D{i}'][0]
        print(cat.value, nombre.value, marca.value , ref.value)


        cat_name = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_825'.replace(' ', '.'))))
        cat_name.send_keys(nombre.value)


        child_name = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_831'.replace(' ', '.'))))
        child_name.click()
        child_name.clear()
        time.sleep(1)
        child_name.send_keys(cat.value)
        time.sleep(1)
        child_name.send_keys(Keys.ENTER)
        time.sleep(1)

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_832'.replace(' ', '.'))))\
        .send_keys(ref.value)

        time.sleep(1)

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_834'.replace(' ', '.'))))\
        .send_keys(marca.value)


        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.o_form_button_save'.replace(' ', '.'))))\
        .click()  

        time.sleep(1)
        
        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.o_form_button_create'.replace(' ', '.'))))\
        .click()          


Autobot()                        

    
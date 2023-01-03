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
a = "atrivia123"




def Autobot():

    #Inicializando el diriver
    s = Service("geckodriver")


#PON EL CHOME DIRME EN UNA CARPETA ASI DEJA EL SERVICES ASI PORQUE CON EL PATH YA ESO ES VIEJO Y TE LO DICE AL EJECUTARLO
    driver = webdriver.Firefox(service=s)

    driver.get('https://rierba-14-0-report-jorgebm-6372526.dev.odoo.com/web#action=466&model=product.product&view_type=list&cids=1&menu_id=294')
                


    print("Driver leido con exito")



    #Agregar hoja de excel.







    filesheet = './inventario_rierba12.xlsx'
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
    .send_keys(a)

    time.sleep(1)

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button.btn btn-primary btn-block'.replace(' ', '.'))))\
    .click()


    time.sleep(2)

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button.btn:nth-child(3)'.replace(' ', '.'))))\
    .click()

    for i in range (4048,5370):
        art, nom, nom2, part, fam = nombres[f'A{i}:E{i}'][0]
        print(art.value, nom.value, nom2.value, part.value, fam.value)


        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            '//*[@id="o_field_input_915"]'.replace(' ', '.'))))\
        .send_keys(nom.value)


        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_921'.replace(' ', '.'))))\
        .send_keys(art.value)

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_922'.replace(' ', '.'))))\
        .send_keys(nom2.value)


        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_927'.replace(' ', '.'))))\
        .send_keys(part.value)
        

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_926'.replace(' ', '.'))))\
        .send_keys(fam.value)
        

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.o_form_button_save'.replace(' ', '.'))))\
        .click()        
        
        time.sleep(2)

        WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".o_form_button_create".replace(' ', '.'))))\
        .click()        


Autobot()                        

        
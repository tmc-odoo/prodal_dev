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

    driver.get('https://autohaus.odoo.com/web#id=11&action=406&model=stock.inventory&view_type=form&cids=2&menu_id=246')
                


    print("Driver leido con exito")



    #Agregar hoja de excel.







    filesheet = './INVENTARIO.xlsx'
    wb = load_workbook(filesheet)
    hojas = wb.get_sheet_names()
    print(hojas)
    nombres = wb.get_sheet_by_name('Inventario')
    wb.close()
    

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#login'.replace(' ', '.'))))\
    .send_keys(user_pass )

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#password'.replace(' ', '.'))))\
    .send_keys(user_pass )


    time.sleep(1)


    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button.btn btn-primary btn-block'.replace(' ', '.'))))\
    .click()

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/button[2]'.replace(' ', '.'))))\
    .click()        
    
    for i in range (338,388):
        nom, cant = nombres[f'A{i}:B{i}'][0]
        print(nom.value, cant.value)


        ing = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.o_searchview_input'.replace(' ', '.'))))
        ing.click()
        ing.send_keys(nom.value)
        ing.send_keys(Keys.ENTER)

        time.sleep(1)

        cant_var1 = WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'td.o_data_cell:nth-child(8)'.replace(' ', '.'))))
        cant_var1.click()


        cant_var = WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'input.o_field_float'.replace(' ', '.',))))
        cant_var.click()
        cant_var.clear()
        cant_var.send_keys('1')
     

        time.sleep(1)   

        WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "button.btn-primary:nth-child(2)".replace(' ', '.'))))\
        .click()

        time.sleep(1)

        driver.refresh()
        
            
Autobot()                        

        
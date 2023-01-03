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

    driver.get('https://rierba.odoo.com/web#id=26&action=481&model=stock.inventory&view_type=form&cids=1&menu_id=294')
                


    print("Driver leido con exito")



    #Agregar hoja de excel.







    filesheet = './producto.xlsx'
    wb = load_workbook(filesheet)
    hojas = wb.get_sheet_names()
    print(hojas)
    nombres = wb.get_sheet_by_name('Sheet2')
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
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[1]/button[2]'.replace(' ', '.'))))\
    .click()    

    time.sleep(2)
    for i in range (352,2102):
        seq, art, nul = nombres[f'A{i}:c{i}'][0]
        print(seq.value, art.value,nul.value)

        time.sleep(1)

        variable = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.o_searchview_input'.replace(' ', '.'))))
        variable.click()
        variable.send_keys(art.value)
        variable.send_keys(Keys.ENTER)
        time.sleep(4)
        # variable1 = WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                     '.o_data_row'.replace(' ', '.'))))

        # variable1.click()
        # time.sleep(1)


        # variable2 = WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                     'input.o_field_float'.replace(' ', '.'))))
        # variable2.click()
        # time.sleep(1)
        # variable2.send_keys(nul.value)
        # time.sleep(1)

        # WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                     '        button.btn-primary:nth-child(2)'.replace(' ', '.'))))\
        # .click()


        # S = 1


        # S.send_keys(Keys.F5)
Autobot()                        

        
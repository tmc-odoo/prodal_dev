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

    driver.get('https://laulet-14-0-test-henca-6469692.dev.odoo.com/web#action=211&cids=1&menu_id=268&model=account.account&view_type=list')



    print("Driver leido con exito")



    #Agregar hoja de excel.







    filesheet = './palonga.xlsx'
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
    .send_keys(user_pass )


    time.sleep(2)


    
    # while a < 235:

    WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        'button.btn btn-primary btn-block'.replace(' ', '.'))))\
    .click()

    
    for i in range (72,126):
        cod, cuenta, tipo, perm, mon = nombres[f'A{i}:E{i}'][0]
        print(cod.value, cuenta.value, tipo.value, perm.value, mon.value)
        

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'button.btn btn-primary o_list_button_add'.replace(' ', '.'))))\
        .click()
 
        
        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            "//input[@name='code']".replace(' ', '.'))))\
        .send_keys(int(cod.value))
        time.sleep(2)
            



        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            "//input[@name='name']".replace(' ', '.'))))\
        .send_keys(cuenta.value)
        time.sleep(1)


        select = Select(driver.find_element(By.XPATH,"//select[@name='user_type_id']"))
        select.select_by_visible_text(tipo.value)
        tipo = tipo.value

        time.sleep(1)

        pvalue = str(perm.value)
        valor = "1"
        
        if tipo == 'Por cobrar':
            WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/div".replace(' ', '.'))))\
            .click()

        elif tipo == 'Por pagar':
            WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/div".replace(' ', '.'))))\
            .click()

        




    #aqui haras el codicion del checkbox
        # if pvalue == 'VERDADERO':
        #     WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.XPATH,
        #                                     "/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/div".replace(' ', '.'))))\
        #     .click()
        # elif  pvalue == valor:
        #     WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.XPATH,
        #                                     "/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/div".replace(' ', '.'))))\
        #     .click()        

        # moneda = WebDriverWait(driver, 5000)\
        #     .until(EC.element_to_be_clickable((By.XPATH,
        #                                     "/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[6]/div/div/input".replace(' ', '.'))))
        # moneda.click()

        # moneda.send_keys(mon.value)
        # time.sleep(1)
        # moneda.send_keys(Keys.ENTER)

            # time.sleep(2)
            # moneda.send_keys("DOP")
            # time.sleep(2)
            # moneda.send_keys(Keys.ENTER)


        # time.sleep(1)
        # driver.navigate().refersh()
        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.XPATH,
                                            "//button[normalize-space()='Guardar']".replace(' ', '.'))))\
        .click()
        
        # driver.refresh()





Autobot()

# driver.find_element("xpath", '//*[@id="login"]').send_keys('admin')
# driver.find_element("xpath",'//*[@id="password"]').send_keys('admin')

# driver.find_element("xpath", '/html/body/div/main/div/div/div/form/div[3]/button').click()
# time.sleep(3)
# driver.find_element("xpath", '/html/body/div[2]/div/div[1]/div[2]/div[1]/div/div/button[3]').click()

# for i in range (2,300):
#     cod, cuenta, tipo, perm, mon, comp = nombres[f'A{i}:F{i}'][0]
#     print(cod.value, cuenta.value, perm.value, mon.value, comp.value)

#     driver.find_element("xpath" , '/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/input').send_keys(int(cod.value))
#     time.sleep(1)
#     driver.find_element("xpath", '/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[3]/input').send_keys(cuenta.value)
#     time.sleep(1)
#     driver.find_element("css selector", '/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[4]/select').click(1)
#     time.sleep(1)
#     # driver.find_element("css selector", 'tr.o_data_row:nth-child(1) > td:nth-child(5) > div:nth-child(1)).click(True)
#     # time.sleep(1)
#     driver.find_element("css selector", '/html/body/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[6]/div/div/input').click(2)
#     time.sleep(1)
#     driver.find_element("xpath", '/html/body/div[2]/div/div[1]/div[2]/div[1]/div/div/button[1]').click()
#     time.sleep(1)

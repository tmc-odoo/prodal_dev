# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from openpyxl import load_workbook
# import time

# driver = webdriver.Firefox('/home/atrivia/Desktop/ok/webdriver')
# driver.get('https://grupob-14-0-print-account-move-danher-5930019.dev.odoo.com/web#action=220&cids=10&menu_id=287&model=account.account&view_type=list')
# #Agregar hoja de excel.

# filesheet = './argentra.xlsx'
# wb = load_workbook(filesheet)
# hojas = wb.get_sheet_names()
# print(hojas)
# nombres = wb.get_sheet_by_name('Gastos')
# wb.close()

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


# driver.close()


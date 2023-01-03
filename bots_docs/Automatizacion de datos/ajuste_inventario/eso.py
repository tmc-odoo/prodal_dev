        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'button.btn:nth-child(3)'.replace(' ', '.'))))\
        .click()


        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_930'.replace(' ', '.'))))\
        .send_keys(desc.value)


        select = Select(driver.find_element(By.CSS_SELECTOR,'#o_field_input_940'))
        select.select_by_visible_text(tipo.value)
        tipo = tipo.value
        time.sleep(1)

        moneda = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_943'.replace(' ', '.'))))
        moneda.click()
        moneda.send_keys(marc.value)
        time.sleep(1)
        moneda.send_keys(Keys.ENTER)

        submodel1 = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_945'.replace(' ', '.'))))
        submodel1.click()
        submodel1.send_keys(sub.value)
        time.sleep(1)
        submodel1.send_keys(Keys.ENTER)



        modelo = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_944'.replace(' ', '.'))))
        modelo.click()
        modelo.send_keys(mod.value)
        time.sleep(1)
        modelo.send_keys(Keys.ENTER)

        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_946'.replace(' ', '.'))))\
        .send_keys(col.value)


        ano1 = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_947'.replace(' ', '.'))))
        ano1.clear()
        ano1.send_keys(ano.value)


        selectn = Select(driver.find_element(By.CSS_SELECTOR,'#o_field_input_935'))
        selectn.select_by_visible_text(nuevo.value)
        time.sleep(1)

        chasis1 = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_936'.replace(' ', '.'))))
        chasis1.send_keys(chasis.value)
        chasis1.send_keys(Keys.ENTER)


        kmpre= "km"
            
        kmpre1 = WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_938'.replace(' ', '.'))))
        kmpre1.send_keys(kmpre)
        time.sleep(1)
        kmpre1.send_keys(Keys.ENTER)

        if km != ".":
            km1 = WebDriverWait(driver, 5000)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    '#o_field_input_937'.replace(' ', '.'))))
            km1.clear()
            km1.send_keys(km.value)
            time.sleep(1)  



        if placa != 'N/A':
            placa1 = WebDriverWait(driver, 5000)\
                .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                '#o_field_input_941'.replace(' ', '.'))))
            placa1.clear()
            placa1.send_keys(placa.value)


        trans1= "Automático"
        select_trans = Select(driver.find_element(By.CSS_SELECTOR,'#o_field_input_950'))
        select_trans.select_by_visible_text(trans1)
        time.sleep(1)

        gaso = "Gasolina"
        select_gaso = Select(driver.find_element(By.CSS_SELECTOR,'#o_field_input_951'))
        select_gaso.select_by_visible_text(gaso)
        time.sleep(1)

        estado = "Propio"
        select_est = Select(driver.find_element(By.CSS_SELECTOR,'#o_field_input_934'))
        select_est.select_by_visible_text(estado)
        time.sleep(1)

            




        WebDriverWait(driver, 5000)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'li.nav-item:nth-child(3)'.replace(' ', '.'))))\
        .click()


        var_coste = WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="o_field_input_983"]'.replace(' ', '.'))))
        var_coste.clear()
        time.sleep(1)
        var_coste.send_keys(coste.value)
        time.sleep(1)




        code1 = WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '#o_field_input_979'.replace(' ', '.'))))
        code1.clear()
        code1.send_keys(cod.value)
        time.sleep(1)

        var_precio = WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '#o_field_input_981'.replace(' ', '.'))))
        var_precio.click()  
        var_precio.clear()                          
        var_precio.send_keys(precio.value)
        time.sleep(1)

        WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        ".o_form_button_save".replace(' ', '.'))))\
        .click()

        time.sleep(1)

        WebDriverWait(driver, 5000)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "li.breadcrumb-item:nth-child(1)".replace(' ', '.'))))\
        .click()

        time.sleep(1)
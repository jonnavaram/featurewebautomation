import os
import time
import random
import logging
from behave import *
from log_msg import *
from details import *
from selenium import webdriver
# from pypdf import pdfReader
from PyPDF2 import PdfReader
from common import FindElement
from locators import Locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import requests
import PyPDF2
import pdfplumber

import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


wait = FindElement()
current_file_name = os.path.basename(__file__)
new_file_name = os.path.splitext(current_file_name)[0] + ".png"

def findelement(context, path):
    return WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable((By.XPATH, path)))

@when(u'show the OMS page and select direct sales tab')
def step_impl(context):
    try:
        time.sleep(1)
        oms_path = findelement(context, Locators.oms_menu_path)
        oms_path.click()
        time.sleep(1)
        direct_sales = context.driver.find_element(By.XPATH, Locators.oms_direct_sales_tab_xpath)
        direct_sales.click()
        logging.info("Selected direct sales tab")
        time.sleep(2)

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_oms_page.format(str(e)))
        context.driver.close()
        raise Exception from e


@when(u'User in Direct Sales tab')
def step_impl(context):
    try:
        time.sleep(2)
        sales = context.driver.find_element(By.XPATH, Locators.dsalestab_xpath).text
        logging.info("User is in sales tab")
        time.sleep(2)
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.userin_direct_sales.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'click on Add sale button')
def step_impl(context):
    try:
        time.sleep(3)
        add_sale = findelement(context, Locators.add_sale_xpath)
        add_sale.click()
        time.sleep(1)
        logging.info("Selected Add sale button")

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.clickon_addsale_button.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'click on the "{branch}" from the dropdown')
def step_impl(context,branch):
    try:
        time.sleep(5)
        branch_dropdown = context.driver.find_element(By.XPATH, '//*[@id="exampleModal"]/div/div[2]/form/div[1]/app-company-filter/div/div/div/app-custom-select/div/div[1]/div[1]/div')
        branch_dropdown.click()
        time.sleep(2)
        companies = context.driver.find_elements(By.XPATH, "//app-add-directsales/div/div/div[2]/form/div[1]/app-company-filter/div/div/div/app-custom-select/div/div[2]/div/div[2]/cdk-virtual-scroll-viewport/div[1]/div[@role='option']")
        logging.info(f"Number of companies found: {len(companies)}")
        for i in range(1, len(companies) + 1):
            company_xpath = "//app-add-directsales/div/div/div[2]/form/div[1]/app-company-filter/div/div/div/app-custom-select/div/div[2]/div/div[2]/cdk-virtual-scroll-viewport/div[1]/div[{}]".format(i)
            logging.info(f"Checking XPath: {company_xpath}")
            branch_element = WebDriverWait(context.driver, 10).until(EC.presence_of_element_located((By.XPATH, company_xpath)))
            branch_text = branch_element.text.strip()
            logging.info(f"Found Branch: {branch_text}")
            if branch_text == branch:
                branch_element.click()
                logging.info("Branch selected successfully")
                break
 
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.clickon_branch_dropdown.format(str(e)))
        context.driver.close()
        raise Exception from e


# random_vehicle_number = generate_random_vehicle_number()


@then(u'Enter the Name, Phone number')
def step_impl(context):
    obj = Details()

    branch_name, branch_mobile, vehicle_number = obj.branchdetails()
    try:
        time.sleep(1)
        add_name = context.driver.find_element(By.XPATH, Locators.add_name_xpath)
        add_name.send_keys(branch_name)
        time.sleep(2)
        add_phno = context.driver.find_element(By.XPATH, Locators.add_phno_xpath)
        add_phno.send_keys(branch_mobile)
        context.mobile_number = branch_mobile

        time.sleep(1)
        logging.info(f"Entered Name: {branch_name}")
        logging.info(f"Entered Phone Number: {branch_mobile}")
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.enter_name_phonenumber.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'Select the Payment method \'POD\', Aggregate type')
def step_impl(context):
    try:
        global random_aggregate_type
        time.sleep(1)
        # payment
        payment = context.driver.find_element(By.XPATH, Locators.payment_xpath)
        payment.click()
        time.sleep(1)
        payment_method = findelement(context, Locators.payment_method_xpath)
        payment_method.click()
        time.sleep(1)
        # aggregate
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(1)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[4]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            time.sleep(1)
            xpath = "//app-add-directsales/div/div/div[2]/form/div[4]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)


    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.Paymentmethod_POD_Aggregatetype.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'enter the quantity')
def step_impl(context):
    obj = Details()
    salesquantity = obj.salesquantity()
    try:
        time.sleep(1)
        # quantity
        quantity = context.driver.find_element(By.XPATH, Locators.quantity_in_ton_xpath)
        quantity.send_keys(salesquantity)
        time.sleep(0.3)
        logging.info(f"quantity is: {salesquantity}")
        context.salesquantity = salesquantity


    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.enter_quantity_inexecutive.format(str(e)))
        context.driver.close()
        raise Exception from e

    


@then(u'Enter Vehicle number click on save')
def step_impl(context):
    try:
        obj = Details()
        branch_name, branch_mobile, generated_vehicle_number= obj.branchdetails()
        time.sleep(2)
        vehicle_number = context.driver.find_element(By.XPATH, Locators.vehicle_xpath)
        # vehicle_number.send_keys(vehicle_number)
        vehicle_number.send_keys(generated_vehicle_number)
        time.sleep(1)
        save_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locators.add_vehicle_save)))
        save_button.click()
        time.sleep(1)
        logging.info("Save button clicked")
        success_msg = WebDriverWait(context.driver, 10).until(EC.visibility_of_element_located((By.XPATH, Locators.container2_xpath))).text
        assert success_msg == "Details are updated Successfully"
        logging.info(f"Pop up message is: {success_msg}")
        time.sleep(5)
        
        # clear button
        # time.sleep(5)
        clear_button = context.driver.find_element(By.XPATH, Locators.oms_clear_button)
        clear_button.click()
        logging.info("Clicked on clear button")
        time.sleep(2)

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.enter_vehiclenumber.format(str(e)))
        context.driver.close()
        raise Exception from e
    

@then(u'Verify the order is placed with above deatils')
def step_impl(context):
    try:
        time.sleep(3)
        global random_aggregate_type
        branch_mobile =  context.mobile_number
        context.driver.find_element(By.XPATH, Locators.searchbar).send_keys(branch_mobile)
        time.sleep(1)
        # Extract details from the order details section
        order_id = context.driver.find_element(By.XPATH, Locators.order_id_xpath).text
        context.order_id = order_id
        logging.info(f"order_id is {order_id}")
        # phone number
        order_phno = context.driver.find_element(By.XPATH, Locators.order_phno_xpath).text
        order_phone = order_phno[2:]
        context.order_phone = order_phone
        logging.info(f"order_phone is {order_phone}")
        # aggregate
        order_aggregate = context.driver.find_element(By.XPATH, Locators.order_aggregate_xpath).text
        context.order_aggregate_type = order_aggregate
        logging.info(f"order_aggregate_type is {order_aggregate}")
        # quantity
        order_quantity = context.driver.find_element(By.XPATH, Locators.order_quantity_xpath).text
        context.order_quantity_type = order_quantity
        logging.info(f"order_quantity_type is {order_quantity}")
        # verify the details
        assert order_phone == context.mobile_number, "Order phone number doesn't match"
        assert order_aggregate == random_aggregate_type, "Order aggregate type doesn't match"
        salesquantity = float(context.salesquantity)
        logging.info(f"sales quantity:{salesquantity}")
        try:
            quantity = float(salesquantity) * 23.5
            logging.info(f"sales quantity is : {salesquantity}")
            logging.info(f"Qunatity in cft is: {quantity} TON")
            order_quantity = str(order_quantity).replace("TON", "").strip()
            order_quantity = float(order_quantity)  # Convert to float after removing text
            logging.info(f"order_quantity after removing the ton is : {order_quantity}")
            logging.info(f"Comparing quantity {quantity} with order_quantity {order_quantity}")
            # assert quantity == order_quantity, "Order quantity type doesn't match"
            # assert round(quantity, 2) == round(order_quantity, 2), f"Order quantity mismatch: {quantity} != {order_quantity}"
            # logging.info("Order details verified successfully")
            # time.sleep(2)
            
        except:
            pass
            # assert salesquantity == order_quantity, "Order quantity type doesn't match1"
            # logging.info("Order details verified successfully1")
            # logging.error(f"Assertion failed: {str(e)}")
            # logging.info(f"Values at failure - Salesquantity: {salesquantity}, Order quantity: {order_quantity}")
            # raise  # Raise the error so you can fix the values instead of skipping it


    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e
    


@then(u'Open the DC and Verify the order details')
def download_dc_pdf(context):
    driver = context.driver
    try:
        order_id = context.order_id
        dc_link = context.driver.find_element(By.XPATH, Locators.dc_xpath)
        dc_link.click()
        time.sleep(10)
        # # code for chrome
        # # Get the user's home directory  
        # home_dir = os.path.expanduser('~')        
        # # Define a common subdirectory within the home directory    
        # pdf_dir = os.path.join(home_dir, 'common_pdfs')        
        # if not os.path.exists(pdf_dir):  # Create the directory if it doesn't exist
        #     os.makedirs(pdf_dir)
        # logging.info(f"pdf dir is : {pdf_dir}")
        # file_name = f"DC-{order_id}.pdf"
        # pdf_path = os.path.join(pdf_dir, file_name)
        # logging.info(f"Pdf path is: {pdf_path}")
        # time.sleep(7)
        # # Read and verify the PDF contents
        # reader = PdfReader(pdf_path)
        # page = reader.pages[0]
        # extracted_text = page.extract_text()
        # logging.info(f"extracted_text is: {extracted_text}")
        # time.sleep(5)

        # code for firefox
        # Switch to new tab if opened
        tabs = context.driver.window_handles
        if len(tabs) > 1:
            context.driver.switch_to.window(tabs[-1])

        # Get PDF URL
        pdf_url = context.driver.current_url
        logging.info(f"Attempting to download from: {pdf_url}")

        # Define download directory
        home_dir = os.path.expanduser("~")
        pdf_dir = os.path.join(home_dir, "common_pdfs")

        # Create directory if it doesn't exist
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Define the file name and full path
        file_name = f"DC-{order_id}.pdf"
        file_path = os.path.join(pdf_dir, file_name)

        # Download the PDF
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"PDF downloaded and saved to {file_path}")
        else:
            logging.error(f"Failed to download PDF. Status code: {response.status_code}")
            exit(1)  # Stop execution if download failed

        # Add a wait to ensure download is complete
        timeout = 30  # Max wait time in seconds
        elapsed_time = 0

        while not os.path.exists(file_path) and elapsed_time < timeout:
            time.sleep(2)
            elapsed_time += 2

        if not os.path.exists(file_path):
            logging.error("PDF file was not downloaded within the expected time.")
            exit(1)  # Stop execution if file is missing

        # Verify file size (Ensure it’s not empty)
        if os.path.getsize(file_path) == 0:
            logging.error("Downloaded file is empty. PDF might not have been downloaded correctly.")
            exit(1)  # Stop execution if file is empty

        # Verify PDF content before parsing
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                logging.error("Downloaded file is not a valid PDF.")
                exit(1)  # Stop execution if it's not a valid PDF
            else:
                logging.info("Valid PDF detected. Proceeding with extraction.")

        # Read and verify the PDF contents
        reader = PdfReader(file_path)
        page = reader.pages[0]
        extracted_text = page.extract_text()
        logging.info(f"Extracted text is: {extracted_text}")

        time.sleep(5)

        # Compare with expected order details
        order_id_number = f"DC-{order_id}"
        order_phone = context.order_phone
        order_aggregate = context.order_aggregate_type
        order_quantity = context.order_quantity_type
        # Verify order details in the extracted text
        assert order_id_number in extracted_text, f"Order ID {order_id_number} not found in the PDF"
        logging.info(f"Order ID {order_id} found in the PDF")
        assert order_phone in extracted_text, f"Order Phone {order_phone} not found in the PDF"
        logging.info(f"Mobile No.{order_phone} found in the PDF")
        assert order_aggregate in extracted_text, f"order aggregate {order_aggregate} not found in the PDF"
        logging.info(f"Aggregate Type {order_aggregate} found in the PDF")
        # Quantity
        # order_quantity = float(context.order_quantity_type)
        salesquantity = context.salesquantity
        salesquantity1 = float(salesquantity)
        try:
            assert salesquantity in extracted_text, f"order aggregate {salesquantity} not found in the PDF"
            logging.info(f"Total Quantity {salesquantity} found in the PDF") 

        except:
            result = salesquantity1 / 23.5
            result1 = f"{int(result)} TON"
            logging.info(f"Result of order_quantity / 23.5: {result1}")
            assert result1 in extracted_text, f"order aggregate {result1} not found in the PDF"
            logging.info(f"Total Quantity {result1} found in the PDF") 

        if len(tabs) > 1:
            context.driver.close()  # Close the PDF tab
            context.driver.switch_to.window(tabs[0])  # Switch back to the main tab
    

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.open_dc_andverify.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'Select the Payment method \'Credit\', Aggregate type')
def step_impl(context):
    try:
        global random_aggregate_type
        time.sleep(2)
        payment = findelement(context, Locators.payment_xpath)
        payment.click()
        time.sleep(1)
        payment_method1 = context.driver.find_element(By.XPATH, Locators.payment_method1_xpath)
        payment_method1.click()
        time.sleep(1)
        # aggregate
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(1)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[4]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        time.sleep(1)
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            xpath = "//app-add-directsales/div/div/div[2]/form/div[4]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)

 
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_payment_method_credit.format(str(e)))
        context.driver.close()
        raise Exception from e
    

# @then(u'Select the Payment method \'UPI\', Aggregate type and Quantity')
# def step_impl(context):
#     try:
#         time.sleep(2)
#         payment = findelement(context, Locators.payment_xpath)
#         payment.click()
#         time.sleep(2)
#         payment_method1 = findelement(context, Locators.payment_method2_xpath)
#         payment_method1.click()
#         time.sleep(2)
#         # aggregate
#         aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
#         aggregate_type_dropdown.click()
#         time.sleep(10)
#         num_options = len(context.driver.find_elements(By.XPATH, "//mat-option"))
#         # Generate a random index excluding the first element
#         random_index = random.randint(2, num_options)
#         time.sleep(2)
#         xpath = f"//mat-option[{random_index}]"
#         random_aggregate = context.driver.find_element(By.XPATH, xpath)
#         context.driver.execute_script("arguments[0].scrollIntoView();", random_aggregate)
#         context.driver.execute_script("arguments[0].click();", random_aggregate)
#         random_aggregate_type = random_aggregate.text
#         context.random_aggregate_type = random_aggregate_type
#         logging.info(f"Selected aggregate is: {random_aggregate_type}")
#         time.sleep(2)

#         # quantity
#         quantity_type_dropdown = findelement(context, Locators.quantity_xpath)
#         quantity_type_dropdown.click()
#         time.sleep(2)
#         quantity_options = len(context.driver.find_elements(By.XPATH, "//mat-option"))
#         random_index1 = random.randint(2, quantity_options)
#         xpath = f"//mat-option[{random_index1}]"
#         random_quantity = context.driver.find_element(By.XPATH,xpath)
#         context.driver.execute_script("arguments[0].scrollIntoView();", random_quantity)
#         context.driver.execute_script("arguments[0].click();", random_quantity)
#         random_quantity_type = random_quantity.text
#         context.random_quantity_type = random_quantity_type
#         logging.info(f"Selected quantity is: {random_quantity_type}")
#         time.sleep(2)
#     except Exception as e:
#         context.driver.save_screenshot(f"./{new_file_name}")
#         logging.error(Error.show_company_page.format(str(e)))
#         context.driver.close()
#         raise Exception from e

    
# @then(u'Pay the payment from the payment link')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then Pay the payment from the payment link')


# @then(u'Verify the Payment status is changes to Paid')
# def step_impl(context):
#     raise NotImplementedError(u'STEP: Then Verify the Payment status is changes to Paid')



@then(u'Enter Invalid Name and check error message')
def step_impl(context):
    obj = Details()

    invalid_vehicle_number, invalid_owner_name, invalid_phone_number = obj.invalid_vehicle_details()
    try:
        time.sleep(1)
        add_name = findelement(context, Locators.add_name_xpath)
        add_name.send_keys(invalid_owner_name)
        time.sleep(1)
        error_message = context.driver.find_element(By.XPATH, Locators.error_message_xpath).text
        time.sleep(1)

    except Exception as e:
        screenshot_name = "invalid_name_error.png"
        context.driver.save_screenshot(screenshot_name)
        logging.error(f"Error occurred while checking error message for invalid name: {e}")
        context.driver.close()
        raise
        

@then(u'Enter Invalid Phone number and check error message')
def step_impl(context):
    obj = Details()

    invalid_vehicle_number, invalid_owner_name, invalid_phone_number = obj.invalid_vehicle_details()
    try:
        time.sleep(1)
        enter_mobile1 = context.driver.find_element(By.XPATH, Locators.add_phno_xpath)
        enter_mobile1.send_keys(invalid_phone_number)
        time.sleep(1)
        logging.info(f"Entering invalid number is: {invalid_phone_number}")
        time.sleep(1)
        error_message1 = context.driver.find_element(By.XPATH, Locators.error_message1_xpath).text
        logging.info(f"Error message is {error_message1}")
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e
   
@then(u'Select the Pay mode as POD')
def step_impl(context):
    try:
        time.sleep(1)
        payment = findelement(context, Locators.payment_xpath)
        payment.click()
        time.sleep(1)
        payment_method = context.driver.find_element(By.XPATH, Locators.payment_method_xpath)
        payment_method.click()
        time.sleep(1)
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e

@then(u'Select the Aggregate type from the dropdown')
def step_impl(context):
    try:
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(3)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[4]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            xpath = "//app-add-directsales/div/div/div[2]/form/div[4]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e
    
@then(u'Enter the Invalid vehicle number and check error message')
def step_impl(context):
    obj = Details()

    invalid_vehicle_number, invalid_owner_name, invalid_phone_number = obj.invalid_vehicle_details()
    try:
        time.sleep(1)
        vehicle_number = context.driver.find_element(By.XPATH, Locators.vehicle_xpath)
        vehicle_number.send_keys(invalid_vehicle_number)
        time.sleep(1)
        logging.info(f"Entered invalid Vehicle Number: {invalid_vehicle_number}")
        error_message2 = context.driver.find_element(By.XPATH, Locators.error_message2_xpath).text
        logging.info(f"Error message is: {error_message2}")
        time.sleep(1)
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e 
    
@then(u'enter the invalid quantity')
def step_impl(context):
    try:
        time.sleep(1)
        # quantity
        quantity = context.driver.find_element(By.XPATH, Locators.quantity_in_ton_xpath)
        quantity.send_keys(2000)
        time.sleep(0.3)
        error_message3 = context.driver.find_element(By.XPATH, Locators.error_message3_xpath).text
        logging.info(f"Error message is: {error_message3}")
        

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'Verify if bill amount is displayed or not')
def step_impl(context):
    try:
        time.sleep(1)
        bill_amount = context.driver.find_element(By.XPATH, Locators.bill_amount_xpath)
        # Check if the bill amount element is displayed
        if bill_amount.is_displayed():
            logging.info("Bill amount is displayed.")
        else:
            logging.error("Bill amount is not displayed.")
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e 


@then(u'check if Submit button is clickable')
def step_impl(context):
    try:
        time.sleep(2)
        save = context.driver.find_element(By.XPATH, Locators.add_vehicle_save )
        close_button = context.driver.find_element(By.XPATH, Locators.add_vehicle_close)
        if save.is_enabled():
            try:
                WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(save))
                save.click()
                logging.info("Save button clicked.")
            except:
                logging.error("Save button is not clickable despite being enabled. Clicking the Close button.")
                close_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(close_button))
                close_button.click()
                logging.info("Close button clicked.")
                time.sleep(2)
        else:
            logging.info("Save button is not enabled. Clicking the Close button.")
            close_button = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable(close_button))
            close_button.click()
            logging.info("Close button clicked.")
            time.sleep(5)
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.if_enabled_show_error_else_show_success.format(str(e)))
        context.driver.close()
        raise Exception from e
    

@when(u'Verify that the bill amount should populate automatically.')
def step_impl(context):
    try:
        time.sleep(2)
        
        bill_amount = context.driver.find_element(By.XPATH, Locators.bill_amount_xpath)
        # Get the value of the bill amount field
        bill_amount_value = bill_amount.get_attribute('value')
        # Check if the bill amount field is  automatically pre-filled
        if bill_amount_value:
            logging.info(f"Bill amount is automatically populated: {bill_amount_value}")
        else:
            logging.error("Bill amount is not automatically populated.")
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e 
    
@then(u'Edit the bill amount and enter a random bill amount.')
def step_impl(context):
    try:
        time.sleep(1)
        # Locate the bill amount field
        bill_amount_field = context.driver.find_element(By.XPATH, Locators.bill_amount_xpath)  
        bill_amount_field.clear()
        # Generate a random bill amount
        random_bill_amount = round(random.uniform(100, 100000))  
        
        # Enter the random bill amount
        bill_amount_field.send_keys(str(random_bill_amount))
        logging.info(f"Entered random bill amount: {random_bill_amount}")
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e 







# partner
@then(u'Select the Payment method \'POD\', Aggregate type in partner')
def step_impl(context):
    try:
        global random_aggregate_type
        time.sleep(1)
        # payment
        payment = context.driver.find_element(By.XPATH, Locators.payment_xpath)
        payment.click()
        time.sleep(1)
        payment_method = findelement(context, Locators.payment_method_xpath)
        payment_method.click()
        time.sleep(1)
        # aggregate
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(1)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[6]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            xpath = "//app-add-directsales/div/div/div[2]/form/div[5]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)


    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.Paymentmethod_POD_Aggregatetype.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'enter the quantity in partner')
def step_impl(context):
    obj = Details()
    salesquantity = obj.salesquantity()
    try:
        # quantity
        quantity = context.driver.find_element(By.XPATH,"//input[@placeholder='Quantity (in TON)']")
        quantity.send_keys(salesquantity)
        time.sleep(0.3)
        logging.info(f"quantity is: {salesquantity}")
        context.salesquantity = salesquantity


    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.enter_quantity_inexecutive.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'Select the Payment method \'Credit\', Aggregate type in partner')
def step_impl(context):
    try:
        global random_aggregate_type

        time.sleep(2)
        payment = findelement(context, Locators.payment_xpath)
        payment.click()
        time.sleep(2)
        payment_method1 = context.driver.find_element(By.XPATH, Locators.payment_method1_xpath)
        payment_method1.click()
        time.sleep(1)
        # aggregate
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(1)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[6]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        time.sleep(1)
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            xpath = "//app-add-directsales/div/div/div[2]/form/div[5]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)

 
    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_payment_method_credit.format(str(e)))
        context.driver.close()
        raise Exception from e
# invalif for partner

@then(u'Select the Aggregate type from the dropdown in partner')
def step_impl(context):
    try:
        aggregate_type_dropdown = findelement(context, Locators.aggregate_xpath)
        aggregate_type_dropdown.click()
        time.sleep(1)
        options = context.driver.find_elements(By.XPATH, "(//div[@class='cdk-virtual-scroll-content-wrapper'])[6]//div")
        com_len = len(options)
        logging.info(f"length of aggregate is : {com_len}")
        if com_len > 0:
            random_index = str(random.randint(1 , com_len))
            xpath = "//app-add-directsales/div/div/div[2]/form/div[5]/app-custom-select/div/div[2]/div/div/cdk-virtual-scroll-viewport/div[1]/div[{}]"
            aggregate_xpath = xpath.format(random_index)
            logging.info(f"Random XPath selected: {aggregate_xpath}")
            aggregate_element = context.driver.find_element(By.XPATH,aggregate_xpath)
            random_aggregate_type = aggregate_element.text
            logging.info(f"Randomly selected branch: {random_aggregate_type}")
            aggregate_element.click()
            time.sleep(1)
        context.random_aggregate_type = random_aggregate_type
        logging.info(f"Selected aggregate is: {random_aggregate_type}")
        time.sleep(1)

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e

@then(u'enter the invalid quantity in partner')
def step_impl(context):
    try:
        # quantity
        quantity = context.driver.find_element(By.XPATH, Locators.quantity_in_ton_xpath)
        quantity.send_keys(2000)
        time.sleep(0.3)
        error_message4 = context.driver.find_element(By.XPATH, "//span[@class='ng-star-inserted']").text
        logging.info(f"Error message is: {error_message4}")
        

    except Exception as e:
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.show_company_page.format(str(e)))
        context.driver.close()
        raise Exception from e

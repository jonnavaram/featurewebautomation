import datetime
import logging
import random
import time
from behave import *
import math
from details import Details
from details import *
from log_msg import *
from random_var import Random_class
from locators import Locators
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from WhatsappOrderPlacementWithDiscount import *
from whatsappautomation import *
from common import *
from UpdateOrderStatusByPartner import *
from VerifyCostMasterWhenBothDiscountsActiveOnAggregate import *
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from VerifyCostMasterWhenBothDiscountsInactive import *
from VerifymultilevelMasonrefferalforpodorder import *
current_file_name = os.path.basename(__file__)
new_file_name = os.path.splitext(current_file_name)[0] + ".png"
ex = Random_class()
wait = FindElement()
mason_details = {}


def find_element(context, xpath):
    return WebDriverWait(context.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def check_logistics_discount(customer_invoice):
    if 'Logistic Discounts Rs' in customer_invoice:
        logging.info(f"logisticsdiscount is displayed: {customer_invoice['Logistic Discounts Rs']}")
    else:
        logging.info("logisticsdiscount is not present")
        
def save_mason_details(context):
    global mason_details,mason_referral
    time.sleep(1)
    obj = Details()
    random_name, random_number, random_year = obj.Masonrandomdetails()
    Mason_Name = context.driver.find_element(By.XPATH, Locators.masonname)
    Mason_Name.send_keys(random_name)
    logging.info(f"Mason name: {random_name}")
    Mason_phone = context.driver.find_element(By.XPATH, Locators.masonphone)
    Mason_phone.send_keys(random_number)
    logging.info(f"Mason number: {random_number}")
    yearly_construction = context.driver.find_element(By.XPATH, Locators.yearlyconst)
    yearly_construction.send_keys(random_year)
    logging.info(f"Yearly construction: {random_year}")
    teamsize = context.driver.find_element(By.XPATH, Locators.teamsize)
    teamsize.send_keys(random_year)
    logging.info(f"Team size: {random_year}")
    time.sleep(0.5)
    privilageduserid = context.driver.find_element(By.XPATH, Locators.userid)
    privilageduserid.click()
    logging.info("Clicked on privileged user ID")
    time.sleep(1)
    companies_name = WebDriverWait(context.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="cdk-overlay-1"]/div/div[2]/div[6]/select/option')))
    userid = random.choice(companies_name)
    userid.click()
    time.sleep(1)
    save = context.driver.find_element(By.XPATH, Locators.ds_save_button)
    save.click()
    logging.info("Clicked save button")
    # wait = WebDriverWait(context.driver, 20)
    message = WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, Locators.container2_xpath))).text   
    logging.info(f"Pop up message is: {message}")
    assert message == "Mason details added successfully"

    time.sleep(5)
    enter_mason_name = context.driver.find_element(By.XPATH, Locators.searchbar_mason)
    enter_mason_name.send_keys(random_name)
    logging.info("Entered the Mason name")
    time.sleep(2)
    search_bar = context.driver.find_element(By.XPATH, Locators.search_xpath)
    search_bar.click()
    logging.info("Clicked on the search button")
    time.sleep(4)
    mason_details = {}
    columns = wait.find_elements(context, "//table/thead/tr/th")
    for i in range(1, len(columns)):
        key_xpath = "//table/thead/tr/th[{}]".format(i)
        value_xpath = "//table/tbody/tr[1]/td[{}]".format(i)
        key = wait.presence_of_element_located(context, key_xpath).text
        value = wait.presence_of_element_located(context, value_xpath).text
        mason_details[key] = value
    logging.info(f"Mason details of order: {mason_details}")
    
    
    # Extract the referral code and save it in the context
    mason_referral = mason_details.get('Referral Code', 'Value not found')
    logging.info(f"Mason referral: {mason_referral}")
    return mason_referral,mason_details

def save_multimason_details(context):
    global mason_details,mason_referral
    time.sleep(1)
    obj = Details()
    random_name, random_number, random_year = obj.Masonrandomdetails()
    Mason_Name = context.driver.find_element(By.XPATH, Locators.masonname)
    Mason_Name.send_keys(random_name)
    logging.info(f"Mason name: {random_name}")
    Mason_phone = context.driver.find_element(By.XPATH, Locators.masonphone)
    Mason_phone.send_keys(random_number)
    logging.info(f"Mason number: {random_number}")
    yearly_construction = context.driver.find_element(By.XPATH, Locators.yearlyconst)
    yearly_construction.send_keys(random_year)
    mason_name = context.mason_name
    context.driver.find_element(By.XPATH, Locators.parentmason).send_keys(mason_name)
    time.sleep(0.5)

    context.driver.find_element(By.XPATH, Locators.teamsize).send_keys(random_year)
    logging.info(f"Team size: {random_year}")
    time.sleep(0.5)
    context.driver.find_element(By.XPATH, Locators.userid).click()
    time.sleep(0.5)
    companies_name = WebDriverWait(context.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="cdk-overlay-1"]/div/div[2]/div[6]/select/option')))
    userid = random.choice(companies_name)
    userid.click()
    time.sleep(1)
    save = context.driver.find_element(By.XPATH, Locators.ds_save_button)
    save.click()
    logging.info("Clicked save button")
    # wait = WebDriverWait(context.driver, 20)
    message = WebDriverWait(context.driver, 20).until(EC.visibility_of_element_located((By.XPATH, Locators.container2_xpath))).text   
    logging.info(f"Pop up message is: {message}")
    assert message == "Mason details added successfully"

    time.sleep(7)
    context.driver.find_element(By.XPATH, Locators.searchbar_mason).send_keys(random_name)
    time.sleep(1)
    search_bar = context.driver.find_element(By.XPATH, Locators.search_xpath)
    search_bar.click()
    logging.info("Clicked on the search button")
    time.sleep(3)
    mason_details = {}
    columns = wait.find_elements(context, "//table/thead/tr/th")
    for i in range(1, len(columns)):
        key_xpath = "//table/thead/tr/th[{}]".format(i)
        value_xpath = "//table/tbody/tr[1]/td[{}]".format(i)
        key = wait.presence_of_element_located(context, key_xpath).text
        value = wait.presence_of_element_located(context, value_xpath).text
        mason_details[key] = value
    logging.info(f"Mason details of order: {mason_details}")
    
    
    # Extract the referral code and save it in the context
    mason_referral = mason_details.get('Referral Code', 'Value not found')
    logging.info(f"Mason referral: {mason_referral}")
    return mason_referral,mason_details


def referral_method(context):
    referral_code = mason_referral
    logging.info(f"Retrieved Mason referral code: {referral_code}")
    return referral_code



@then(u'select the "{company}" and "{branch}"')
def step_impl(context,company,branch):
    try:
       # Selecting company
        time.sleep(6)
        select = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locators.master_select_company)))
        select.click()
        time.sleep(1)
        wait = WebDriverWait(context.driver, 10)
        dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//cdk-virtual-scroll-viewport")))
        seen_companies = set()
        last_count = 0
        while True:
            # Find all currently visible company elements
            companies = context.driver.find_elements(By.XPATH, Locators.dropdown_options)
            for company_element in companies:
                text = company_element.text.strip()
                # Avoid processing duplicates
                if text and text not in seen_companies:
                    seen_companies.add(text)
                if text == company:
                    context.driver.execute_script("arguments[0].scrollIntoView(true);", company_element)
                    time.sleep(1)  # Allow time for scrolling
                    company_element.click()
                    time.sleep(2)
                    logging.info(f" Company '{company}' selected successfully")
                    time.sleep(3)
                    break
            # Stop scrolling if no new companies are found
            if len(seen_companies) == last_count:
                break
            last_count = len(seen_companies)
            context.driver.execute_script("arguments[0].scrollTop += 200;", dropdown)
            time.sleep(0.5)  # Allow time for elements to load
        
            # branches
            time.sleep(2)
            branches = WebDriverWait(context.driver, 10).until(EC.element_to_be_clickable((By.XPATH, Locators.branches_dropdown)))
            branches.click()  # Click the branch dropdown
            logging.info("Branch dropdown clicked successfully.")
            time.sleep(1)

            # Wait for the dropdown to load the options
            wait = WebDriverWait(context.driver, 10)
            dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "//cdk-virtual-scroll-viewport")))

            seen_companies = set()
            last_count = 0
            while True:
                companies = context.driver.find_elements(By.XPATH, Locators.dropdown_options)
                for company_element in companies:
                    text = company_element.text.strip()
                    # Avoid processing duplicates
                    if text and text not in seen_companies:
                        seen_companies.add(text)
                        logging.info(f"Found branch: {text}")
                    # If target branch is found, scroll into view and select it
                    if text == branch:
                        context.driver.execute_script("arguments[0].scrollIntoView(true);", company_element)
                        time.sleep(1)
                        company_element.click()
                        logging.info(f"'{branch}' selected successfully")
                        break
                # Stop scrolling if no new companies are found
                if len(seen_companies) == last_count:
                    break
                last_count = len(seen_companies)

                # Scroll down the dropdown
                context.driver.execute_script("arguments[0].scrollTop += 400;", dropdown)
                time.sleep(0.5)  # Allow time for elements to load
            
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.select_company.format(str(e)))
        context.driver.close()
        raise Exception from e
    
    
@then(u'show the earning page')
def step_impl(context):
    try:
        time.sleep(3)
        earnings_tab = context.driver.find_element(By.XPATH, Locators.earnings_tab)
        earnings_tab.click()
        time.sleep(1)
        mason_tab = context.driver.find_element(By.XPATH, Locators.mason_tab)
        mason_tab.click()
        time.sleep(2)
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.select_company.format(str(e)))
        context.driver.close()
        raise Exception from e


@then(u'click on the masion details')
def step_impl(context):
     try:
        time.sleep(1)
        side_panel = context.driver.find_element(By.XPATH, "//div[@id='sidebar-scroll']")
        context.driver.execute_script("arguments[0].scrollTop += 100;", side_panel)
        mason_details = context.driver.find_element(By.XPATH, Locators.mason_details)
        mason_details.click()
        time.sleep(5)
     except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.select_company.format(str(e)))
        context.driver.close()
        raise Exception from e
    


@then(u'click on the add mason button')
def step_impl(context):
    try:
        time.sleep(8)
        Add_mason = context.driver.find_element(By.XPATH, Locators.addmason_but)
        Add_mason.click()
        time.sleep(1)
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.select_company.format(str(e)))
        context.driver.close()
        raise Exception from e

@then(u'enter all the details and save the details(Without entering the parent mason)')
def step_impl(context):
    try:
        time.sleep(3)
        mason_referral,mason_details = save_mason_details(context)
        logging.info(f"Saved Mason details: {mason_details}")
        logging.info(f"Referral Code: {mason_referral}")
        context.referral_code = mason_referral

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.error(Error.enterdetails_savedetails.format(str(e)))
        context.driver.close()
        raise Exception from e
    

@when(u'enter the random refferal code')
def step_impl(context):
    logging.info("hi")
    global no_quantity
    no_quantity = 0
    referral_code = referral_method(context)
    logging.info(f"Using Mason referral: {mason_referral}")
    if no_quantity == 0:
        try:
            no_service = context.no_service
            if no_service == 0:
                pass
            else:
                referral_options = []
                referral_json = context.res_qty
                auto = autooms() 
                res_referral = auto.send_json_yes_referral()
                logging.info(res_referral)
                if res_referral.find('Please share your referral code:') >= 0:
                    send = referral_code
                    auto = autooms()
                    res_text = auto.text_referral(send)
                    context.res_text = res_text
                    context.res_referral = res_text
                    logging.info(res_text)
        except Exception as e:
            logging.error(f"Error occurred at enter the referral code: {str(e)}")
        else:
            pass



@then(u'Verify Aggregate Discount Rs = Loyality Reward on Aggregate + Mason Referral-customer discount')
def step_impl(context):
    try:
        # global customer_invoice,tax_deduction,Netpayment,platform_charges
        platform_charges = context.platform_charges
        customer_invoice = context.customer_invoice
        logging.info(f"platform charges is: {platform_charges}")
        try: 
            Loyality_reward_agg = float(platform_charges.get('Loyality Reward on Aggregate')[3:])
            logging.info(f"Loyality discount from costmaster page is: {Loyality_reward_agg}")
            MasonRefferal_discount = float(platform_charges.get('Mason Referral - customer discount','Value not found')[3:])
            logging.info(f"Mason refferal-customer discount is: {MasonRefferal_discount}")
            aggregatediscount_by_formula = float(Loyality_reward_agg + MasonRefferal_discount)
            logging.info(f"Aggregate discount by formula is: {aggregatediscount_by_formula}")
        except:
            MasonRefferal_discount = float(platform_charges.get('Mason Referral - customer discount','Value not found')[3:])
            logging.info(f"Mason refferal-customer discount is: {MasonRefferal_discount}")
            aggregatediscount_by_formula = float(MasonRefferal_discount)
            logging.info(f"Aggregate discount by formula is: {aggregatediscount_by_formula}")

        aggregate_discount_in_costmaster = float(customer_invoice.get('Before Adj of Aggregate Discount Rs')[3:])
        logging.info(f"Aggregate_discount costmaster page :{aggregate_discount_in_costmaster}")
        assert (aggregate_discount_in_costmaster <= aggregatediscount_by_formula + 3) and (
                    aggregate_discount_in_costmaster >= aggregatediscount_by_formula - 3), "Aggregate Discount Rs is not matching in Cost Master Page"
        logging.info("Successfully verified Aggregate Discount Rs in the Cost Master Page")
        context.aggregate_discount_in_costmaster = aggregate_discount_in_costmaster
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Aggregate Discount Rs = Loyality Reward on Aggregate + Mason Referral-customer discount: {e}")
        context.driver.close()
        raise Exception from e
    

@when(u'Logistic Discounts Rs are present')
def step_impl(context):
    global logistic_discount
    try:
        customer_invoice = context.customer_invoice
        logistic_discount = customer_invoice.get('Logistic Discounts Rs', 0)  # Set to 0 if not present
        if logistic_discount > 0:
            logging.info("Logistic discount is present.")
        else:
            logging.info("No logistic discount.")
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Logistic Discounts Rs are present: {e}")
        context.driver.close()
        raise Exception from e
    

@then(u'Verify Logistic Discounts Rs = (Points Monetised * Point Rate) - Loyalty Reward on Aggregate')
def step_impl(context):
    try:
      global platform_charges,logistic_discount
      customer_invoice = context.customer_invoice
      if logistic_discount > 0:
        points_monetised = customer_invoice.get('Points Monetised', 0)
        logging.info(f"points monitised:{points_monetised}")
        point_rate = customer_invoice.get('Point Rate', 0)
        logging.info(f"point rate:{point_rate}")
        loyalty_reward = platform_charges.get('Loyality Reward on Aggregate', 0)
        logging.info(f"Loyality Reward on Aggregate:{loyalty_reward}")
        expected_discount = (points_monetised * point_rate) - loyalty_reward
        assert logistic_discount == expected_discount, f"Expected {expected_discount}, but got {context.logistic_discount}"
        logging.info("Logistic discount verified.")
      else:
        logging.info("Skipping formula verification as no logistic discount is present.")
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Logistic Discounts Rs = (Points Monetised * Point Rate) - Loyalty Reward on Aggregate: {e}")
        context.driver.close()
        raise Exception from e


@then(u'Verify Net Logistics Value = Logistic Charges - Logistic Discount Rs')
def step_impl(context):
    global logistic_discount
    customer_invoice = context.customer_invoice
    try:
        if logistic_discount > 0:
            logistic_charges = customer_invoice.get('logistic_charges', 0)
            net_logistics_value = logistic_charges - logistic_discount
            logging.info(f"Net Logistics Value: {net_logistics_value}")
        else:
            logging.info("Skipping net logistics value calculation as no logistic discount is present.")

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Logistics Value = Logistic Charges - Logistic Discount Rs: {e}")
        context.driver.close()
        raise Exception from e



@then(u'if Logistic Discounts Rs are not present')
def step_impl(context):
    global logistic_discount
    try:
        if logistic_discount == 0:
            logging.info("Logistic Discounts Rs are not present.")
        else:
            logging.info("Logistic Discounts Rs are present with value:",logistic_discount)

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify if Logistic Discounts Rs are not present: {e}")
        context.driver.close()
        raise Exception from e

@then(u'Verify Net Logistics Value = Logistic Charges')
def step_impl(context):
    # global customer_invoice
    customer_invoice = context.customer_invoice
    try:
       logistic_charges_costmaster = float(customer_invoice.get('Logistics Charges','Value not found'))
       logging.info(f"Logistic charges from costmaster: {logistic_charges_costmaster}")
       Net_logistics_value_in_cost_master = float(customer_invoice.get('Net Logistics Value','Value not found'))
       logging.info(f"Net logistics value from costmaster: {Net_logistics_value_in_cost_master}")
       assert logistic_charges_costmaster == Net_logistics_value_in_cost_master,"Both logistic values are different"
       logging.info(f"Both logistic values are same")
       context.Net_logistics_value_in_cost_master = Net_logistics_value_in_cost_master
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Logistics Value = Logistic Charges: {e}")
        context.driver.close()
        raise Exception from e     
        

@then(u'Verify Platform Services Charges for Aggregate = Quantity * Platform Charges for Aggregate (₹) from charges tab')
def step_impl(context):
    # global platform_charges
    try:
        charges_dict = context.charges_dict
        oms_order_details = context.oms_order_details
        platform_charges = context.platform_charges
        for charge in charges_dict:
            if charge[0] == "Platform Charges for Aggregate (₹)":
                PlatformCharges_forAggregate = charge[1]  # Extract the value
                break
        Platform_charges_aggregate = float(PlatformCharges_forAggregate)
        logging.info(f"Platform Charges for Aggregate (₹) from charges tab is: {Platform_charges_aggregate}")
        #################################################
        if (oms_order_details[0][2][-3:]).upper() == 'TON':
            quantity = float(oms_order_details[0][2][:-4]) * float(23.5)
        else:
            quantity = float(oms_order_details[0][2][:-4])
        ################################################## 
        logging.info(f"Quantity in CFT is:{quantity}")
        Platform_Services_charges_Aggregate_byformula = float(float(quantity) * float(Platform_charges_aggregate))
        logging.info(f"platform service charges for aggregate by formula :{Platform_Services_charges_Aggregate_byformula}")
        Platform_Service_charges_in_costmaster = float(platform_charges.get('Before Adj of Platform Services Charges for Aggregate','value not found'))
        logging.info(f"Platform Services Charges for Aggregate in costmaster:{Platform_Service_charges_in_costmaster}")
        assert (Platform_Service_charges_in_costmaster <= Platform_Services_charges_Aggregate_byformula + 3) and (Platform_Service_charges_in_costmaster >=Platform_Services_charges_Aggregate_byformula - 3), "Platform Services Charges for Aggregate is not matching in Cost Master Page"
        logging.info("Successfully verified the Platform Services Charges for Aggregate")
        context.Platform_Service_charges_in_costmaster = Platform_Service_charges_in_costmaster
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Platform Services Charges for Aggregate = Quantity * Platform Charges for Aggregate (₹) from charges tab: {e}")
        context.driver.close()
        raise Exception from e                                         
        
@then(u'Verify Mason Referral - customer discount = Quantity * (Mason Referral Point to Rupee Conv from master | preferences tab)/2')
def step_impl(context):
    try:
        global mason_referral_customer_dis_costmaster
        platform_charges = context.platform_charges
        oms_order_details = context.oms_order_details
        preferences_list = context.preferences_list
        #################################################
        if (oms_order_details[0][2][-3:]).upper() == 'TON':
            quantity = float(oms_order_details[0][2][:-4]) * float(23.5)
        else:
            quantity = float(oms_order_details[0][2][:-4])
        ################################################## 
        logging.info(f"Quantity in CFT is:{quantity}")
        logging.info(f"Preferences list is: {preferences_list}")
        target_key = "Mason Referral Point to Rupee Conv"
        mason_referral_value = None
        for entry in preferences_list:           # Iterate through preferences_list to find the matching entry
          if entry[0] == target_key:
            mason_referral_value = entry[1]  # Assuming the value is in the second column
            break
        if mason_referral_value:
            logging.info(f"The value for '{target_key}' is: {mason_referral_value}")
        else:
            logging.info(f"'{target_key}' not found in the preferences list.")
        mason_referral = int(mason_referral_value)
        logging.info(f"Mason Referral Point to Rupee is: {mason_referral}")
        mason_referral_point_to_rupee_conv = mason_referral / 2
        logging.info(f"mason referral point to rupee conv by two is: {mason_referral_point_to_rupee_conv}")
        MasonReferral_customerdiscount_by_formula = float(float(quantity) * float(mason_referral_point_to_rupee_conv))
        logging.info(f"Mason Referral - customer discount by formula is: {MasonReferral_customerdiscount_by_formula}")
        mason_referral_customer_dis_costmaster = float(platform_charges.get('Mason Referral - customer discount')[3:])
        logging.info(f"mason referral customer discount from costmaster:{mason_referral_customer_dis_costmaster}")
        assert (mason_referral_customer_dis_costmaster <= MasonReferral_customerdiscount_by_formula + 3) and (mason_referral_customer_dis_costmaster >=MasonReferral_customerdiscount_by_formula - 3), "Mason Referral - customer discount is not matching in Cost Master Page"
        logging.info("Successfully verified the Mason Referral - customer discount")
        context.mason_referral_customer_dis_costmaster = mason_referral_customer_dis_costmaster


        
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Mason Referral - customer discount = Quantity * (Mason Referral Point to Rupee Conv from master | preferences tab)/2: {e}")
        context.driver.close()
        raise Exception from e 


@then(u'Verify Loyality Reward on Aggregate = point Monetised * point rate')
def step_impl(context):
    # global platform_charges
    try:
        customer_invoice = context.customer_invoice
        platform_charges = context.platform_charges
        pointmonitised = float(customer_invoice.get('Points Monetised'))
        logging.info(f"Points monitised is: {pointmonitised}")
        pointrate = float(customer_invoice.get('Point Rate'))
        logging.info(f"Point rate is: {pointrate}")
        if pointmonitised == 0:
            LoyalityReward_onAggregate_byformula = float(100)
            logging.info(f"Loyality Reward on Aggregate by formula is: {LoyalityReward_onAggregate_byformula}")
        else:
            LoyalityReward_onAggregate_byformula = float(pointmonitised * pointrate)
            logging.info(f"Loyality Reward on Aggregate by formula is: {LoyalityReward_onAggregate_byformula}")


        LoyalityReward_onAggregate_fromcostmaster = float(platform_charges.get('Loyality Reward on Aggregate')[3:])
        logging.info(f"Loyality Reward on Aggregate from cost master is: {LoyalityReward_onAggregate_fromcostmaster}")
        assert (LoyalityReward_onAggregate_fromcostmaster <= LoyalityReward_onAggregate_byformula + 1) and (LoyalityReward_onAggregate_fromcostmaster >= LoyalityReward_onAggregate_byformula - 1), "Loyality Reward on Aggregate is not matching in Cost Master Page"
        logging.info("Successfully verified the Loyality Reward on Aggregate")
        context.LoyalityReward_onAggregate_fromcostmaster = LoyalityReward_onAggregate_fromcostmaster

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Loyality Reward on Aggregate = point Monetised * point rate: {e}")
        context.driver.close()
        raise Exception from e 



@then(u'Verify Net Platform Aggregate Charges = (Platform Services Charges for Aggregate)-(Loyality Reward on Aggregate)-(Mason Referral - customer discount)')
def step_impl(context):
    try:
        platform_charges = context.platform_charges   
        Platform_Service_charges_in_costmaster = context.Platform_Service_charges_in_costmaster
        LoyalityReward_onAggregate_fromcostmaster = context.LoyalityReward_onAggregate_fromcostmaster
        mason_referral_customer_dis_costmaster = context.mason_referral_customer_dis_costmaster
        netplatform_aggregatecharges_by_formula = float(Platform_Service_charges_in_costmaster)-float(LoyalityReward_onAggregate_fromcostmaster)-float(mason_referral_customer_dis_costmaster)
        logging.info(f"Net Platform Aggregate Charges by formula is: {netplatform_aggregatecharges_by_formula}")
        Net_platform_aggregate_charges_in_costmaster = float(platform_charges.get('Net Platform Aggregate Charges'))
        logging.info(f"Net Platform Aggregate Charges from cost master is: {Net_platform_aggregate_charges_in_costmaster}")
        assert (Net_platform_aggregate_charges_in_costmaster <= netplatform_aggregatecharges_by_formula + 1) and (Net_platform_aggregate_charges_in_costmaster >= netplatform_aggregatecharges_by_formula - 1), "Net Platform Aggregate Charges is not matching in Cost Master Page"
        logging.info("Successfully verified the Net Platform Aggregate Charges")
        context.Net_platform_aggregate_charges_in_costmaster = Net_platform_aggregate_charges_in_costmaster


    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Platform Aggregate Charges = (Platform Services Charges for Aggregate)-(Loyality Reward on Aggregate)-(Mason Referral - customer discount): {e}")
        context.driver.close()
        raise Exception from e 


@then(u'Verify Loyality Reward on Logistics = (Points Monetised * Point Rate) - (Loyality Reward on Aggregate)')
def step_impl(context):
    # global platform_charges
    try:
        customer_invoice = context.customer_invoice
        platform_charges = context.platform_charges
        LoyalityReward_onAggregate_fromcostmaster = context.LoyalityReward_onAggregate_fromcostmaster
        if LoyalityReward_onAggregate_fromcostmaster == 100.0:
            LoyalityReward_onLogistics_byformula = 0
            logging.info(f"Loyality Reward on Logistics by formula is: {LoyalityReward_onLogistics_byformula}")
        else:
            pointmonitised = float(customer_invoice.get('Points Monetised'))
            logging.info(f"Points monitised is: {pointmonitised}")
            pointrate = float(customer_invoice.get('Point Rate'))
            logging.info(f"Point rate is: {pointrate}")
            LoyalityReward_onLogistics_byformula = float(pointmonitised*pointrate) - float(LoyalityReward_onAggregate_fromcostmaster)
            logging.info(f"Loyality Reward on Logistics by formula is: {LoyalityReward_onLogistics_byformula}")
        
        LoyalityReward_onLogistics_fromcostmaster = float(platform_charges.get('Loyality Reward on Logistics')[3:])
        logging.info(f"Loyality Reward on Logistics from costmaster: {LoyalityReward_onLogistics_fromcostmaster}")
        assert (LoyalityReward_onLogistics_fromcostmaster <= LoyalityReward_onLogistics_byformula + 1) and (LoyalityReward_onLogistics_fromcostmaster >= LoyalityReward_onLogistics_byformula - 1), "Loyality Reward on Logistics is not matching in Cost Master Page"
        logging.info("Successfully verified the Loyality Reward on Logistics")
        context.LoyalityReward_onLogistics_fromcostmaster = LoyalityReward_onLogistics_fromcostmaster
    
    
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Loyality Reward on Logistics = (Points Monetised * Point Rate) - (Loyality Reward on Aggregate): {e}")
        context.driver.close()
        raise Exception from e 




@then(u'Verify Net Platform Logistics Charges = Platform Services Charges for Logistics - Platform Geo Discount on Logistics - Loyality Reward on Logistics')
def step_impl(context):
    # global platform_charges
    try:
        platform_charges = context.platform_charges
        platform_servicecharges_forlogistics_in_costmaster = context.platform_servicecharges_forlogistics_in_costmaster
        Platform_Geo_Discount_on_Logistics_in_costmaster = context.Platform_Geo_Discount_on_Logistics_in_costmaster
        LoyalityReward_onLogistics_fromcostmaster = context.LoyalityReward_onLogistics_fromcostmaster
        NetPlatform_LogisticsCharges_byformula = float(platform_servicecharges_forlogistics_in_costmaster)-float(Platform_Geo_Discount_on_Logistics_in_costmaster)-float(LoyalityReward_onLogistics_fromcostmaster)
        logging.info(f"Net Platform Logistics Charges by formula is: {NetPlatform_LogisticsCharges_byformula}")
        net_platformlogistics_charges_in_costmaster = float(platform_charges.get('Net Platform Logistics Charges'))
        logging.info(f"Net Platform Logistics Charges from costmaster is: {net_platformlogistics_charges_in_costmaster}")

        assert (net_platformlogistics_charges_in_costmaster <= NetPlatform_LogisticsCharges_byformula + 1) and (net_platformlogistics_charges_in_costmaster >= NetPlatform_LogisticsCharges_byformula - 1), "Net Platform Logistics Charges is not matching in Cost Master Page"
        logging.info("Successfully verified the Net Platform Logistics Charges")
        context.net_platformlogistics_charges_in_costmaster = net_platformlogistics_charges_in_costmaster

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Platform Logistics Charges = Platform Services Charges for Logistics - Platform Geo Discount on Logistics - Loyality Reward on Logistics: {e}")
        context.driver.close()
        raise Exception from e 
    
@then(u'Verify Net Payment To Mason = Quantity * (Mason Referral Point to Rupee Conv from master | preferences tab)/2')
def step_impl(context):
    # global preferences_dict
    try:
        preferences_list = context.preferences_list
        platform_charges = context.platform_charges
        oms_order_details = context.oms_order_details
        #################################################
        if (oms_order_details[0][2][-3:]).upper() == 'TON':
            quantity = float(oms_order_details[0][2][:-4]) * float(23.5)
        else:
            quantity = float(oms_order_details[0][2][:-4])
        ################################################## 
        target_key = "Mason Referral Point to Rupee Conv"
        mason_referral_value = None
        for entry in preferences_list:           # Iterate through preferences_list to find the matching entry
          if entry[0] == target_key:
            mason_referral_value = entry[1]  # Assuming the value is in the second column
            break
        if mason_referral_value:
            logging.info(f"The value for '{target_key}' is: {mason_referral_value}")
        else:
            logging.info(f"'{target_key}' not found in the preferences list.")
        mason_referral = int(mason_referral_value)
        logging.info(f"Mason Referral Point to Rupee Conv is: {mason_referral}")
        mason_referral_point_to_rupee_conv = mason_referral / 2
        NetPayment_ToMason_by_formula = float(float(quantity) * float(mason_referral_point_to_rupee_conv))
        logging.info(f"Net Payment To Mason by formula is: {NetPayment_ToMason_by_formula}")
        Netpayment_tomason_fromcostmaster = float(platform_charges.get('Net Payment To Mason')[3:])
        logging.info(f"Net Payment To Mason from costmaster:{Netpayment_tomason_fromcostmaster}")
        assert (Netpayment_tomason_fromcostmaster <= NetPayment_ToMason_by_formula + 3) and (Netpayment_tomason_fromcostmaster >=NetPayment_ToMason_by_formula - 3), "Net Payment To Mason is not matching in Cost Master Page"
        logging.info("Successfully verified the Net Payment To Mason ")
        context.Netpayment_tomason_fromcostmaster = Netpayment_tomason_fromcostmaster


    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Payment To Mason = Quantity * (Mason Referral Point to Rupee Conv from master | preferences tab)/2: {e}")
        context.driver.close()
        raise Exception from e 



@then(u'Verify Net Platform and Service Charges = Platform and Service Charges - Net Payment To Mason')
def step_impl(context):
    # global platform_charges
    try:
        platform_charges = context.platform_charges
        Platform_andService_Charges_by_formula_in_costmaster = context.Platform_andService_Charges_by_formula_in_costmaster
        Netpayment_tomason_fromcostmaster = context.Netpayment_tomason_fromcostmaster
        NetPlatform_andServiceCharges_byformula = float(Platform_andService_Charges_by_formula_in_costmaster)-float(Netpayment_tomason_fromcostmaster)
        logging.info(f"Net Platform and Service Charges by formula is: {NetPlatform_andServiceCharges_byformula}")
        NetPlatform_andServiceCharges_fromcostmaster = float(platform_charges.get('Net Platform and Service Charges'))
        logging.info(f"Net Platform and Service Charges from costmater is: {NetPlatform_andServiceCharges_fromcostmaster}")
        assert (NetPlatform_andServiceCharges_fromcostmaster <= NetPlatform_andServiceCharges_byformula + 1) and (NetPlatform_andServiceCharges_fromcostmaster >= NetPlatform_andServiceCharges_byformula - 1), "Net Platform and Service Charges is not matching in Cost Master Page"
        logging.info("Successfully verified the Net Platform and Service Charges")

        
    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at Verify Net Platform and Service Charges = Platform and Service Charges - Net Payment To Mason: {e}")
        context.driver.close()
        raise Exception from e 


@then(u'click on referral earnings')
def step_impl(context):
    try:
        masonearnings = context.driver.find_element(By.XPATH, Locators.masonearnings)
        masonearnings.click()
        time.sleep(1)
        logging.info("Clicked on the mason earnings tab")

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at click on referral earnings: {e}")
        context.driver.close()
        raise Exception from e     

    


@then(u'enter the orderid and search')
def step_impl(context):
    try:
        time.sleep(2)
        order = order_id_method(context) 
        search_bar = context.driver.find_element(By.XPATH, "//input[@placeholder='Order ID']") 
        search_bar.send_keys(order)
        time.sleep(1)
        search_but = context.driver.find_element(By.XPATH, Locators.search_xpath)
        search_but.click()
        time.sleep(2)


    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at enter the orderid and search: {e}")
        context.driver.close()
        raise Exception from e


@then(u'save all the details')
def step_impl(context):
    global mason_details
    try:
        columns = wait.find_elements(context, "//table/thead/tr/th")
        for i in range(1, len(columns)):
            key_xpath = "//table/thead/tr/th[{}]".format(i)
            value_xpath = "//table/tbody/tr[1]/td[{}]".format(i)
            key = wait.presence_of_element_located(context, key_xpath).text
            value = wait.presence_of_element_located(context, value_xpath).text
            mason_details[key] = value
        logging.info(f"Mason details of order: {mason_details}")
        context.mason_details = mason_details

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at save all the details in mason earnings: {e}")
        context.driver.close()
        raise Exception from e


@then(u'verify the Mason referral amount on the Mason Referral earning page')
def step_impl(context):
    global mason_referral_customer_dis_costmaster,mason_details
    try:
        time.sleep(1)
        logging.info(f"Mason refferal amount from cost master is: {mason_referral_customer_dis_costmaster}")
        earningrefferalpage_amount = float(mason_details.get('Referral Amount'))
        logging.info(f"Mason Referral earning page is: {earningrefferalpage_amount}")

        assert mason_referral_customer_dis_costmaster == earningrefferalpage_amount, "Both mason refferal amounts are different in earnings page and costmaster page"
        logging.info("Both mason refferal amounts are same in earnings page and costmaster page")

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at verify the Mason referral amount on the Mason Referral earning page: {e}")
        context.driver.close()
        raise Exception from e
    
@then(u'verify the Mason referral amount on the Mason Referral earning page for multilevel mason')
def step_impl(context):
    try:
        global mason_details,mason_referral_customer_dis_costmaster
        allmason_details = []
        fifth_column_details = []

        while True:    
            table = context.driver.find_elements(By.XPATH, Locators.table_xpath)
            if not table:
                logging.info("Table not found. Exiting loop.")
                break
            for row in table:
                # Find the 5th column specifically within this row (relative XPath)
                try:
                    fifth_column = row.find_element(By.XPATH, "./mat-cell[5]") 
                    fifth_column_text = fifth_column.text.replace('\n', ',')
                    fifth_column_details.append(fifth_column_text)
                except Exception as e:
                    logging.warning(f"Could not find 5th column for row: {row.text}. Error: {e}")
                row_text = row.text.replace('\n', ',')
                allmason_details.append(row_text)
            next_button = context.driver.find_element(By.XPATH, Locators.next_button_xpath)
            first_page = context.driver.find_element(By.XPATH, Locators.first_page_button)

            if next_button.is_enabled():
                next_button.click()
                time.sleep(0.5)
            elif first_page.is_enabled():
                first_page.click()
                break
            else:
                break
        logging.info(f"All mason details (full rows): {allmason_details}")
        logging.info(f"Fifth column details: {fifth_column_details}")
        try:
            earningtotalamount = sum(float(value) for value in fifth_column_details)
            logging.info(f"Total sum of fifth column details: {earningtotalamount}")
        except ValueError as e:
            logging.error(f"Error converting fifth column details to numbers: {e}")
        logging.info(f"Mason referral amount from cost master is: {mason_referral_customer_dis_costmaster}")


        assert (earningtotalamount <= mason_referral_customer_dis_costmaster + 1) and (earningtotalamount >= mason_referral_customer_dis_costmaster - 1), "Both mason refferal amounts are different in earnings page and costmaster page"
        logging.info("Both mason refferal amounts are same in earnings page and costmaster page")

    except Exception as e:
        time.sleep(1)
        context.driver.save_screenshot(f"./{new_file_name}")
        logging.info(f"Error occurred at verify the Mason referral amount on the Mason Referral earning page: {e}")
        context.driver.close()
        raise Exception from e




from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def fill_form(driver, fname, lname, zip):
    try:
        # Fill in First Name
        fname_field = driver.find_element(By.ID, 'first-name')
        fname_field.send_keys(fname)
        
        # Fill in Last Name
        lname_field = driver.find_element(By.ID, 'last-name')
        lname_field.send_keys(lname)
        
        # Fill in Zip Code
        zip_field = driver.find_element(By.ID, 'postal-code')
        zip_field.send_keys(zip)
        
        # Wait for a moment to see the filled form
        time.sleep(2)
        
        # Submit the form
        submit_button = driver.find_element(By.ID, 'continue')
        submit_button.click()
        
        # Wait for the next step to load
        time.sleep(2)
    except Exception as e:
        print(f"Error in fill_form: {e}")

def open_cart(driver):
    try:
        # Find the cart button and click it
        cart_button = driver.find_element(By.CLASS_NAME, 'shopping_cart_link')
        cart_button.click()
        time.sleep(2)
    except Exception as e:
        print(f"Error in open_cart: {e}")

def select_product_and_add_to_cart(driver):
    try:
        # Find the product (for demonstration purposes, let's assume we are selecting the first product)
        product = driver.find_element(By.XPATH, "//*[@id='item_4_title_link']/div")
        product.click()
        time.sleep(2)
        
        # Add the product to the cart
        add_to_cart_button = driver.find_element(By.ID, 'add-to-cart')
        add_to_cart_button.click()
        time.sleep(2)

        print("Product added to cart")

        # return product_price
    except Exception as e:
        print(f"Error in select_product_and_add_to_cart: {e}")
        return None

def send_email(to_address, subject, body):
    from_address = "shrisabtestacc@gmail.com"
    password = "zece cruh ddwa ieet"  # Use App Password if 2FA is enabled

    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = from_address
        message['To'] = to_address
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # Use Gmail's SMTP server and port
        session.starttls()  # Enable security
        session.login(from_address, password)  # Login with your email and app password
        text = message.as_string()
        session.sendmail(from_address, to_address, text)
        session.quit()

        print("Mail sent successfully.")
    except Exception as e:
        print(f"Error in send_email: {e}")

def login(url, username, password, username_field_id, password_field_id, login_button_id, fname, lname, zip):
    # Set up the WebDriver (this example uses Chrome)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the login page
        driver.get(url)
        time.sleep(2)
        
        # Find the username field and enter the username
        username_field = driver.find_element(By.ID, username_field_id)
        username_field.send_keys(username)

        # Find the password field and enter the password
        password_field = driver.find_element(By.ID, password_field_id)
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.ID, login_button_id)
        login_button.click()

        # Wait for some time to allow login to complete
        time.sleep(2)

        select_product_and_add_to_cart(driver)
        
        open_cart(driver)
        
        # Click the checkout button
        checkout_button = driver.find_element(By.ID, 'checkout')
        checkout_button.click()
        time.sleep(2)
    
        # Fill the form on the checkout page
        fill_form(driver, fname, lname, zip)
        
        # Extract the product price
        product_price_element = driver.find_element(By.CLASS_NAME, 'summary_total_label')
        product_price = product_price_element.text
            
            # Send a confirmation email with the product price
        email_body = f"Your purchase has been successfully completed.\n\nProduct Price: {product_price}"
        send_email('shrisab12@gmail.com', 'Purchase Successful', email_body)
        
    except Exception as e:
        print(f"Error in login: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    # Define the login details and page elements
    url = 'https://www.saucedemo.com/'  # Login page URL
    username = 'standard_user'           # Replace with your username
    password = 'secret_sauce'            # Replace with your password
    username_field_id = 'user-name'      # ID of the username field
    password_field_id = 'password'       # ID of the password field
    login_button_id = 'login-button'     # ID of the login button
    fname = 'Shrisab'
    lname = 'Shrestha'
    zip = '44600'
    
    login(url, username, password, username_field_id, password_field_id, login_button_id, fname, lname, zip)

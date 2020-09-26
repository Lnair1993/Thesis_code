import argparse, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui

parser = argparse.ArgumentParser(description='Downloading and processing data from the SCiO sensor.')
#parser.add_argument('-u', '--username', help='Username', required=True)
#parser.add_argument('-p', '--password', help='Password', required=True)
parser.add_argument('-u', '--username', help='Username', required=False)
parser.add_argument('-p', '--password', help='Password', required=False)
parser.add_argument('-c', '--collection_name', help='Collection Name', required=False) # Need to figure this out
args = parser.parse_args()

driver = webdriver.Chrome('/home/lnair3/Nimbus_ws/src/nimbus_explore/src/chromedriver')
wait = ui.WebDriverWait(driver, 10)

# SCiO RAIL sign in 
scio_username = ''
scio_password = ''

# Login to SCiO Lab
driver.get('https://sciolab.consumerphysics.com/#/login')
driver.switch_to.frame(driver.find_element_by_id('login-iframe'))

username = driver.find_element_by_id('username')
wait.until(lambda driver: driver.find_element_by_id('username').is_displayed())
if args.username is not None:
    username.send_keys(args.username)
else:
    username.send_keys(scio_username)

password = driver.find_element_by_id('password')
if args.password is not None:
    password.send_keys(args.password)
else:
    password.send_keys(scio_password)

password.send_keys(Keys.ENTER)

# Wait for SCiO webpage to load
wait.until(lambda driver: driver.find_element_by_id('collection-name-0').is_displayed())

# Get the collection id
time.sleep(0.5)

if args.collection_name is not None:
    collection_id = driver.find_element_by_xpath("//*[contains(text(), '%s')]" % args.collection_name).find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('col_id')
    # driver.find_element_by_xpath("//*[contains(text(), 'Lakshmi')]").find_element_by_xpath('..').click()
else:
    collection_id = '00d5e78b-6f15-492b-94e2-22ed79302069'

# Open up specific collection
# driver.get('https://sciolab.consumerphysics.com/#/collections/f596a03f-5c67-47a9-83f3-51a7e2b6fc54/samples')
driver.get('https://sciolab.consumerphysics.com/#/collections/%s/samples' % collection_id)

# Get rid of "New features" dialog if it pops up
wait.until(lambda driver: (driver.find_element_by_id('confirm-modal-close').is_displayed() and driver.find_element_by_id('confirm-modal-close').is_enabled()) or driver.find_element_by_css_selector('header.title.clearfix').find_element_by_css_selector('button.app.btn-ok.action.pull-right.ng-binding.ng-scope').is_displayed())
time.sleep(0.5)
if driver.find_element_by_id('confirm-modal-close').is_displayed() and driver.find_element_by_id('confirm-modal-close').is_enabled():
    driver.find_element_by_id('confirm-modal-close').click()

# Open the download data dialog
time.sleep(0.5)
header = driver.find_element_by_css_selector('header.title.clearfix')
header.find_element_by_css_selector('button.app.btn-ok.action.pull-right.ng-binding.ng-scope').click()

# Click on the download button
popup = driver.find_element_by_css_selector('div.popup-content.download-collection-panel.ng-scope')
popup.find_element_by_css_selector('button.btn.app.btn-ok.ng-binding').click()

# driver.quit()
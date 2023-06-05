from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver
from utilities.allure_methods import *
from time import sleep

logger = get_logger(logger_name=__name__)
config_file = read_config_file(section='auth')


@given(u'that I want to view the specials on the specials page')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Navigating to the specials page")


@when(u'I login to the e-commerce')
def step_impl(context):
    context.execute_steps("When I login in to the e-commerce")


@when(u'I navigate to the page')
def step_impl(context):
    AmplifyEcommerce(context.driver).navigate_to_specials()


@then(u'I should be able to see the page')
def step_impl(context):
    AmplifyEcommerce(context.driver).screenshot(message="The specials page")


@then(u'the url should be of format "https://host/specials"')
def step_impl(context):
    current_url = AmplifyEcommerce(context.driver).specials_url()
    
    assert_with_allure(
        condition="specials" in current_url,
        message="URL should contain specials",
        data=f"Current:{current_url}"
    )
    
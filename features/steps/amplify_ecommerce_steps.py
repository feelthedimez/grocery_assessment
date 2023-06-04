from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver
from utilities.allure_methods import *

logger = get_logger(logger_name=__name__)
config_file = read_config_file(section='auth')


@given(u'that I want to search for an invalid (nonexistant) category')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Searching for a non-existant category")


@when(u'I navigate to the app, and search that category {category}')
def step_impl(context, category):


    AmplifyEcommerce(context.driver).login(
        username=config_file['username'], 
        password= config_file['password']
    )

    AmplifyEcommerce(context.driver).search_category(category=category)


@then(u'I should get no products displayed')
def step_impl(context):
    
    all_products = AmplifyEcommerce(context.driver).all_products_from_screen()

    assert_with_allure(
        condition=len(all_products) == 0,
        message="There should not be any products displayed",
        data=f"All products: {all_products}",
    )


@given(u'that I want to search for a valid (existant) category')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Searching for an existant category")


@when(u'I navigate to the app, and seach for the category as the step above {category}')
def step_impl(context, category):
    context.execute_steps(f'When I navigate to the app, and search that category {category}')


@then(u'I should get all necessary products for category {category_products}')
def step_impl(context, category_products: str):
    categories = category_products.split(',')
    feature_categories = [item.strip() for item in categories]
    all_products_from_web = AmplifyEcommerce(context.driver).all_products_from_screen()

    assert_with_allure(
        condition=sorted(feature_categories) == sorted(all_products_from_web),
        message="Check if the two lists contain the same products",
        data=f"\nWeb: {all_products_from_web} \nFeature: {feature_categories}"
    )


@given(u'that I want to add {items} of {product} to the cart')
def step_impl(context, items, product):
    context.driver = initialize_driver()
    log_to_allure(message=f"Adding {items} items of {product} to cart")


@when(u'I login in to the e-commerce')
def step_impl(context):
    AmplifyEcommerce(context.driver).login(
        username=config_file['username'], 
        password= config_file['password']
    )


@when(u'I add {items} of {product} and I click add to cart')
def step_impl(context, items, product):
    AmplifyEcommerce(context.driver).add_product_to_cart(product, items)


@then(u'I should see "You have just added {items} of {product} to cart" message')
def step_impl(context, items, product):
    message = f"You have just added {items} of {product} to cart"
    message_from_web = AmplifyEcommerce(context.driver).alert_message()

    assert_with_allure(
        condition=message == message_from_web,
        message="Validate if the add to cart messages alerts are the same",
        data=f"Feature: {message}. \nWebApp: {message_from_web}"
    )
from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver
from utilities.allure_methods import *
from time import sleep

logger = get_logger(logger_name=__name__)
config_file = read_config_file(section='auth')


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
    AmplifyEcommerce(context.driver).add_product_to_cart(
        product_name=product, 
        items_to_add=items,
        add_to_cart=True
        )


@then(u'I should see "You have just added {items} of {product} to cart" message')
def step_impl(context, items, product):
    message = f"You have just added {items} of {product} to cart"
    message_from_web = AmplifyEcommerce(context.driver).alert_message()

    assert_with_allure(
        condition=message == message_from_web,
        message="Validate if the add to cart messages alerts are the same",
        data=f"Feature: {message}. \nWebApp: {message_from_web}"
    )


@given(u'that I want to add the exceeded number of products in cart')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Adding an exceed amount of products to cart")


@when(u'I login in to the e-commerce like the previous step')
def step_impl(context):
    context.execute_steps("When I login in to the e-commerce")


@when(u'I exceed the number {items} of {product}')
def step_impl(context, items, product):
    AmplifyEcommerce(context.driver).add_product_to_cart(product, items, add_to_cart=False)


@then(u'I should have a button become disabled for product {product}')
def step_impl(context, product):
    
    add_cart_btn = AmplifyEcommerce(context.driver).is_button_active(product)
    
    assert_with_allure(
        condition=add_cart_btn==False,
        message="The add cart button should not be clickable",
        data=f"Is button clicable: {add_cart_btn}"
    )


@given(u'that I want to increase the items of a product in the product screen')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Increasing and decreasing items to zero")


@when(u'I login as the other steps')
def step_impl(context):
    context.execute_steps("When I login in to the e-commerce")


@then(u'I add the product {product} with {items} items')
def step_impl(context, product, items):
    AmplifyEcommerce(context.driver).add_product_to_cart(product_name=product, items_to_add=items, add_to_cart=False)


@then(u'I decrease them to zero by the same {items} items amount for {product}')
def step_impl(context, items, product):
    AmplifyEcommerce(context.driver).decrement_products(product, items)


@then(u'I should see zero on the amount of items to add for {product}')
def step_impl(context, product):
    current_value = AmplifyEcommerce(context.driver).get_current_item_value(product_name=product)

    assert_with_allure(
        condition=current_value==0,
        message="The value of the items for that product is supposed to be zero",
        data=f"Current value: {current_value}"
    )


@given(u'that I want to input the number of items for a product')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Inputting the value of the product items")


@when(u'I login as previous steps as above, then input item {items} for product {product}')
def step_impl(context, items, product):
    context.execute_steps("When I login in to the e-commerce")
    AmplifyEcommerce(context.driver).input_item_value(product_name=product, items_to_add=items)


@when(u'I re-edit back to 0 items for product {product}')
def step_impl(context, product):
    context.product = product
    AmplifyEcommerce(context.driver).input_item_value(product_name=product, items_to_add=0)


@then(u'the button should not be clikable')
def step_impl(context):

    add_cart_btn = AmplifyEcommerce(context.driver).is_button_active(context.product)
    
    assert_with_allure(
        condition=add_cart_btn==False,
        message="The add cart button should not be clickable",
        data=f"Is button clicable: {add_cart_btn}"
    )


@given(u'that I want to input a character instead of a number')
def step_impl(context):
    context.driver = initialize_driver()
    log_to_allure(message="Inputting a letter in the product item number")


@when(u'I login as previous steps and then input the letter {letter} for product {}')
def step_impl(context, product, letter):
    context.execute_steps("When I login in to the e-commerce")
    context.product = product
    AmplifyEcommerce(context.driver).input_item_value(product_name=product, items_to_add=letter)


@then(u'the button should not be clickable as the above step')
def step_impl(context):
    context.execute_steps("Then the button should not be clikable")

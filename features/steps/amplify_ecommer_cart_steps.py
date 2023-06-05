from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver
from utilities.allure_methods import *
from time import sleep

logger = get_logger(logger_name=__name__)
config_file = read_config_file(section='auth')


@given(u'that I want to add {items} items of product {product}')
def step_impl(context, items, product):
    context.driver = initialize_driver()
    log_to_allure(message="Navigating to the specials page")


@when(u'I add {items} items of product {product}')
def step_impl(context, product, items):
    context.items = int(items)
    AmplifyEcommerce(context.driver).add_product_to_cart(product_name=product, items_to_add=items, add_to_cart=True)


@then(u'I should get the same amount of items on the cart counter')
def step_impl(context):
    cart_items = AmplifyEcommerce(context.driver).extract_items_number_cart()

    assert_with_allure(
        condition=cart_items==context.items,
        message="The number of items added to the cart should match the icon amout",
        data=f"Cart: {cart_items}. Items added: {cart_items}"
    )


@given(u'that I want to add a list of items')
def step_impl(context):
    log_to_allure("Adding multiple items to the cart")
    context.driver = initialize_driver()


@when(u'I add list; {item_list} of products; {product_list}')
def step_impl(context, item_list, product_list):
    values = item_list.split(",")
    product_names = product_list.split(',')

    items = [int(value.strip()) for value in values]
    products = [item.strip() for item in product_names]

    context.items = items
    context.products = products

    cost = []

    for i in range(len(items)):
        AmplifyEcommerce(context.driver).add_product_to_cart(
            product_name=products[i],
            items_to_add=items[i],
            add_to_cart=True
        )

        cost.append(AmplifyEcommerce(context.driver).extract_cost_from_item(
            product_name=products[i],
        ))

    context.cost = cost


@then(u'I check the amount of items added to cart')
def step_impl(context):

    total_items_added = sum(context.items)

    cart_items = AmplifyEcommerce(context.driver).extract_items_number_cart()

    assert_with_allure(
        condition=cart_items==total_items_added,
        message="The number of items added to the cart should match the icon amout",
        data=f"Cart: {cart_items}. Items added: {cart_items}"
    )


@then(u'then I navigate to cart and check the total balance')
def step_impl(context):
    
    monetary_values = []

    for price in context.cost:
        monetary_value = float(price.split('R')[1])
        monetary_values.append(monetary_value)
    
    result = [x * y for x, y in zip(monetary_values, context.items)]

    AmplifyEcommerce(context.driver).navigate_to_cart()
    
    sum_cost = sum(result)
    total = AmplifyEcommerce(context.driver).total_cost_cart()

    assert_with_allure(
        condition=sum_cost==total,
        message="The total acutal cost should be equal to the cost on the e-commerce",
        data=f"Total cost items: {sum_cost}. Total cost from website: {total}"
    )


@given(u'that I want to add a product to cart')
def step_impl(context):
    log_to_allure("Adding products to cart and the removing them")
    context.driver = initialize_driver()


@when(u'I add {items} items of the product {product} and add to cart')
def step_impl(context, items, product):
    context.items = int(items)
    AmplifyEcommerce(context.driver).add_product_to_cart(product_name=product, items_to_add=items, add_to_cart=True)


@then(u'I add an extra item while at cart')
def step_impl(context):
    AmplifyEcommerce(context.driver).navigate_to_cart()
    AmplifyEcommerce(context.driver).increment_cart()

@then(u'I check the total')
def step_impl(context):
    context.total = AmplifyEcommerce(context.driver).total_cost_cart()


@then(u'total should be the number of added items amount')
def step_impl(context):
    
    assert_with_allure(
        condition=context.total != 0 or context.total < 0,
        message="The total should not be zero at all",
        data=f"The total is: {context.total}"
    )
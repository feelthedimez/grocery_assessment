from behave import *
from utilities.project_logger import get_logger
from utilities.read_properties import read_config_file
from services.web.amplify_ecommerce_service import AmplifyEcommerce
from utilities.chrome_driver_init import initialize_driver
from utilities.allure_methods import *
from time import sleep

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
        message="The url should contain `specials`: 'https://host/specials'",
        data=f"The current url: {current_url}"
    )
    

@given(u'that I want to add 5 items of product Keloggs Cornflakes')
def step_impl(context):
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
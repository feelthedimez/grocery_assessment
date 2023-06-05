Feature: The e-commerce cart feature

    Scenario Outline: Validate the counter on the cart
        Given that I want to add <items> items of product <product>
        When I login to the e-commerce
        And I add <items> items of product <product>
        Then I should get the same amount of items on the cart counter

        Examples:
            | items | product            |
            # | 5     | Keloggs Cornflakes |


    Scenario Outline: Add items to cart and check the total
        Given that I want to add a list of items
        When I login to the e-commerce
        And I add list; <item_list> of products; <product_list>
        Then I check the amount of items added to cart
        And then I navigate to cart and check the total balance

        Examples:
            | item_list | product_list |
            # | 5, 4, 5   | Keloggs All Bran, Grapes, Apples |

    Scenario Outline: Add <items> items of <product> to cart and then removing them from cart
        Given that I want to add a product to cart
        When I login to the e-commerce
        When I add <items> items of the product <product> and add to cart
        Then I add an extra item while at cart
        And I check the total
        Then total should be the number of added items amount

        Examples:
            | items | product            |
            | 1     | Keloggs Cornflakes |

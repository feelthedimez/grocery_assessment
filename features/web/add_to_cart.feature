Feature: The add to cart functionality

    Scenario Outline: Adding <items> of <product> to cart
        Given that I want to add <items> of <product> to the cart
        When I login in to the e-commerce
        And I add <items> of <product> and I click add to cart
        Then I should see "You have just added <items> of <product> to cart" message

        Examples:
            | items | product            |
            # | 5     | Keloggs Cornflakes |
            # | 6     | Jungle Oats        |
            # | 1     | Oranges            |

    Scenario Outline: Adding <items> of <product> to cart
        Given that I want to add the exceeded number of products in cart
        When I login in to the e-commerce like the previous step
        And I exceed the number <items> of <product>
        Then I should have a button become disabled

        Examples:
            | items | product            |
            | 50    | Keloggs Cornflakes |
            # | 60    | Jungle Oats        |
            # | 70    | Oranges            |
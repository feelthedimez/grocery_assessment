Feature: The add to cart functionality

    Scenario Outline: Adding <items> of <product> to cart
        Given that I want to add <items> of <product> to the cart
        When I login in to the e-commerce
        And I add <items> of <product> and I click add to cart
        Then I should see "You have just added <items> of <product> to cart" message

        Examples:
            | items | product            |
            | 5     | Keloggs Cornflakes |
            | 6     | Jungle Oats        |
            | 1     | Oranges            |

    Scenario Outline: Adding <items> of <product> to cart

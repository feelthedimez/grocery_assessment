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
        Given that I want to add the exceeded number of products in cart
        When I login in to the e-commerce like the previous step
        And I exceed the number <items> of <product>
        Then I should have a button become disabled for product <product>

        Examples:
            | items | product            |
            | 50    | Keloggs Cornflakes |
            | 60    | Jungle Oats        |
            | 70    | Oranges            |


    # Issue with this - For some reason, I can't seem to be able to click the decrement button :\ :|
    Scenario Outline: Adding <items> of the <product> and decrementing them
        Given that I want to increase the items of a product in the product screen
        When I login as the other steps
        Then I add the product <product> with <items> items
        And I decrease them to zero by the same <items> items amount for <product>
        Then I should see zero on the amount of items to add for <product>

        Examples:
            | items | product            |
            | 5     | Keloggs Cornflakes |
            | 3    | Jungle Oats        |

    
    Scenario Outline: Adding <items> of the <product> and editing the field after
        Given that I want to input the number of items for a product
        When I login as previous steps as above, then input item <items> for product <product>
        And I re-edit back to 0 items for product <product>
        Then the button should not be clikable

        Examples:
            | items | product            |
            | 5     | Keloggs Cornflakes |

    Scenario Outline: Adding a letter <letter> for product <product> using the input editor
        Given that I want to input a character instead of a number
        When I login as previous steps and then input the letter <letter> for product <product>
        Then the button should not be clickable as the above step

        Examples:
            | letter | product            |
            | e     | Keloggs Cornflakes |

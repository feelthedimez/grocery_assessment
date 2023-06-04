Feature: The Amplify app e-commerce search functionality

    Scenario Outline: Search for an invalid product category: <category>
        Given that I want to search for an invalid (nonexistant) category
        When I navigate to the app, and search that category <category>
        Then I should get no products displayed

        Examples:
            | category |
            # | Veggies  |


    Scenario Outline: Search for the valid product category: <category>
        Given that I want to search for a valid (existant) category
        When I navigate to the app, and seach for the category as the step above <category>
        Then I should get all necessary products for category <categoryProducts>

        Examples:
            | category | categoryProducts                                  |
            | cereal   | Keloggs Cornflakes, Keloggs All Bran, Jungle Oats |
            | Fruits   | Oranges, Grapes, Apples, Banana                   |
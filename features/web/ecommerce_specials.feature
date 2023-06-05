Feature: Viewing specials of products in the e-commerce

    Scenario: Visiting the specials page
        Given that I want to view the specials on the specials page
        When I login to the e-commerce
        And I navigate to the page
        Then I should be able to see the page
        And the url should be of format "https://host/specials"
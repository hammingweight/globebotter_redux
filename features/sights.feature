Feature: Rome

  Scenario: Test recommendation
    Given a session with the chatbot
    When a user asks the chatbot "I'm in Rome for one day. Please suggest three sights, in numbered bullet form that I should visit. Do not include any details about the sights."
    Then the response should be similar to "1. The Colosseum 2. Vatican City 3. Trevi Fountain"
    And the response should not be similar to
      | Bad Response                                           |
      | "1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe"     |
      | "1. Pane e Salame. 2. Tonnarello. 3. Cantina e Cucina" |
      | "All mimsy were the borogoves"                         |


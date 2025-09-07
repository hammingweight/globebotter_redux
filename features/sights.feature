Feature: Rome

  Scenario: Test Rome sights recommendation
    Given a session with the chatbot	    
    When a user asks the chatbot to recommend three sights in Rome
    Then the response should be similar to "1. The Colosseum 2. Vatican City 3. Trevi Fountain"
    And the response should be less similar to
      | 1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe     |
      | 1. Pane e Salame. 2. Tonnarello. 3. Cantina e Cucina |
      | All mimsy were the borogoves                         |


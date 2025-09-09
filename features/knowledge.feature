Feature: Chatbot knowledge

  @rome
  Scenario: Test tourist sights knowledge
    Given a session with the chatbot
    When a user asks the chatbot
    """
    I'm in Rome for one day. Suggest three sights, in numbered bullet form, that I should visit.
    Do not include any details about the sights.
    """
    Then the response should be similar to "1. The Colosseum 2. Vatican City 3. Trevi Fountain"
    And the response should not be similar to
      | Bad Response                                        | Reason                              |
      | 1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe    | These are sights in Paris, not Rome |
      | 1. Pane e Salame. 2. Tonnarello 3. Cantina e Cucina | These are restaurants, not sights   |
      | All mimsy were the borogoves                        | Nonsense                            |

    When a user asks the chatbot "Is the Asinelli Tower in Rome?"
    Then the response should be similar to "No, the Asinelli Tower is in Bologna"
    And the response should not be similar to
      | Bad Response                      | Reason      |
      | Yes                               | 100% wrong  |
      | No, the Asinelli Tower is in Pisa | Wrong tower |

  Scenario: Test geography knowledge
    Given a session with the chatbot
    When a user asks the chatbot
    """ 
    List five towns in Tuscany in numbered bullet form. Do not include any details about the towns.
    """
    Then the response should be similar to "1. Florence 2. Siena 3. Lucca 4. Arezzo 5. Viareggio"
    And the response should not be similar to
      | Bad Response                                         | Reason                   |
      | 1. Florence 2. Siena 3. Lucca 4. Naples 5. Viareggio | Naples is not in Tuscany |
      | 1. Florence 2. Siena 3. Lucca                        | Only three towns         |
      | Florence, Siena, Lucca, Naples and Viareggio         | Not a bullet list        |

  Scenario: Test food knowledge
    Given a session with the chatbot
    When a user asks the chatbot
    """ 
    List four typical Florentine main dishes in bullet form.
    List only main courses (no starters, no desserts).
    Do not describe the food; just provide the names of the foods.
    """
    Then the response should be similar to "* Bistecca alla fiorentina  * Ribollita  * Panzanella * Pappa al Pomodoro "
    And the response should not be similar to
      | Bad Response                                                                             | Reason               |
      | * Spaghetti cacio e pepe  * Spaghetti alla carbonara  * Abbachio  * Carciofi alla giudea | Roman food           |
      | * Sfogliatella  * Babà  * Pastiera Napoletana  * Struffoli                               | Neapolitan desserts  |

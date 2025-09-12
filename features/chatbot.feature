Feature: Chatbot knowledge

  @sights
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

    When a user asks the chatbot "Is the Asinelli tower in Rome? Your answer should be at most ten words."
    Then the response should be similar to "No, the Asinelli Tower is in Bologna."
    And the response should not be similar to
      | Bad Response                      | Reason      |
      | Yes                               | 100% wrong  |
      | No, the Asinelli Tower is in Pisa | Wrong tower |

  @geography
  Scenario: Test geography knowledge
    Given a session with the chatbot
    When a user asks the chatbot
    """ 
    List five towns in Tuscany as a numbered list. Do not include any details about the towns.
    Do not explain your reasoning for the selection of towns.
    """
    Then the response should be similar to "1. Florence  2. Pisa  3. Siena  4. Lucca  5. San Gimignano"
    And the response should not be similar to
      | Bad Response                                           | Reason                               |
      | 1. Florence  2. Pisa  3. Siena  4. Naples  5. Verona   | Naples and Verona are not in Tuscany |
      | Florence, Pisa, Siena, Lucca, San Gimignano            | Not a numbered list                  |

  @food
  Scenario: Test food knowledge
    Given a session with the chatbot
    When a user asks the chatbot 
    """
    List four foods that are famous in Sicily.
    Just list the foods without any additional detail.
    """
    Then the response should be similar to "Arancini, Pasta alla Norma, Cannoli, Caponata."
    And the response should not be similar to
      | Bad Response                                                                     | Reason               |
      | Sfogliatella, Babà, Pastiera Napoletana, Struffoli                               | Neapolitan desserts  |
      | Spaghetti Cacio e Pepe, Spaghetti alla Carbonara, Abbachio, Carciofi alla Giudea | Roman food           |

  @irrelevant
  Scenario: Question unrelated to Italy
    Given a session with the chatbot
    When a user asks the chatbot "What is the square root of 10?"
    Then the response should be similar to "The question is about mathematics and is unrelated to Italy. I am unable to assist.""
    And the response should not be similar to
      | Bad Response                                  | Reason              |
      | The square root of 10 is approximately 3.162. | Irrelevant to Italy |
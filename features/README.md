# The BDD Tests
When running the tests, `behave` logs the results to a file, `behave_test.log`.

```
2025-09-16 05:14:01,326 - INFO - Query: I'm in Rome for one day. Suggest three sights, in numbered bullet form, that I should visit.
Do not include any details about the sights.


2025-09-16 05:23:24,329 - INFO - Expected: 1. The Colosseum 2. Vatican City 3. Trevi Fountain, got: 1. Colosseum and Roman Forum  
2. Pantheon  
3. Castel Sant’Angelo
2025-09-16 05:23:24,330 - INFO - Good similarity = 0.8940389830294155
2025-09-16 05:23:26,502 - INFO - Bad comparison: 1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe, similarity = 0.8607740952255404
2025-09-16 05:23:28,771 - INFO - Bad comparison: 1. Pane e Salame. 2. Tonnarello 3. Cantina e Cucina, similarity = 0.8112054030468968
2025-09-16 05:23:29,801 - INFO - Bad comparison: All mimsy were the borogoves, similarity = 0.7066087620852702
2025-09-16 05:23:29,803 - INFO - Query: Is the Asinelli tower in that city? Your answer should be at most ten words
```

The logs include the similarity measures; the tests expected the answer "1. The Colosseum 2. Vatican City 3. Trevi Fountain" which has
a cosine similarity of 0.894 with the actual answer of "1. Colosseum and Roman Forum  2. Pantheon  3. Castel Sant’Angelo"

A wrong answer, "1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe", has a lower cosine similarity of 0.861 with the actual answer.

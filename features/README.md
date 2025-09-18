# The BDD Tests
When running the tests, `behave` logs the results to a file, `behave_test.log`.

```
>>> Test knowledge of Rome
Expected: 1. The Colosseum 2. Vatican City 3. Trevi Fountain
Actual: - Colosseum and Roman Forum
- Pantheon
- Castel Sant’Angelo
Good similarity: 0.8796704807399977
Bad comparison: 1. The Louvre 2. Eiffel Tower 3. Arc de Triomphe
Bad similarity: 0.8460213191439558
Bad comparison: 1. Pane e Salame. 2. Tonnarello 3. Cantina e Cucina
Bad similarity: 0.804558885194027
Bad comparison: All mimsy were the borogoves
Bad similarity: 0.7160645870564805

...

```

The logs include expected versus actual answers and the similarity measure. In the log above, we can see that the similarity between the expected answer 
and the actual answer is 0.880. The similarity between an obviously wrong answer (tourist sights in France, not Rome) and the actual answer is also quite high
(0.846). Nevertheless, the actual answer is closer to a correct answer than an incorrect answer.

The similarity measures are also sensitive to the LLM used to calculate the embedding vectors. For example, for these tests a good answer will typically
have a similarity above 0.8 when using the Qwen3-4B embeddings but is typically a little above 0.6 when using the Mistral-7B embeddings.

It's possible to explicitly set a minimum value that for the similarity for a test to pass

```
Given a session with the chatbot
  When a user asks the chatbot "What is the square root of 10?"
  Then the response should be similar to "The question is about mathematics and is unrelated to Italy. I cannot assist."
  And the similarity should be at least 0.85
```
# GlobeBotter Redux: BDD Testing an LLM Chatbot
<img src="/images/globebotter_redux.png" align="right" width="400px">

In 2023, Valentina Alto in her book ["Building LLM Powered Applications"](https://www.packtpub.com/en-us/product/building-llm-powered-applications-9781835462638) wrote a fun LangChain chatbot, *GlobeBotter*, to help plan a travel intinerary. The source code is on [GitHub](https://github.com/PacktPublishing/Building-LLM-Powered-Applications/blob/main/Chapter%206%20-%20Building%20conversational%20apps.ipynb). The application demonstrated a few things:
 * Retrieval Augmented Generation (RAG)
 * Integrating a tool (Google search) with LangChain
 * Vector Databases (FAISS) for similarity search
 * Using a cloud-hosted LLM (OpenAI)

 In 2023, [LangChain](https://www.langchain.com/) provided opinionated components. However, since 2023, opinions on best practices have changed and LangChain
 has deprecated much of their earlier code. Instead, LangChain now provides AI primitives that developers wire together using *LangGraph* to create applications.
 
 Revisiting *GlobeBotter* seemed like a good way to learn about:
  * Writing a chatbot using the LangGraph idioms
  * Using a local LLM (Qwen3)
  * Switching from FAISS to [ChromaDB](https://www.trychroma.com/)
  * **Writing BDD tests to evaluate a chatbot**


## Testing LLM Applications
One of the challenges with writing LLM applications is testing them. One popular approach is to have a more powerful LLM evaluate the answers of a less
powerful LLM. That's not always possible or cost-effective if you're running an LLM locally. 

This repository explores the idea of testing whether
the response from an LLM application is *similar* to a reasonable (expected) answer. *Vector embeddings* are a fundamental concept in LLMs where text is converted into
a numerical vector of a large dimension (e.g. 2560 or 4096 dimensions) where the embedding captures the meaning and relationship of the text. If we
have two embeddings we can measure how similar the embeddings are by considering the euclidean distance or the (cosine of the) angle between the vectors.
For example, if the angle between the vectors is close to zero, then the cosine similarity will be close to 1.

If we asked a chatbot to suggest three sights that we should visit in Rome, we might expect that it would respond with something like "1. The Colosseum 2. Vatican City 3. Trevi Fountain". Realistically, we're not going to get precisely that answer and we might instead get "1. Colosseum and Roman Forum 2. Pantheon 3. Castel Sant'Angelo" since those are also sensible recommendations. The cosine similarity isn't going to be precisely 1 and we can't even realistically guess whether we should expect the similarity to be above, say, 0.7 or 0.8.

If the LLM is returning sensible answers we would expect the answer to be more similar to "1. Colosseum and Roman Forum 2. Pantheon 3. Castel Sant'Angelo" than to
a list of three tourist sights in Paris. The vector embedding of three tourist sights in Paris would encode the facts (1) that there are three entities and (2) that
the entities are popular with tourists but it would encode "Paris" rather than "Rome". Similarly, the vector embedding of three Roman restaurants would encode (1) that there are three entities and (2) that the entities are in Rome but would not embed the meaning of "tourist sight" in the vector.

The result of this reasoning is that this chatbot is exercised with BDD tests like

```gherkin
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
```

The [chatbot.feature](./features/chatbot.feature) file contains all the tests.


## Prerequisites for Running/Testing the Application
To run this code, you'll need
 * Python 3.11
 * Ollama

### Installing Python Dependencies
You can install the dependencies using either a `virtualenv` or, if you're on Linux, using Anaconda. But, first, check out this repository

```
git clone https://github.com/hammingweight/globebotter_redux.git
cd globebotter_redux
```

#### Using a virtualenv
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

#### Using Anaconda
```
conda env create
conda activate globebotter
```

### Installing Ollama
`GlobeBotter Redux` runs on the Qwen3 LLM with 4 billion parameters (and 4-bit quantization) using Ollama.
To install [Ollama](https://ollama.com/download/linux) and the Qwen3-4B LLM

```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve 
ollama pull qwen3:4b-q4_K_M
```

## Running the Chatbot
The `GlobeBotter Redux` chatbot is a streamlit application; to run it

```
PYTHONPATH=src streamlit run streamlit/app.py
```

The chatbot is then available at [http://localhost:8501](http://localhost:8501)


## Running the Behavior Tests
The tests are run using Python `behave`; to run the tests

```
PYTHONPATH=src behave
```

If the tests all pass, you should see output similar to

```
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
19 steps passed, 0 failed, 0 skipped
Took 28min 48.755s
```
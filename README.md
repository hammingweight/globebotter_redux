# GlobeBotter Redux: BDD Testing an LLM Chatbot
<img src="/images/globebotter_redux.png" align="right" width="400px">

In 2023, [Valentina Alto](https://github.com/valentina-alto) in her book ["Building LLM Powered Applications"](https://www.packtpub.com/en-us/product/building-llm-powered-applications-9781835462638) wrote a fun LangChain chatbot, *GlobeBotter*, to help plan a travel intinerary. The source code is on [GitHub](https://github.com/PacktPublishing/Building-LLM-Powered-Applications/blob/main/Chapter%206%20-%20Building%20conversational%20apps.ipynb). The application demonstrated a few concepts:
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

## The `GlobeBotter Redux` Application
`GlobeBotter Redux` is a chatbot that answers questions about Italy, its culture, its cuisine, sights to see and things to do. The chatbot uses RAG to supplement
the parametric knowledge of the LLM. The RAG information is obtained from a [mini travel guide](https://isiflorence.org/wp-content/uploads/2022/02/MINI-TRAVEL-GUIDE.pdf)
that was chunked and stored in a Chroma vector database.

## Testing LLM Applications
One of the challenges with LLM applications is testing them. One popular approach is to have a more powerful LLM evaluate the answers of a less
powerful LLM. That's not always possible or cost-effective if you're running an LLM locally. 

This repository explores the idea of testing whether
the response from an LLM application is *similar* to a reasonable (expected) answer. *Vector embeddings* are a fundamental concept in LLMs where text is converted into
a numerical vector of a large dimension (e.g. 2560 or 4096 dimensions). The embedding captures the meaning and relationship of the text. If we
have two embeddings, we can measure how similar the embeddings are by considering the euclidean distance or the cosine of the angle between the vectors.
For example, if the angle between the vectors is close to zero, then the cosine similarity will be close to 1.

If we asked a chatbot to suggest three sights that we should visit in Rome, we might expect that it would respond with something like "1. The Colosseum 2. Vatican City 3. Trevi Fountain". Realistically, we're not going to get precisely that answer and we might instead get "1. Colosseum and Roman Forum 2. Pantheon 3. Castel Sant'Angelo". The cosine similarity between our expected and actual answers isn't going to be precisely 1. We can't even assume that the similarity will be above, say, 0.7 or 0.8. However, we would expect the actual answer to be less similar to an answer that is subtly wrong than it is to our expected, correct answer.

If the LLM is returning sensible answers we would expect the answer to be more similar to "1. Colosseum and Roman Forum 2. Pantheon 3. Castel Sant'Angelo" than to
a list of three tourist sights in Paris. The vector embedding of three tourist sights in Paris would encode the facts (1) that there are three entities and (2) that
the entities are popular with tourists but it would encode "Paris" rather than "Rome". Similarly, the vector embedding of three Roman restaurants would encode (1) that there are three entities and (2) that the entities are in Rome but would not embed the meaning of "tourist sight" in the vector.

So we should also add sanity checks that the LLM is returning answers that are more similar to correct answers than wrong ones, like 

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

## Is this BDD Testing Useful?
Initially, I could not get the BDD tests to pass reliably; I needed to tune the application. Parameters that can be tuned are:
 * Document chunking strategies (fixed-size, recursive-character, semantic chunking, etc.)
 * Advanced RAG techniques (hubrid retrieval, contextual compression, etc.)
 * Choice of LLM (Mistral, Qwen, Deepseek, etc.)

Interestingly, I never managed to get all the tests to pass when using Mistral with 7B parameters while I could get the tests to pass when I changed the LLM to Qwen3 with 4B parameters. Mistral-7B uses 4096-dimensional vector embeddings while Qwen3-4B uses 2560-dimensional vectors. An examination of the document snippets retrieved by Mistral showed that they were frequently irrelevant and that the poor performance might have been due to the [curse of dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality).

Contextual compression significantly slowed down the application but was not necessary to get the tests to pass. 

BDD tests like this aren't sufficient to evaluate a RAG application but BDD tests are useful for sanity checking the application when tuning it.


## Prerequisites for Running/Testing the Application
To run this code, you'll need
 * Python 3.11
 * Ollama

### Installing Python Dependencies
You can install the dependencies using either a `virtualenv` or, if you're on Linux, using Anaconda. But, first, check out this repository

```bash
git clone https://github.com/hammingweight/globebotter_redux.git
cd globebotter_redux
```

#### Using a virtualenv
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
```

#### Using Anaconda
```bash
conda env create
conda activate globebotter
```

### Installing Ollama
`GlobeBotter Redux` runs on the Qwen3 LLM with 4 billion parameters (and 4-bit quantization) using Ollama.
To install [Ollama](https://ollama.com/download/linux) and the Qwen3-4B LLM

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve 
ollama pull qwen3:4b-q4_K_M
```


## Running the Behavior Tests
The tests are run using Python `behave`; to run the tests

```bash
PYTHONPATH=src behave
```

If the tests all pass, you should see output similar to

```
1 feature passed, 0 failed, 0 skipped
4 scenarios passed, 0 failed, 0 skipped
19 steps passed, 0 failed, 0 skipped
Took 28min 48.755s
```

By default, the BDD tests use the same LLM as the chatbot (Qwen3-4B) to check that the expected and actual responses are similar.  That might introduce coupling between
the chatbot's behavior and the tests. If you want to use a different (possibly more powerful) LLM to evaluate the expected versus actual test responses, you can pass the name
of a different model via the `LLM_MODEL` environment variable. For example, if you want to use Mistral-7B to check that the chatbot is returning sensible results, you
can run the tests like

```bash
ollama pull mistral:7b-instruct-q4_K_M 
LLM_MODEL="mistral:7b-instruct-q4_K_M" PYTHONPATH=src behave
```

## Running the Chatbot
The `GlobeBotter Redux` chatbot is a streamlit application; to run it

```bash
PYTHONPATH=src streamlit run streamlit/app.py
```

The chatbot is then available at [http://localhost:8501](http://localhost:8501)


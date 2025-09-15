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


## Prerequisites
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
The `GlobeBotter Redux` application is a streamlit app; to run it

```
PYTHONPATH=src streamlit run streamlit/app.py
```

The chatbot is then available at [http://localhost:8501](http://localhost:8501)


## Running the Behavior Tests
The behavior ("BDD") [tests](./features/chatbot.feature) use the `behave` library to test various scenarios. The tests ask the chatbot questions and
check that the chatbot's answer is more `similar` to some expected answer than to some incorrect answers. For more details about how the similarity measures and the tests, read the [README](./features/README.md) in the [features directory](./features/).

To run the tests

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

https://isiflorence.org/wp-content/uploads/2022/02/MINI-TRAVEL-GUIDE.pdf

    Then the response should be similar to "Arancini, Pasta alla Norma, Cannoli, Caponata." # features/steps/chatbot.py:35
Expected: Arancini, Pasta alla Norma, Cannoli, Caponata., got: Couscous alla Trapanese, Caponata, Arancine, Pasta alla norma.
Good similarity = 0.9685369844915186
    And the response should not be similar to                                               # features/steps/chatbot.py:46
      | Bad Response                                                                     | Reason              |
      | Sfogliatella, Babà, Pastiera Napoletana, Struffoli                               | Neapolitan desserts |
      | Spaghetti Cacio e Pepe, Spaghetti alla Carbonara, Abbachio, Carciofi alla Giudea | Roman food          |
Bad similarity = 0.6420451365733053
Bad similarity = 0.6923445125793662


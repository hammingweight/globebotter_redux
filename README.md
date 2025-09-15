# GlobeBotter Redux

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


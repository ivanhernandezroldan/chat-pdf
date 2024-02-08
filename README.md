# py-ai-certificate

## Quick Start

### Clon the repository (SSH)

```
git clone git@github.com:The-Cliff/py-ai-certificate.git

cd py-ai-certificate
```

### Set up the virtual environment

Install [Poetry](https://python-poetry.org/) if you haven't alerady.

```
pip install poetry
```

In the root directory (py-ai-certificate/) run the following command to install the project dependencies, without dev dependencies.

```
poetry install --without dev --sync
```

### Set up the API Key

Grab your API Key, or create a new one, from the [OpenAI](https://platform.openai.com/account/api-keys).

Copy `.env.sample` and name the file `.env`.

```
cp .env.sample .env
```

Open `.env` and set the environment variable `OPENAI_API_KEY` with the API key available on your dashboard.

```
# .env
OPENAI_API_KEY=sk-WWfeS4VHB0XXXXXXXXXXX
```

## Run the app

From the root directory (py-ai-certificate/) run:

```
poetry run streamlit run main.py
```



## Testing

In the root directory (py-ai-certificate/) run the following command to install all the project dependencies:

```
poetry install --sync
```

In order to perform static type checking with Mypy, run the following command in the root directory (py-ai-certificate/):

```
mypy src
```

Once you've got all the requirements in place, you should be able to test the app by simply running:

```
python -m pytest
```
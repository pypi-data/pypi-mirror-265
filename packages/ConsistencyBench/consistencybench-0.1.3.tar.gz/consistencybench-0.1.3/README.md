# ConsistencyBench

## Setup

First install the package from PyPI.

```bash
pip install consistencybench
```
Additionally, if you'd like to use the NER metric (`consistencybench.metrics.AgreementNER`), run the following first.
```bash
python -m spacy download en_core_web_sm
```

## To start generation and scoring

Set the arguments from `run_eval.py`

```bash
python run_eval.py --openai_api_key <OPENAI_API_KEY>
```

**Example Output file**: `consistencybench/result_gpt-3.5-turbo_paraphrasing.csv`

**Example Jupyter Notebook**: `example.ipynb`

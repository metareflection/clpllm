# CLP(LLM)

The idea is to use an LLM to decide whether a list of sentences are consistent.

For now, we have propositional sentences, and conjunctions and disjunctions at the search level.

In the future, we might want to be able to normalize and decrease the size of the constraint set. One idea is that the LLM could generate summaries.


## Setup

First create a `.env` file in the root directory containing your OpenAI API key:

```bash
OPENAI_API_KEY="sk-xxxx"
```

Also install the Python dependencies:

```bash
pip install -r requirements.txt
```

To use the `ollama` server and model file

`brew install ollama`
`ollama pull orca2`
`ollama create constraint_solver -f constraint_solver.model`

Then start the server and you can communicate with the model via `ollama run constraint_solver` 

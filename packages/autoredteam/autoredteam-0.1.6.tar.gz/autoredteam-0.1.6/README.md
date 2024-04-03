# autoredteam

Automated Red Teaming Test suite by [vijil](https://www.vijil.ai/).

## CLI calling patterns

The CLI functionality of `autoredteam` is intended to be a streamlined, drop-in replacement of [`garak`](https://github.com/leondz/garak/).
Currently, you can use it to kick off tests by either module (`--tests`) or dimension (`--dimensions`).

```
python -m autoredteam --model_type <> --model_name <> --tests <>
python -m autoredteam --model_type <> --model_name <> --dimensions <>
python -m autoredteam --model_type <> --model_name <> --rag <> --metrics <> --documents_path <>
```
We currently support LLMs hosted on a number of model providers as agents. For a model provider, there are three possible deployment types: local model, public API, and private endpoint. Some providers offer only a subset of these deployment types.

## Options

Below are the options that are currently supported for selection through CLI. The default is set to only evaluate a single model in a standalone fashion but you can also test a RAG setup as well. You need to provide a seed document(s) and our backend will generate a set of potential questions and responses to evaluate based on the defined metrics. It is worth noting that you can also run our typical tests against the LLM in a RAG setting by providing --tests or --dimensions in addition to --rag, --metrics, and --documents_path.

--model_type, -m: Specifies the module and optionally also class of the generator, e.g. 'huggingface', or 'openai'. This is a required argument.
--model_name, -n: Specifies the name of the model, e.g. 'timdettmers/guanaco-33b-merged'. This is an optional argument.
--generations, -g: Specifies the number of generations to run. The default value is 10.
--tests, -t: Specifies a list of test modules to run. This is an optional argument.
--dimensions, -d: Specifies a list of test dimensions to use. This is an optional argument.
--rag, -r: A boolean flag to select rag. The default value is False.
--metrics, -me: Specifies a list of metrics to use, separated by space. This is an optional argument.
--documents_path, -dp: Specifies the path to the documents. This is an optional argument.

The following table provides respective `--model_type` values for each such provider x deployment type. If a deployment type is not listed for a provider, the respective radio button should be inactive in the GUI.

| Agent | Deployment Type | `model_type`
|---|---|---|
| Anyscale | public API | `anyscale` |
| Hugging Face | public API | `huggingface` |
| | private endpoint | `huggingface.InferenceEndpoint` |
| Mistral | public API | `mistral` |
| Replicate | public API | `replicate` |
| | private endpoint | `replicate.ReplicateEndpoint` |
| OctoAI | public API | `octo` |
| | private endpoint | `octo.OctoEndpoint` |
| OpenAI | public API | `openai` |
| Together | public API | `together` |
| REST API | public API | `rest` |

When `model_type` is `rest`, a config file supplied as `model_name`, which contains the URL, API key name, and prompt and response handlers to handle input and output patterns associated with the specific URL. Example as follows

```
python -m autoredteam --model_type rest --model_name notebooks/config/together.json --tests <>
```

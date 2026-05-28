This folder contains a Perl implementation of an AI-powered data classification
engine.

The engine uses an OpenAI-compatible chat completions endpoint, with OpenRouter
as the default provider.

## Files

```text
bin/classify_text.pl              CLI demo script
lib/DataSec/Classifier.pm         Reusable classifier module
t/classifier.t                    Unit tests
```

## What It Classifies

For each short text sample, the engine asks the LLM to return JSON with:

| Field | Meaning |
| --- | --- |
| `sensitivity` | `public`, `internal`, `confidential`, or `restricted` |
| `category` | Type of data, such as `credential`, `personal_data`, or `financial` |
| `risk` | `low`, `medium`, `high`, or `critical` |
| `reason` | Short explanation |

Example output:

```json
{
   "category" : "credential",
   "reason" : "The text contains a password-like secret.",
   "risk" : "critical",
   "sensitivity" : "restricted"
}
```

## Requirements

- Perl 5.34 or newer.
- No CPAN dependencies are required.
- An OpenRouter API key, or another OpenAI-compatible API key.

The implementation uses only available/core Perl modules:

- `HTTP::Tiny`
- `JSON::PP`
- `Getopt::Long`
- `Test::More`

## Run A Live Demo With OpenRouter

From this folder:

```bash
OPENROUTER_API_KEY="your-api-key" \
perl bin/classify_text.pl --text "User email: ana@example.com"
```

The default endpoint is:

```text
https://openrouter.ai/api/v1/chat/completions
```

The default model is:

```text
openai/gpt-4o-mini
```

You can override the model:

```bash
OPENROUTER_API_KEY="your-api-key" \
perl bin/classify_text.pl \
  --model "openai/gpt-4o-mini" \
  --text "AWS_SECRET_ACCESS_KEY=abc123"
```

## Run A Live Demo With Ollama

Ollama also exposes an OpenAI-compatible chat completions endpoint.

Start Ollama:

```bash
ollama serve
```

Check available models:

```bash
ollama list
```

Run the classifier against local Ollama:

```bash
OPENAI_API_KEY="ollama" \
perl bin/classify_text.pl \
  --endpoint "http://127.0.0.1:11434/v1/chat/completions" \
  --model "qwen2.5:7b" \
  --text "Customer email: ana@example.com password=secret123"
```

`OPENAI_API_KEY="ollama"` is a dummy value for local Ollama. The local server
usually does not require a real API key, but the classifier uses the same bearer
token flow as OpenAI-compatible hosted providers.

## Use Another OpenAI-Compatible Endpoint

```bash
OPENROUTER_API_KEY="your-api-key" \
perl bin/classify_text.pl \
  --endpoint "https://your-provider.example.com/v1/chat/completions" \
  --model "your-model-name" \
  --text "Customer CPF: 123.456.789-00"
```

The environment variable name `OPENROUTER_API_KEY` is used because OpenRouter is
the default provider. The code also accepts `OPENAI_API_KEY` for compatible
providers. In both cases, the value is sent as a bearer token.

## Input Options

Pass text directly:

```bash
OPENROUTER_API_KEY="your-api-key" \
perl bin/classify_text.pl --text "password: hunter2"
```

Read from a file:

```bash
OPENROUTER_API_KEY="your-api-key" \
perl bin/classify_text.pl --file sample.txt
```

Read from stdin:

```bash
echo "Credit card 4111 1111 1111 1111" | \
OPENROUTER_API_KEY="your-api-key" perl bin/classify_text.pl
```

## How The Code Works

1. The CLI reads the text sample from `--text`, `--file`, or stdin.
2. `DataSec::Classifier` builds a strict classification prompt.
3. The classifier sends an HTTP POST request to the chat completions endpoint.
4. The LLM response is expected to contain JSON.
5. The code parses and validates the required fields.
6. The CLI prints formatted JSON for the evaluator.

## Why The Tests Do Not Call The Real API

The tests inject a fake HTTP function into the classifier. This makes the tests:

- Fast.
- Deterministic.
- Runnable without an API key.
- Runnable without internet access.

## Run Tests

From this folder:

```bash
perl -Ilib t/classifier.t
```

From the repository root:

```bash
perl -Ichallenge-4/lib challenge-4/t/classifier.t
```

![chat-cli-anything](./logo.png)

# Chat-Cli-Anything

Interact with GPT-like services from the command line, supports local RAG, and pipe input.

## Tutorial

1. Installation

```shell
pip install "chat-cli-anything[all]"
```

To simplify command length, set command aliases (optional)

```shell
alias config="cc-config"
alias code="cc-code"
alias chat="cc-chat"
alias db="cc-db"
alias service="cc-service"
```

2. Add LLM provider

```
cc-config add "openai" "https://api.openai.com/v1"  --api-key "your-api-key"
```

If command aliases are set

```
config add "openai" "https://api.openai.com/v1"  --api-key "your-api-key"
```

3. Start Using

*example1* Normal question

```
cc-ask "Who is the author of the science fiction novel 'Three Body'?"
```

*example2* Using pipe

```
cat names_of_diseases.txt | cc-ask "What are the most common types of diseases among the names listed?"
```

*example3* Interactive questioning

```
cc-chat "What is the capital of France?"
```

*example4* Local RAG

step 1: Digest text to build a local database

```
cc-db ingest "/path/to/西游记.txt" -n xiyouji
```

step 2: Ask a question

```
# for open question, '-a/--advance' option would be helpful
cc-ask -d xiyouji "孙悟空一打白骨精的时候说了啥" -a
```


## Commands

### cc-config
Configure LLM provider

#### 1. Add LLM provider

```
cc-config add [OPTIONS] NAME BASE_URL

Options:
  --model TEXT
  --api-key TEXT
  --proxy TEXT
  --help          Show this message and exit.
```

example:

```
cc-config add "openai" "https://api.openai.com/v1"  --model "gpt-3.5-turbo-1106" --api-key "sk-xxxxxxxxxxx"
```

#### 2. Test provider
```
cc-config ping [OPTIONS] NAME

  Switch to a different configuration and save the change.

Options:
  --help  Show this message and exit.
```

#### 3. List all providers

```
cc-config list [OPTIONS]

  List all configurations.

Options:
  -s, --show-api-key
  --help              Show this message and exit.
```
The default api-key is hidden, use `-s/--show-api-key` to display the key.

#### 4. Remove provider
```
cc-config remove [OPTIONS] [NAME]

  Remove a configuration.

Options:
  --help  Show this message and exit.
```

#### 5. Switch active provider
```
ask.py cc-config switch [OPTIONS] NAME

  Switch to a different configuration and save the change.

Options:
  --help  Show this message and exit.
```

#### 6. Load configuration file
```
Import configurations.

Options:
  -o, --override  Whether override original config.
  --help          Show this message and exit.
```

#### 7. Export configuration file
```
ask.py cc-config dump [OPTIONS] PATH

  Export current configurations.

Options:
  -o, --override  Whether override existing file.
  --help          Show this message and exit.
```

### cc-ask

Perform a question-answering task
```
cc-ask [OPTIONS] QUERY

  Start a chat session with the given query.

Options:
  -d, --db TEXT        Name of database.
  -f, --filename TEXT  Name of file.
  -r, --rerank         Whether to rerank the results.
  -s, --show-chunks    Whether to show the related chunks retrieved from
                       database.
  -a, --advance        Whether to use advance RAG.
  --help               Show this message and exit.
```

### cc-chat
Interactive Q&A
```
cc-chat [OPTIONS] [QUERY]

  Interactive chat. Enter '/quit' to exit

Options:
  -d, --db TEXT          name of database.
  -f, --filename TEXT    Name of file.
  -n, --not-interactive
  -s, --show-history
  -c, --clear
  --help                 Show this message and exit.
```

### cc-code
Some common commands for code based on cc-ask.

#### Code Explanation

```
cc-code explain [OPTIONS] [FILENAME] [OBJECT_NAME]

  Explain code.

Options:
  --help  Show this message and exit.
```

example1: Specify filename
```
cc-code explain some_complex_scripts.py
```

example2: Specify a particular function
```
cc-code explain some_complex_scripts.py SomeClass::some_function
```

example3: Use pipe
```
cat some_complex_scripts.py | cc-code explain
```

#### Fix Issues
```
cc-code fix [OPTIONS] [FILENAME] [OBJECT_NAME]

  Fix code.

Options:
  --help  Show this message and exit.
```

#### Code Refactoring
```
cc-code refactor [OPTIONS] [FILENAME] [OBJECT_NAME]

  Refactor code.

Options:
  --help  Show this message and exit.
```

#### Code Review
```
cc-code review [OPTIONS] [FILENAME] [OBJECT_NAME]

  Review code.

Options:
  --help  Show this message and exit.
```

#### Code Translation
```
cc-code translate [OPTIONS] [FILENAME] [OBJECT_NAME] LANGUAGE

  Translate code from one language to another. Supported languages include c++, cpp,
  c, rust, typescript, javascript, markdown, html.

Options:
  --help  Show this message and exit.
```

#### Select Code from Generated Results

Used to select code snippets from the generated responses of the above commands

```
cc-code select [OPTIONS] [INDEX]

  Select code snippet from last output.

  Argument:     index: code snippet index

Options:
  -c, --count  get the number of code snippets
  --help       Show this message and exit.
```

`-c/--count` Get the number of candidate code blocks in the last response

example:
```
>>> cc-code select -c
2

# Select the second code block from the last output
# for macos
>>> cc-code select 1 | pbcopy
# for linux
>>> cc-code select 1 | xclip -selection clipboard
```

### cc-db

#### list: List all text collections
```
cc-db list [OPTIONS] [NAME]

  List all document databases

Options:
  -s, --short  List in short format
  --help       Show this message and exit.
```

#### ingest: Digest documents
```
cc-db ingest [OPTIONS] [FILES]...

  Read documents and convert them into a searchable database.

Options:
  -n, --name TEXT     The name of the knowledge base.
  -m, --comment TEXT  Add comment to info
  --help              Show this message and exit.
```

#### remove: Remove text collection
```
cc-db remove [OPTIONS] NAME

  Remove database with the given name.

Options:
  -d, --remove-documents  Remove documents if data
  --help                  Show this message and exit.
```

#### search: Search within a document collection
```
cc-db search [OPTIONS] DB QUERY

Options:
  -k, --topk INTEGER  Number of top results to return.
  --help              Show this message and exit.
```

### cc-service
Used to manage local text-to-index services

#### start:
```
cc-service start [OPTIONS]

Options:
  --help  Show this message and exit.
```

#### stop:
```
cc-service stop [OPTIONS]

Options:
  --help  Show this message and exit.
```

#### status
```
cc-service status [OPTIONS]

Options:
  --help  Show this message and exit.
```

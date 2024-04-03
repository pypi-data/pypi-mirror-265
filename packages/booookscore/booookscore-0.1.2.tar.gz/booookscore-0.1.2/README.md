# BooookScore

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)
[![arxiv](https://img.shields.io/badge/arXiv-2305.14251-b31b1b.svg)](https://arxiv.org/abs/2310.00785)

This repository hosts the official code and data release for our ICLR 2024 paper, [BooookScore: A systematic exploration of book-length summarization in the era of LLMs](https://arxiv.org/abs/2310.00785). There are 4 O's!

If you find BooookScore useful, please cite:
```
@inproceedings{
    chang2024booookscore,
    title={BooookScore: A systematic exploration of book-length summarization in the era of {LLM}s},
    author={Yapei Chang and Kyle Lo and Tanya Goyal and Mohit Iyyer},
    booktitle={The Twelfth International Conference on Learning Representations},
    year={2024},
    url={https://arxiv.org/pdf/2310.00785.pdf}
}
```

# Announcements

- `2024/04/01` BooookScore is now available as a Python package!
- `2024/02/27` We now have BooookScore v2, a version that batches sentences when obtaining model-generated annotations for summaries. Kudos to [@IlyaGusev](https://github.com/IlyaGusev) for implementing this!
- `2023/10/10` Initial data release: all summaries, GPT-4 annotations, and human annotations.

# Install BooookScore

```
pip install booookscore
```

# Using BooookScore

## Getting chunked data

Before running the chunking script, you need to have a **pickle** file containing a dictionary, where keys are book names and values are full texts of the books. Refer to `data/example_all_books.pkl` for an example. Once you have this file ready, run the following command to chunk the data:

```
python -m booookscore.chunk --chunk_size {chunk_size} --input_path {input_path}
```

- `--chunk_size`: your desired chunk size (each chunk will not exceed this limit)
- `--input_path`: should be set to the path storing the pickle file described above
- `--include_empty_lines` (optional): if specified, it does not remove the empty lines that may exist in the input texts

Example usage:

```
python -m booookscore.chunk --chunk_size 2048 --input_path all_books.pkl
```

In this example, the chunked data will be saved to `all_books_2048.pkl`.

## Obtain summaries

```
python -m booookscore.summ --book_path {book_path} --summ_path {summ_path} --model {model} 
    --openai_key {openai_key} --method {method} --chunk_size {chunk_size} 
    --max_context_len {max_context_len} --max_summary_len {max_summary_len}
```

- `--book_path`: the path to the chunked data (pickle file)
- `--summ_path`: the path to save the generated summaries
- `--model`: the name of the language model to use for summarization (currently only supports models in the OpenAI API)
- `--openai_key`: the path to the txt file storing your OpenAI API key
- `--method`: the summarization method to use, "inc" for incremental updating, "hier" for hierarchical merging
- `--chunk_size`: the desired size of each chunk of text, must be consistent with your data in `book_path`
- `max_context_len`: the maximum context window of the model
- `max_summary_len`: the maximum number of tokens a summary can have

Example usage:

```
python -m booookscore.summ --book_path all_books_chunked_4096.pkl --summ_path summaries.json 
    --model gpt-4 --openai_key openai_key.txt --method hier --chunk_size 4096 --max_context_len 32000
```

### Checkpointing

Incremental updating saves progress every 10 chunks. Hierarchical merging saves progress every book. Improved checkpointing for hierarchical merging will be implemented in future versions.

## Post-processing summaries

After generating summaries with incremental updating or hierarchical merging, we create a json file with a dictionary that maps book names to their final summaries. If the input file is `summaries.json`, then the extracted final summaries will be saved to `summaries_cleaned.json`.

```
python -m booookscore.postprocess --input_path {input_path} 
    --model {model} --openai_key {openai_key}
```

- `--input_path`: the path to the chunked data (pickle file)
- `--model` (optional): the name of the language model to use for summarization (currently only supports models in the OpenAI API), defaults to `gpt-4`
- `--openai_key` (optional): the path to the txt file storing your OpenAI API key
- `--remove_artifacts` (optional): if specified, it will ask a language model remove artifacts from merging (must also specify `model` and `openai_key` in this case)

Example usage (without artifact removal):

```
python -m booookscore.postprocess --input_path summaries.json 
    --model {model} --openai_key {openai_key}
```

## Compute BooookScore

```
python -m booookscore.score --summ_path {summ_path} --annot_path {annot_path} 
    --model {model} --openai_key {openai_key}
```

The input summaries must be stored in a json file that maps from book names to final book summaries.

- `--summ_path`: the path to all summaries (must specify if there are no annotations yet)
- `--annot_path`: the path to model-generated annotations
- `--model`: the name of the language model to use for summarization (currently only supports models in the OpenAI API), defaults to `gpt-4`
- `--openai_key`: the path to the txt file storing your OpenAI API key
- `--v2` (optional): if specified, it will generate annotations using v2 code and prompt, which uses sentence batching instead of evaluating sentence by sentence (contributed by [@IlyaGusev](https://github.com/IlyaGusev)!)
- `--batch_size` (optional): batch size to use if using v2, defaults to `10`

Example usage (original BooookScore):

```
python -m booookscore.score --summ_path summaries/chatgpt-2048-hier-cleaned.json 
    --annot_path annotations.json --model gpt-4 --openai_key openai_key.txt
```

Example usage (v2 BooookScore with sentence batching):

```
python -m booookscore.score --summ_path summaries/chatgpt-2048-hier-cleaned.json 
    --annot_path annotations.json --model gpt-4 --openai_key openai_key.txt --v2 --batch_size 10
```

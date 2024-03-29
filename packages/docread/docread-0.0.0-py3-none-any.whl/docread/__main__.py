import os
import sys
import json
import argparse
import traceback
from dotenv import load_dotenv


def load_env(args):
    if args.env:
        load_dotenv(args.env)

def read(args, parser):
    from docread.reader import Reader
    llm_provider = os.environ.get("LLM_PROVIDER") or "openai"
    llm_args = {
        "base_url": os.environ.get("OPENAI_API_BASE"),
        "api_key": os.environ.get("OPENAI_MODEL_NAME") or "sk-",
        "model": os.environ.get("OPENAI_MODEL_NAME") or "gpt-3.5-turbo"
    }

    reader = Reader(
        token_limit=args.token_limit,
        text_threshold=args.text_threshold,
        llm_provider=llm_provider,
        llm_args=llm_args
    )

    src = args.src
    dst = args.dst

    reader.read(src, dst, progress=True)

    if not args.embed:
        embed_model = os.environ.get("EMBED_MODEL")
        if embed_model is None:
            raise ValueError("EMBED_MODE required.")
        embed_model_args = os.environ.get("EMBED_MODEL_ARGS")
        if embed_model_args:
            embed_model_args = json.loads(embed_model_args)
        reader.embed(file=src, output=dst, model=embed_model, model_args=embed_model_args)

def extract_epub(args):
    from docread.epub import extract_file
    extract_file(src=args.src, dst=args.dst)

def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog='docread',
    )
    parser.add_argument('--env', default='.env', metavar="ENV_FILE", help="environment configuration file")
    parser.add_argument('--traceback', action="store_true", help="print error traceback")

    subparser = parser.add_subparsers(title="commands", help="type command --help to print help message")

    parser_read = subparser.add_parser('read', help="read document")
    parser_read.add_argument(
        "src", default=None, help="doc file to read"
    )

    parser_read.add_argument(
        "dst", nargs="?", default=None, help="output file"
    )
    parser_read.add_argument('--token-limit', default=1000, help="token limit per gist")
    parser_read.add_argument('--text-threshold', default=100, help="min text length per gist")
    parser_read.add_argument('--embed', default=True, action="store_true", help="just embeddings")
    parser_read.set_defaults(func=lambda args: read(args=args, parser=parser_read))

    parser_epub = subparser.add_parser('epub', help="extract epub")
    parser_epub.add_argument(
        "src", default=None, help="epub files to extract"
    )

    parser_epub.add_argument(
        "dst", nargs="?", default=None, help="output file or dir"
    )
    parser_epub.set_defaults(func=extract_epub)

    args = parser.parse_args(argv)
    return args, parser

def main():
    args, parser = parse_args(sys.argv[1:])

    load_env(args=args)

    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            if args.traceback:
                traceback.print_exc()
            else:
                print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye.\n")

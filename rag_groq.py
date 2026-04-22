import argparse
from rag.commands import cmd_check, cmd_baseline, cmd_rag
from rag.indexing import build_index

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check")
    sub.add_parser("index")

    p_base = sub.add_parser("baseline")
    p_base.add_argument("question", type=str)

    p_rag = sub.add_parser("rag")
    p_rag.add_argument("question", type=str)
    p_rag.add_argument("--top_k", type=int, default=4)

    args = p.parse_args()

    if args.cmd == "check":
        cmd_check()
    elif args.cmd == "index":
        build_index()
    elif args.cmd == "baseline":
        cmd_baseline(args.question)
    elif args.cmd == "rag":
        cmd_rag(args.question, top_k=args.top_k)

if __name__ == "__main__":
    main()

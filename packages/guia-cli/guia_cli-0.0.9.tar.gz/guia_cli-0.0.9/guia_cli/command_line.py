import argparse
import os
import sys
import re
from datetime import datetime

from guia_cli.assistant import create_gu_agent, gu_is_coding, gu_is_mentoring


def use_argparse():
    parser = argparse.ArgumentParser(
        description="Gu, the specialist agent in Software Engineering"
    )
    parser.add_argument(
        "--coding",
        nargs="?",
        metavar="YOUR REQUEST",
        const="default",
        type=str,
        help="Use coding skill",
    )
    parser.add_argument(
        "--mentoring",
        metavar="YOUR QUESTION",
        nargs="?",
        type=str,
        help="Use mentoring skill",
    )
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    return args


def parse_filename(resultType, identifier):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    identifier_clean = re.sub(r"[^\w\s]", "_", identifier).replace(" ", "_")
    filename = f"{timestamp}__{resultType}__{identifier_clean}.md"
    return filename.lower()


def save_data_to_file(filename, data):
    output_path = f"./outputs/{filename}"
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True,
    )
    with open(output_path, "w") as file:
        file.write(data)
    return output_path


def output_result(result):
    print("========================== Gu answer's ============================")
    print(result)
    print("============================== END ================================")


def main():
    args = use_argparse()
    gu = create_gu_agent()

    result = ""
    resultType = ""

    if args.coding:
        result = gu_is_coding(gu, args.coding)
        resultType = "coding"
    elif args.mentoring:
        result = gu_is_mentoring(gu, args.mentoring)
        resultType = "mentoring"

    output_result(result)

    output_path = save_data_to_file(
        filename=parse_filename(resultType, args.coding or args.mentoring),
        data=result,
    )
    print(f"[+] Result saved in: {output_path}")


if __name__ == "__main__":
    main()

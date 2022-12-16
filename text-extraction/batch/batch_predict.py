import os
import argparse
import json
from extractor import extract_pdf
import traceback
cnvrg_workdir = os.environ.get("CNVRG_WORKDIR", "/cnvrg")

# argument parsing
def argument_parser():
    parser = argparse.ArgumentParser(description="""Creator""")
    parser.add_argument(
        "--dir",
        action="store",
        dest="dir",
        required=True,
        help="""directory containing all pdf files""",
    )
    return parser.parse_args()


def validation(args):
    """
    check if the pdf directory provided is a valid path if not raise an exception

    Arguments
    - argument parser

    Raises
    - An assertion error if the path provided is not a valid directory
    """
    assert os.path.exists(args.dir), " Path to the files provided does not exist "


def main():
    args = argument_parser()
    dir = args.dir
    validation(args)

    finaljson = {}
    for filepdf in os.listdir(dir):
        # check if the file is a pdf file
        if filepdf.endswith(".pdf"):
            truepath = os.path.join(dir, filepdf)
            try:
                output = extract_pdf(truepath)
                finaljson[filepdf] = output
            except Exception:
                print("Ran into the following problem while extractin text from: ", filepdf)
                print(traceback.format_exc())
                continue
    with open(cnvrg_workdir+"/result.json", "w") as outfile:
        json.dump(finaljson, outfile)


if __name__ == "__main__":
    main()

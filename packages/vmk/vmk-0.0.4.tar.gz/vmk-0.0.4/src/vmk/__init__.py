import argparse
from .combiner import Combiner


DEFAULT_OUT_FILE = 'CombinedFirstPages1.pdf'
DEFAULT_DIR = './'


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out', help="Output file")

input_type = parser.add_mutually_exclusive_group()
input_type.add_argument('-f', '--files', help="Input files", nargs='+')
input_type.add_argument('-d', '--dir', help="Input directory")


def main():
    args = parser.parse_args()
    combiner = Combiner()
    out = args.out or DEFAULT_OUT_FILE
    
    if args.files:
        for f in args.files:
            combiner.add_file(f)

        combiner.assemble()
        combiner.write_pdf(out)
        print('Combined files into', out)
        return
    
    target_dir = args.dir or DEFAULT_DIR
    combiner.combine_pdfs_in_folder(args.dir, out)
    print('Combined all PDF files in', args.dir, 'into', out)

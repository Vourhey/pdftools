#!/usr/bin/env python3
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter


def main():
    parser = argparse.ArgumentParser(description="PDF Toolkit by Vourhey")
    subparser = parser.add_subparsers()

    parser_split = subparser.add_parser(
        'split', help='Splits a given pdf into pages', aliases=['s'])
    parser_split.add_argument('input', type=argparse.FileType('rb'),
                              help='A pdf file to be split')
    parser_split.add_argument('-o', '--output', type=str,
                              help='A prefix for output files',
                              default='output')
    parser_split.set_defaults(func=split)

    parser_merge = subparser.add_parser(
        'merge', help='Merges given pdfs into one pdf file', aliases=['m'])
    parser_merge.add_argument(
        '-o', '--output', type=argparse.FileType('wb'),
        default=open('output.pdf', 'wb'), help='Specify output file')
    parser_merge.add_argument('input', type=argparse.FileType('rb'), nargs='+')
    parser_merge.set_defaults(func=merge)

    args = parser.parse_args()
    if len(vars(args)) == 0:
        parser.print_help()
    else:
        args.func(args)


def split(args):
    reader = PdfFileReader(args.input)
    padding = len(str(reader.getNumPages()))
    format_str = '{}-{{:0{}d}}.pdf'.format(args.output, padding)
    for i in range(reader.getNumPages()):
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(i))
        stream = open(format_str.format(i), 'wb')
        writer.write(stream)


def merge(args):
    writer = PdfFileWriter()
    for f in args.input:
        reader = PdfFileReader(f)
        writer.appendPagesFromReader(reader)

    writer.write(args.output)


if __name__ == '__main__':
    main()

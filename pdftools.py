#!/usr/bin/env python3
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter


def main():
    parser = argparse.ArgumentParser(description="PDF Toolkit by Vourhey")
    subparser = parser.add_subparsers()

    parser_split = subparser.add_parser('split')
    parser_split.add_argument('input', type=argparse.FileType('rb'))
    parser_split.add_argument(
        '-o', '--output', type=argparse.FileType('wb'), nargs='?')
    parser_split.set_defaults(func=split)

    parser_merge = subparser.add_parser('merge')
    parser_merge.add_argument(
        '-o', '--output', type=argparse.FileType('wb'),
        default=open('output.pdf', 'wb'), help='Specify output file')
    parser_merge.add_argument('input', type=argparse.FileType('rb'), nargs='+')
    parser_merge.set_defaults(func=merge)

    args = parser.parse_args()
    args.func(args)


def split(args):
    reader = PdfFileReader(args.input)
    padding = len(str(reader.getNumPages()))
    format_str = 'output-{{:0{}d}}.pdf'.format(padding)
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

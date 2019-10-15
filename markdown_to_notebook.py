#!/usr/bin/env python

import argparse
import enum
import json
import re
import sys


parser = argparse.ArgumentParser()
parser.add_argument('files', metavar='file', nargs='+', help='Files to compute')
#parser.add_argument('-t', '--title-split', action='store_true')
#parser.add_argument('-p', '--title-page', action='store_true')
parser.add_argument('-o', '--output', default=None)
# Add argument to split on files
# + choose the type of slide when split (ex: file=slide, title=sub-slide or subtitle=sub-slide)
# Possible splits : split on a ---, split on new file, split on title of level ≤N
# For each split : what is the type of the new cell (slide, sub-slide, fragment)?
# For title splits : Should the title be on a separate cell? What is the type of the next cell? => split on title + split after title
# Each split gives the type of the following cell
# Option to give configuration file
args = parser.parse_args()

title_split = {1: 'slide', 2: 'subslide'}
title_split_after = {}


def make_cell(cell_type, source, slide_type='-'):
    cell = {
        'cell_type': cell_type,
        'metadata': {
            'slideshow': {
                'slide_type': slide_type,
            },
        },
        'source': source,
    }

    if cell_type == 'code':
        cell['outputs'] = []
        cell['execution_count'] = None

    return cell


def clean_cell(cell):
    lines = cell['source']

    while lines and not lines[0].rstrip('\r\n'):
        lines.pop(0)
    while lines and not lines[-1].rstrip('\r\n'):
        lines.pop()

    if lines:
        lines[-1] = lines[-1].rstrip('\r\n')

    return cell


class CellType(enum.IntEnum):
    SLIDE = enum.auto()
    SUBSLIDE = enum.auto()
    FRAGMENT = enum.auto()
    NORMAL = enum.auto()
    SKIP = enum.auto()


class _Token:
    def __init__(self, _type, line=None, **kwargs):
        self.type = _type
        self.line = line
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        args = []
        if self.line is not None:
            args.append(repr(self.line))
        for key, value in self.params.items():
            args.append(f'{key}={value!r}')

        return f"{self.type}({', '.join(args)})"


class Token(enum.Enum):
    def __call__(self, *args, **kwargs):
        return _Token(self, *args, **kwargs)

    LINE = enum.auto()
    FILE = enum.auto()
    TITLE = enum.auto()
    AFTER_TITLE = enum.auto()
    SPLIT = enum.auto()
    START_CODE = enum.auto()
    END_CODE = enum.auto()


def iter_file(filename):
    code = False

    with open(filename) as f:
        for line in f:
            if code:
                if line.startswith('```'):
                    code = False
                    yield Token.END_CODE(line)
                else:
                    yield Token.LINE(line)
                continue

            match = re.match(r'(#+) ', line)
            if match:
                level = len(match.group(1))
                yield Token.TITLE(line, level=level)
                yield Token.AFTER_TITLE(line, level=level)
            elif line.startswith('---'):
                yield Token.SPLIT(line)
            elif line.startswith('```'):
                code = True
                args = line[3:].split()
                skip = 'skip' in args
                yield Token.START_CODE(line, language=args[0], skip=skip)
            else:
                yield Token.LINE(line)


def iter_files(filenames):
    for filename in filenames:
        yield from iter_file(filename)
        yield Token.FILE()


def get_cells(filenames):
    cell_type, lines = 'markdown', []
    for token in iter_files(filenames):
        if token.type is Token.FILE:
            pass
        elif token.type is Token.TITLE:
            if token.level in title_split:
                yield cell_type, lines
                yield 'separator', title_split[token.level]
                cell_type, lines = 'markdown', [token.line]
            else:
                lines.append(token.line)
        elif token.type is Token.AFTER_TITLE:
            if token.level in title_split_after:
                yield cell_type, lines
                yield 'separator', title_page[token.level]
                cell_type, lines = 'markdown', []
        elif token.type is Token.SPLIT:
            yield cell_type, lines
            yield 'separator', 'subslide'
            cell_type, lines = 'markdown', []
        elif token.type is Token.START_CODE:
            yield cell_type, lines
            yield 'separator', 'skip' if token.skip else '-'
            cell_type, lines = 'code', []
        elif token.type is Token.END_CODE:
            yield cell_type, lines
            cell_type, lines = 'markdown', []
        elif token.line is not None:
            lines.append(token.line)
    yield cell_type, lines


cells = []
slide_type = '-'
for cell_type, content in get_cells(args.files):
    if cell_type == 'separator':
        slide_type = content
        continue
    cell = make_cell(cell_type, content, slide_type)
    cell = clean_cell(cell)
    if cell['source']:
        cells.append(cell)
        slide_type = '-'

doc = {
    'cells': cells,
    'metadata': {
        'celltoolbar': 'Slideshow',
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {
                'name': 'ipython',
                'version': 3
            },
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.6.5'
        },
        "livereveal": {
            "autolaunch": True
        }
    },
    'nbformat': 4,
    'nbformat_minor': 2,
}


if args.output:
    f = open(args.output, 'w')
else:
    f = sys.stdout

with f:
    json.dump(doc, f, indent=4)

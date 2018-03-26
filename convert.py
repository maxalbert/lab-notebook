#!/usr/bin/env python

# TODOs:
#
#  - Unordered lists based on indentation level
#
#    Currently, unordered lists need to be written in AsciiDoc style, e.g.:
#       * First level
#       ** Second level
#
#    It would be nice if we could use GH-flavoured markdown style, e.g.:
#
#       - First level
#          - Second level
#
#    This would be a simple preprocessing step.

import re
import sys
import textwrap

OUTFILE = "merged.adoc"

preamble = textwrap.dedent("""
    = Lab notebook: BI Tool Project
    Maximilian Albert
    Version 0.1, started 13.2.2018
    :toc:
    :toclevels: 4
    :toc-title: Content
    :experimental:
    :description: Example AsciiDoc document
    :keywords: AsciiDoc
    :imagesdir: ./images

    """)


def replace_section_markers(line):
    """
    Replace any occurrences of '#' at the beginning of a line with '='.
    Return the (unchanged or modified) line.
    """
    m = re.match('^(#+) ', line)
    if m:
        line = re.sub('^(#+) ', '=' * len(m.group(1)) + ' ', line)
    return line


def replace_gh_flavoured_markdown_links(line):
    """
    Replace any hyperlinks in Github-flavoured markdown style with Asciidoc ones.
    """
    ghfm_link_pattern = '\[(.*?)\]\((.*?)\)'
    asciidoc_replacement_pattern = '\\2[\\1]'
    return re.sub(ghfm_link_pattern, asciidoc_replacement_pattern, line)


if __name__ == '__main__':
    try:
        filenames = sys.argv[1:]
        assert all([file.endswith('.md') for file in filenames])
    except IndexError:
        print("Usage: convert.py FILENAME.md [...]")
        sys.exit()

    with open(OUTFILE, 'w') as f:
        f.write(preamble)
        for infile in filenames:
            for line in open(infile, 'r').readlines():
                line = replace_section_markers(line)
                line = replace_gh_flavoured_markdown_links(line)
                f.write(line)
            f.write('\n\n<<<\n\n')

    print("Output successfully written to file: '{}'".format(OUTFILE))

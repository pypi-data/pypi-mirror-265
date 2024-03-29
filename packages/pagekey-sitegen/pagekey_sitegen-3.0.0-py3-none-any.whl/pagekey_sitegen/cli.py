import argparse
import os
import sys
from typing import List

from pagekey_sitegen.generator import SiteGenerator


class DocsDirNotFoundException(Exception):
    pass

def main(args_list: List[str] = sys.argv[1:]):
    parser = argparse.ArgumentParser(prog='pagekey-sitegen', description='Generate documentation site from directory.')
    subparsers = parser.add_subparsers(dest='command')

    build_parser = subparsers.add_parser('build', help='Build the site')
    build_parser.add_argument('docs_dir', metavar='docs_dir', type=str, help='The path to the documents directory')

    run_parser = subparsers.add_parser('run', help='Serve built docs site')

    args = parser.parse_args(args_list)
    
    if args.command == 'build':
        if not os.path.exists(args.docs_dir):
            raise DocsDirNotFoundException()
    
        SiteGenerator(args.docs_dir).generate()
    elif args.command == 'run':
        os.system('python3 -m http.server --directory build/html')

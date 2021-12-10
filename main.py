import argparse

from search_keyword_performace.process import process


def main():
    parser = argparse.ArgumentParser(description="Arg parser for search keyword performance")
    parser.add_argument('datafile', type=str, help="Path to input data file")
    args = parser.parse_args()
    process(args.datafile)


if __name__ == '__main__':
    main()

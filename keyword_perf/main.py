import argparse

from pyspark.sql import SparkSession

from keyword_perf.payload.processor import process


def main():
    parser = argparse.ArgumentParser(description="Arg parser for search keyword performance")
    parser.add_argument('datafile', type=str, help="Path to input data file")
    args = parser.parse_args()
    spark = SparkSession.builder.getOrCreate()
    process(args.datafile, spark)


if __name__ == '__main__':
    main()

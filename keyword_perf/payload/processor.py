from urllib.parse import urlparse, parse_qs

from pyspark.sql import functions as sql_functions
from pyspark.sql.types import StructType, StructField, StringType

from keyword_perf.payload.product_list_parser import ProductListParser


def process(data_file, spark):
    """
    The main process: takes the input file and does the following:
    1. Load data into a data frame
    2. Group by IP address, and collect events, products and referrers as lists
    3. Derive the final event, final product and initial referrer from lists
    4. Parse search engine data to find the search engine and keyword used
    5. Derive revenue from product data
    6. Calculate revenue for each search engine and keyword combination
    """
    raw_df = spark.read.csv(path=data_file, sep=r'\t', header=True)
    ip_grouped_df = group_by_ip(raw_df)
    summarized_df = summarize_events(ip_grouped_df)
    search_engine_df = parse_search_engine_data(summarized_df)
    revenue_df = search_engine_df \
        .withColumn('revenue',
                    sql_functions.when(search_engine_df.final_event == 1,
                                       get_revenue(search_engine_df.final_product)).otherwise(0))
    keyword_performance = revenue_df.groupby([revenue_df.search_engine, revenue_df.keyword])\
        .agg(sql_functions.sum(revenue_df.revenue).alias('revenue'))
    keyword_performance.show()


def group_by_ip(raw_df):
    """

    """
    return raw_df.groupby(raw_df.ip).agg(
        sql_functions.collect_list(raw_df.event_list).alias('event_list'),
        sql_functions.collect_list(raw_df.product_list).alias('product_list'),
        sql_functions.collect_list(raw_df.referrer).alias('referrer_list')
    )


def summarize_events(ip_grouped_df):
    """

    """
    return ip_grouped_df \
        .withColumn('final_product',
                    sql_functions.when(sql_functions.size(ip_grouped_df.product_list) > 0,
                                       sql_functions.element_at(ip_grouped_df.product_list, -1))) \
        .withColumn('final_event',
                    sql_functions.when(sql_functions.size(ip_grouped_df.event_list) > 0,
                                       sql_functions.element_at(ip_grouped_df.event_list, -1))) \
        .withColumn('search_referrer',
                    sql_functions.when(sql_functions.size(ip_grouped_df.referrer_list) > 0,
                                       sql_functions.element_at(ip_grouped_df.referrer_list, 1))) \
        .drop('event_list', 'product_list', 'referrer_list')


def parse_referrer(search_referrer):
    """

    """
    parsed_url = urlparse(search_referrer)
    queries = parse_qs(parsed_url.query)
    keyword = queries['q'][0] if 'q' in queries else queries['p'][0]
    return parsed_url.netloc, keyword.lower()


def parse_search_engine_data(summarized_df):
    """

    """
    referrer_data_schema = StructType([
        StructField("search_engine", StringType(), False),
        StructField("keyword", StringType(), False)
    ])
    udf_parse_referrer = sql_functions.udf(parse_referrer, referrer_data_schema)
    return summarized_df \
        .withColumn('search_parsed_values', udf_parse_referrer(summarized_df.search_referrer)) \
        .select(sql_functions.col('ip'), sql_functions.col('final_product'), sql_functions.col('final_event'),
                sql_functions.col('search_parsed_values.*'))


@sql_functions.udf
def get_revenue(product_string):
    """

    """
    return ProductListParser(product_string).total_revenue if product_string else 0

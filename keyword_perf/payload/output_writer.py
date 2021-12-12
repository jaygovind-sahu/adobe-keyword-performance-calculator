import pathlib


def write(keyword_performance_df, input_file_path):
    keyword_performance_df.show()
    in_path = pathlib.Path(input_file_path)
    out_path = in_path.parent.joinpath('..', 'output', 'SearchKeywordPerformance')
    keyword_performance_df.coalesce(1) \
        .write.partitionBy('process_date') \
        .csv(path=str(out_path), header=True)

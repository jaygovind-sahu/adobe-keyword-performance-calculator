import os

from keyword_perf.payload import processor

from tests.utils.pyspark_test_case import PySparkTestCase


class TestProcessor(PySparkTestCase):
    def setUp(self):
        sample_data_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'data.tsv')
        self.sample_data = self.spark.read.csv(path=sample_data_path, header=True, sep='\t')

    def test_group_by_ip(self):
        result = processor.group_by_ip(self.sample_data)
        self.assertEqual(result.count(), 4)
        result_ips = [row.ip for row in result.select('ip').collect()]
        self.assertListEqual(result_ips, ['44.12.96.2', '23.8.61.21', '67.98.123.1', '112.33.98.231'])

    def test_parse_referrer(self):
        parsed_data = processor.parse_referrer("http://www.google.com/search?hl=en&client=firefox-a&"
                                               "rls=org.mozilla%3Aen-US%3Aofficial&hs=Zk5&q=ipod&aq=f&oq=&aqi=g-p1g9|")
        self.assertTupleEqual(parsed_data, ('www.google.com', 'ipod'))

        parsed_data = processor.parse_referrer("http://www.bing.com/search?q=Zune&go=&form=QBLH&qs=n   ")
        self.assertTupleEqual(parsed_data, ('www.bing.com', 'zune'))

        parsed_data = processor.parse_referrer("http://search.yahoo.com/search?p=cd+player&toggle=1&cop=mss&"
                                               "ei=UTF-8&fr=yfp-t-701")
        self.assertTupleEqual(parsed_data, ('search.yahoo.com', 'cd player'))

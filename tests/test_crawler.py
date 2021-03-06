#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" pystockdb

  Copyright 2019 Slash Gordon

  Use of this source code is governed by an MIT-style license that
  can be found in the LICENSE file.
"""
import unittest

from pystockdb.tools.data_crawler import DataCrawler
from pystockdb.tools.fundamentals import Fundamentals


class TestCrawler(unittest.TestCase):

    SYMBOLS = ['OTCMKTS:ADDDF', 'OTCMKTS:BAYZF', 'OTCMKTS:BMWYY', 'NASDAQ:ADP', 'NASDAQ:BBBY']
    SYMBOLS_Y = ['ADDDF', 'BAYZF', 'BMWYY', 'ADP']

    def test_fundamentals(self):
        """
        Test stock fundamentals crawler
        :return:
        """
        fundamentals = Fundamentals(base_url=Fundamentals.BASE_URL)
        brief = fundamentals.get_company_brief('913261697')
        income = fundamentals.get_sheet('913261697', 1)
        balance = fundamentals.get_sheet('913261697', 2)
        cash_flow = fundamentals.get_sheet('913261697', 3)

        search_results = fundamentals.search('Adidas')
        self.assertIsNotNone(search_results)
        self.assertIn('tickerId', search_results[0])
        ads_id = search_results[0]['tickerId']
        income_2 = fundamentals.get_income_facts(ads_id)
        income_analyse = fundamentals.get_income_analysis(ads_id)
        recommendation = fundamentals.get_recommendation(ads_id)
        ticker = fundamentals.get_ticker_ids(TestCrawler.SYMBOLS)
        self.assertEqual(len(ticker), 5)
        self.assertTrue(
          any([symbol in ticker for symbol in TestCrawler.SYMBOLS])
        )
        self.assertTrue(
          any([income, balance, cash_flow, brief, income_2,
              income_analyse, recommendation, ticker])
        )

    def test_crawler(self):
        """
        Test stock data crawler
        :return:
        """
        crawler = DataCrawler(True)
        price = crawler.get_last_price('ADS.F')
        self.assertIsNotNone(price)
        price_stack = crawler.get_last_price_stack(TestCrawler.SYMBOLS_Y)
        self.assertTrue(
          any([symbol in price_stack and price_stack[symbol]
              for symbol in TestCrawler.SYMBOLS_Y])
        )
        ads_day = crawler.get_series('ADS.F', '1d')
        self.assertIsNotNone(ads_day)
        dax_day = crawler.get_series('DAX', '1d')
        self.assertIsNotNone(dax_day)
        dax_day = crawler.get_series_stack(['DAX'], '1d')
        self.assertIsNotNone(dax_day)


if __name__ == "__main__":
    unittest.main()

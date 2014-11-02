#!/usr/bin/env python

from __future__ import print_function

import argparse
import json


class PlusMinusCalculator:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Championship plus/minus')
        parser.add_argument('--file', '-f', required=True,
                            help='json input file')
        parser.add_argument('--debug', '-d', action='store_true',
                            help='json input file')
        self.args = parser.parse_args()
        self.load_data()

    def apply_delta(self, team, year, count, change):
        if self.args.debug:
            print("{} {} {:+}".format(team, year, change))

        return count + change

    def load_data(self):
        json_data = open(self.args.file)
        self.doc = json.load(json_data)
        json_data.close()

    def calculate(self):
        results = {}

        for team in self.doc['teams']:
            if 'end' not in self.doc['teams'][team]:
                count = 0
                last = "None"
                for year in sorted(self.doc['champions']):
                    if int(self.doc['teams'][team]['start']) <= int(year):
                        year_rec = self.doc['champions'][year]
                        if team == year_rec['winner']:
                            delta = int(year_rec['teams']) - 1
                            count = self.apply_delta(team, year, count, delta)
                            last = year
                        else:
                            count = self.apply_delta(team, year, count, -1)

                results[team] = {'team': self.doc['teams'][team]['name'],
                                 'result': count,
                                 'last': last}

        return results

    def print_results(self, results):
        print("{:25} {:6} {:8}".format('Team', 'Rating', 'Last Win'))
        print("{:25} {:6} {:8}".format('-' * 25, '-' * 6, '-' * 8))

        for team in sorted(results.items(), key=lambda x: x[1]['result'],
                           reverse=True):
            print("{:25} {:+6} {:^8}".format(team[1]['team'],
                                             team[1]['result'],
                                             team[1]['last']))

if __name__ == "__main__":
    c = PlusMinusCalculator()
    c.print_results(c.calculate())

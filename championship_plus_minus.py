#!/usr/bin/env python3

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

    def apply_delta(self, team, year, pm, change):
        if self.args.debug:
            print("{} {} {:+} {:+}".format(team, year, change, pm + change))

        return pm + change

    def load_data(self):
        json_data = open(self.args.file)
        self.doc = json.load(json_data)
        json_data.close()

    def get_years(self, team):
        champs = self.doc['champions']
        if 'prior' in self.doc['teams'][team]:
            prior = self.doc['teams'][team]['prior']
            champs = champs | self.doc[prior]

        return sorted(champs.items())

    def calculate(self):
        results = {}

        for team in self.doc['teams']:
            if 'end' not in self.doc['teams'][team]:
                pm = 0
                count = 0
                last = "None"
                for year_tuple in self.get_years(team):
                    year = year_tuple[0]
                    if 'exclude' in self.doc['teams'][team]:
                        if year in self.doc['teams'][team]['exclude']:
                            continue
                    if int(self.doc['teams'][team]['start']) <= int(year):
                        year_rec = year_tuple[1]
                        if team == year_rec['winner']:
                            delta = int(year_rec['teams']) - 1
                            pm = self.apply_delta(team, year, pm, delta)
                            last = year
                            count = count + 1
                        else:
                            pm = self.apply_delta(team, year, pm, -1)

                results[team] = {'team': self.doc['teams'][team]['name'],
                                 'result': pm,
                                 'count': count,
                                 'last': last}

        return results

    def print_results(self, results):
        print("{:25} {:6} {:8} {:4}".format('Team', 'Rating',
                                            'Last Win', 'Wins'))
        print("{:25} {:6} {:8} {:4}".format('-' * 25, '-' * 6,
                                            '-' * 8, '-' * 4))

        # First sort on name, then result
        name_sort = sorted(results.items(), key=lambda x: x[1]['team'])
        for team in sorted(name_sort, key=lambda x: x[1]['result'],
                           reverse=True):
            print("{:25} {:+6} {:^8} {:3}".format(team[1]['team'],
                                                  team[1]['result'],
                                                  team[1]['last'],
                                                  team[1]['count']))


if __name__ == "__main__":
    c = PlusMinusCalculator()
    c.print_results(c.calculate())

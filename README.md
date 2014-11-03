Championship Plus Minus
=======================
This is a simple Python script to calculate the deviation from expected value for a given sports team's history of winning (or not winning) championships.

In a 30 team sports league, a team is statistically expected to win one championship every 30 years.  A team that meets this expectation has a rating of 0, a team that exceeds this has a positive value, and a teams that lags has a negative rating.

As an example, in the 2014 MLB season in which 30 teams competed, the SF Giants won the World Series.  They received a credit of +29.  Every other team received a debit of -1.  The reason the credit is +29 instead of +30 is because it ensures the measure will have a result of 0 if this is the only win over 30 seasons.

Usage is very simple:
```
$ ./championship_plus_minus.py -f data/nhl.json
```
The tool is compatible with both python 2.7 and python 3.4.  Data files are in `data` and result files are in `results`.  The data files are in a presumably self-explanatory format to describe teams and championship winners.

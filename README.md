# Capital One Code \<FAM/\> Hackathon
Washington, DC (04-05 November 2017)

## Idea introduction
Parents will often be the first source of credit education for children. Using each transaction as a possible learning opportunity can benefit both parents and children. By taking an opportunity to provide lessons around the use of credit in a manner that parents -- and children -- can control, a family may better be able to understanding on what and how a credit card is being used.

This hack identifies a way for parents, through a Slack integration, to generate, on demand, information about children's spending and push the opportunity to provide eductional lessons to children.

## Setup
### Virtual environment
The `requirments.txt` include the Python libraries to load within the virtual environment. To setup the virtual environment, `virtualenv` and `virtualenvwrapper` must be installed. From there, the following can set up the virtual environment:
```
$ mkvirtualenv env
$ pip install -r requirements.txt
```

Note, however, there might be issues using the virtual environment, as this work calls `matplotlib`, which does not always have the best track record with virtualenvs. If that's the case, deactivate the virtual environment to run the work.

### Configuration file
There is a need for a configuration file in the top-level directory. It should have one header: `setup`. The field value for `setup` is:
```
n_family: ?
```

where the value is an integer and represents the number of household members to build a distribution around.

## How it works
This program makes use of the Capital One APIs made available during the hackathon to develop a distribution of spending for like-sized families to one's own. From there, a Slack integration (slash-command) will identify a specific user and focus on their spending or reward points for the previous three months. It will reduce the distribution of like-sized families to individuals that are +/- five years in age of the focal individual for a comparison against peers. From there, it will calculate the distribution of spending for the comparison peers, plot that as a density plot and then overlay the focal individual's spending for the month. This is done on a month-by-month basis for the three previous months from today.

The idea is that understanding where one falls against comparison peers provides parents an opportunity to discuss money and credit with adolescents. The discussion could focus around overall high spending or how a child is doing relatively better or worse than their peer group. In addition, each time the graph populates in the Slack channel, if the child is spending better or worse than their peer group (as determined by a provided cutoff), then an article from Capital One is displayed to help reinforce (in positive cases) or change (in negative cases) behavior.

Within Slack, the execution would be as follows:
```
/finknow 315890000 spend 100
```

where `315890000` represents the focal individual identifies, `spend` represents the category to investigate (the other being `reward`) and `100` is the threshold (+/- from the individual's amount) to determine how their behavior relates to the majority within the peer group.

## Future enhancements
This could be built out in a number of ways:

* Additional literature -- that is more specific -- could be shown within Slack
* This could be segmented further -- geography, spending type, etc.
* There could be more (or less) months shown
* Additional details on payment ability could be included.

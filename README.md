# Capital One Code \<FAM/\> Hackathon
Washington, DC (04-05 November 2017)

## Idea Introduction
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
There is a need for a configuration file in the top-level directory. It should have two headers: `setup` and `run`. The field value for `setup` is:
```
n_family: ?
```

and for `run`:
```
limit: ?
```

where both values are integers and represent the number of household members and the limit -- both above and below -- the maximally dense value of the spend/reward distribution of a given sample.

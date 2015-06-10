# KDDCup2015-CLI
An unofficial command line tool for KDD Cup 2015.

## Installation
```
$ pip install kddcup2015-cli
```

## Usage
Please accept the competition rules before your commands.


### Submit
To submit an entry.

```
$ kdd submit `entry` -u `username` -p `password` -m `message`
```

### Download
To download the data files.

```
$ kdd download -u `username` -p `password`
```

### Rank
To watch currant rank(default top10) from https://www.kddcup2015.com/submission-rank.html.

```
$ kdd rank
```

or watch top20

```
$ kdd rank -n 20
```

### Score
Watch your own scores(default top10) from https://www.kddcup2015.com/submission.html.

```
$ kdd score
```

or watch top5

```
$ kdd score -n 5
```

### Config
To set config.

```
$ kdd config -u `username` -p `password`
```

## Example
```
$ kdd submit sampleSubmission.csv -u USERNAME -p PASSWORD -m "Enter a brief description of this submission here."
```

or

```
$ kdd config -u USERNAME -p PASSWORD
$ kdd submit sampleSubmission.csv -m "Enter a brief description of this submission here."
```

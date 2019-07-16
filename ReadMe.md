# Brandmeister talkgroup search and converter tool for AnyTone radios

Currently supported radios are:

- AT-868
- AT-878 (tested)

## What it does

It allows you to:

- list and search Brandmeister talkgroups by country, name or ID
- create talk groups CSV files that you can import directly to your AnyTone radio

## What you need

The list of talk groups on Brandmeister in CSV format.

- Go to https://brandmeister.network/?page=talkgroups
- Select `Show "ALL" entries`
- Click the CSV button

Tip: The file name contains a lot of unecessary white spaces, I suggest to remove them entirely or to rename the file.

### Installation

Clone the repository and install the requirements: ` pip install -r requirements.txt`

Edit app.py to filter the talk groups you want. There are a few examples to get you started.

Run the app: `python3 app.py`

### Usage:

The brandmeister CSV file provided (TalkgroupsBrandMeister.csv) has been exported 13 july 2019. Use it for testing only and get a current CSV export from Brandmeister if you want fresh data.

Search is case insensitive.


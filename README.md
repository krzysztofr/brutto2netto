# Net salary calculator (Poland)

This simple script provides calculation of net salary when gross salary is given.
It in fact doesn't calculate much, just contacts website providing such information.

## Installation

It is recommended to install the script in `virtualenv`:

`virtualenv .env`
`.env/pip/install -r reqs.txt`

### Requirements

bs4, pycurl

### Running

Run `.env/bin/python b2n.py -h` to see the options.
Interactive mode allows you to type number and get the net values.
Other modes allow you to get values in specified format as an output. In such case, `amount` value is required.

## Disclaimer
I did it as sa handy tool to help in my daily work. I cannot guarantee it's accuracy.
Especially I cannot guarantee it's operation when the supplier changes the data format.
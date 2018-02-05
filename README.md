This is a parser library to scape Coned's account page to get account information. It can be used for creating IFTTT recipes that automatically add the current bill to a google drive or build an API to expose coned billing history.

# Installing

This library relies on phantomjs to do scraping. To install phantom.js:

```
npm -g install phantomjs-prebuilt
```

Then, install all requirements for the project. Best done on a virtualenv

```
pip install -r requirements.txt
```

# TODO

Start supporting historical APIs

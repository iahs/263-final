# 263-final

#### Jonah Kallenbach, Peter Kraft, Thomas Lively, Shai Szulanski

## Instructions

To run the penetration tester, run in the a Django root directory that contains xss_test.py and attackstrings.txt as well as Django's manage.py:

    python xss_test.py  URL [URL ...] [--query Query Strings [Query Strings ...]]

The URL argument is a list of subfolders within your site to attack (written without leading or trailing slashes).  The query keyword lets you optionally specify a list of query-string keywords to also attack on each of the attacked pages.

To run you must have Django and Selenium installed with an up-to-date Firefox for the Selenium webdriver.  To install Django and Selenium for Python, run:

    pip install selenium
    pip install Django

## Examples

The following examples demonstrate how the penetration tester finds vulnerabilities within the hackmelists webapp.

To test an exploit that bypasses Django's template sanitization by injecting into attributes, run:

    python xss_test.py /

To test injection vulnerabilities in query strings, run:

    python xss_test.py query --query name

To test injection vulnerabilities in text boxes, run;

    python xss_test.py list/text_box

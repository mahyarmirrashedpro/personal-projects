# Registration Form Information Extractor

The University of Manitoba chapter of the Institute of Electrical and Electronics Engineers (UMIEEE) held many workshops during the 2020-2021 fall and winter terms. Registration information from attendees was collected through Google Forms and automically pushed to a linked Google Sheets file.

## Main Problem

However, there was substantial hurdles to pulling meaningful stastistics or information aggregated throughout the workshops without getting far into the Google Sheets API and/or custom macros.

Some main issues were as follows:
* Viewing all proposed ideas for future UMIEEE workshops across all registration forms;
* Aggregating set (no repeats) of all participants' emails for advertising to join UMIEEE in subsequent year; and
* Calculating participant counts in each registration form to submit for future chapter funding.

## `extractor.py` Solution

By learning and incorporating the Python `argparse` library, flags for different program functions are able to be set without using complicated RegEx error checking on inputs.

Main program flags:
* `-f` specifies the CSV files to be processed;
* `-u` specifies results should be filtered on uniqueness (e.g. only show unique email addresses throughout all registrations); and
* `-m` specifies results should be filtered on member-only registrants.

Operation flags (mutually exclusive during single program instance):
* `-a` specifies to show attendance count;
* `-c` specifies to show comments; and
* `-e` specifies to show emails.

## Conclusion

With these program flags, `extractor.py` is able to effectively target and solve the problem at hand. Future iterations could include a graphical user interface (GUI) to make the program more accessible to users who are not familiar or proficient with command line programs.
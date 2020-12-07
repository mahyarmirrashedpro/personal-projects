# Imports
from argparse import ArgumentParser, FileType
from colorama import Fore
from os import getcwd, listdir
from os.path import basename
from sys import exit

# Helper functions
attendee_attributes = lambda: f'{"unique " if args.unique else ""}{"IEEE member " if args.membership else ""}'
error = lambda name: print(Fore.RED + f'"{name}" does not match header constraints.' + Fore.WHITE)
summary_title = lambda type: f'{" ".join([w.title() if w.islower() else w for w in attendee_attributes().split()])} {type.strip().title()} Summary'
wrap = lambda txt, char: f' {txt} '.center(100, char)

# Argument parser initialization
parser = ArgumentParser(description='Extract data from registration forms.', prog=basename(__file__).split('.')[0])
parser.add_argument('-f', '--files', help='CSV files to be processed.', nargs='*', type=FileType('r'))
parser.add_argument('-u', '--unique', action='store_true', help='return unique results.')
parser.add_argument('-m', '--membership', action='store_true', help='display member results only.')
operations = parser.add_mutually_exclusive_group(required=True)
operations.add_argument('-a', '--attendance', action='store_true', help='display attendance count.')
operations.add_argument('-c', '--comments', action='store_true', help='display list of comments.')
operations.add_argument('-e', '--emails', action='store_true', help='display list of emails.')
args = parser.parse_args()

# Load in csv files (as IOWrapper objects)
csvs = args.files if args.files else [open(file, mode='r', encoding='utf-8') for file in filter(lambda f: f.endswith('.csv'), listdir(getcwd()))]
if not csvs:
    exit('No CSV files found in current working directory!')

# Present analytics
tot_attendance = 0
tot_registrations = set()

# print summary name if unique
if args.unique:
    if args.comments:
        print(Fore.GREEN + wrap(summary_title('Comments'), '*') + Fore.WHITE)
    elif args.emails:
        print(Fore.GREEN + wrap(summary_title('Emails'), '*') + Fore.WHITE)

# process each csv in list of csvs
for csv in sorted(csvs, key=lambda csv: csv.name):
    # store title of csv
    title = csv.readline().strip().split(',')[0].strip()
    # perform header checks
    header = csv.readline().strip().split(',')
    if header[4].strip().lower() != 'preferred email':
        error(title)
        continue
    elif header[5].strip().lower() != 'are you an ieee member?':
        error(title)
        continue
    elif header[-2].strip().lower() != 'what workshops would you like to see in the future?':
        error(title)
        continue
    # print title of csv if not counting uniques
    if not args.unique:
        print(Fore.GREEN + wrap(title, '-') + Fore.WHITE)

    # keep track of attendance in file
    cur_attendance = 0

    # process each line in file
    for line in csv:
        # pre-emptively strip and split each line
        parts = [part.strip() for part in line.strip().split(',')]
        # only check flags in valid scenarios of membership flag
        if not args.membership or (args.membership and parts[5].lower() == 'yes'):
            if not args.unique or (args.unique and parts[4] not in tot_registrations):
                tot_registrations.add(parts[4])
                # attendance clause check done at end of each file
                cur_attendance += 1
                if args.comments and (comment := parts[-2]) != '':
                    print(f'> {comment}')
                elif args.emails:
                    print(parts[4])
    # print current attendance if necessary
    if args.attendance and not args.unique:
        print(f'There were {cur_attendance} {attendee_attributes()}attendees.')
    # add current attendance to total attendance
    tot_attendance += cur_attendance

# print total attendance if necessary
if args.attendance:
    print(Fore.GREEN + wrap('Registration Attendance Summary', '*') + Fore.WHITE)
    print(f'Among all registrations, there were a total of {tot_attendance} {attendee_attributes()}attendees.')

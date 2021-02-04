#------------------------------------------------------------------------------
# IMPORTS
#------------------------------------------------------------------------------

from argparse import ArgumentParser, FileType
from os import getcwd, listdir
from os.path import basename
import pandas as pd
from sys import exit

#-----------------------------------------------------------------------------
# CONSTANTS
#-----------------------------------------------------------------------------

required_headers = [
    'preferred email',
    'are you an ieee member?',
    'would you like a copy of the slides after the workshop?',
    'what workshops would you like to see in the future?'
]

#------------------------------------------------------------------------------
# HELPER LAMBDA FUNCTIONS
#------------------------------------------------------------------------------

attributes = lambda: f'{"unique " if args.unique else ""}{"IEEE member " if args.membership else ""}'
summary_title = lambda type: f'{" ".join(attr.title() for attr in attributes().split())} {type.strip().title()} Summary'
wrap = lambda txt, char: f' {txt} '.center(100, char)

#------------------------------------------------------------------------------
# FUNCTIONS
#------------------------------------------------------------------------------

def validate_registration_table(df: pd.DataFrame, title: str) -> None:
    for i, header in enumerate(required_headers, start=1):
        assert header in df.columns, f'ERROR ({i:02}): "{title}" does not match header constraints.'

#------------------------------------------------------------------------------
# MAIN PROGRAM START
#------------------------------------------------------------------------------

###############################################################################
# ARGUMENT PARSER INITALIZATION
###############################################################################

parser = ArgumentParser(description='Extract data from registration forms.', prog=basename(__file__).split('.')[0])
parser.add_argument('-f', '--files', help='TSV files to be processed.', nargs='*', type=FileType('r'))
parser.add_argument('-u', '--unique', action='store_true', help='return unique results.')
parser.add_argument('-m', '--membership', action='store_true', help='display member results only.')
parser.add_argument('-s', '--slides', action='store_true', help='return slide requesting attendees')
parser.add_argument('-ie', '--ignore_errors', action='store_true', help='ignore invalidated files')
operations = parser.add_mutually_exclusive_group(required=True)
operations.add_argument('-a', '--attendance', action='store_true', help='display attendance count.')
operations.add_argument('-c', '--comments', action='store_true', help='display list of comments.')
operations.add_argument('-e', '--emails', action='store_true', help='display list of emails.')
args = parser.parse_args()

###############################################################################
# LOAD TSVs
###############################################################################

# load files from argument parser
tsvs = args.files
# if none specified, load all files in current working directory
if not tsvs:
    tsvs = [open(file, mode='r', encoding='utf-8') for file in listdir(getcwd())]
# filter to ensure all items are tsv files
tsvs = filter(lambda f: f.name.endswith('.tsv'), tsvs)
# ensure at least single tsv inside list
if not tsvs:
    exit('No TSV files found in current working directory!')

###############################################################################
# BEGIN ANALYSIS
###############################################################################

cumulative_attendance = 0
registrations = set()

# print summary title if showing unique values
if args.unique:
    if args.comments:
        print(wrap(summary_title('Comments'), '*'))
    elif args.emails:
        print(wrap(summary_title('Emails'), '*'))

# process each tsv alphanumerically
for tsv in sorted(tsvs, key=lambda tsv: tsv.name):

    title = tsv.readline().strip()

    # validate table with header checks
    try:
        df = pd.read_csv(
            tsv,
            sep='\t',
            header=0,
            true_values=['Yes'],
            false_values=['No', 'No, I have never heard of IEEE']
        )

        df.columns = df.columns.str.strip().str.lower()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        validate_registration_table(df, title)
        df['preferred email'] = df['preferred email'].str.lower()
        
    except AssertionError as e:
        if not args.ignore_errors:
            print(e, 'Continuing...')
        continue

    # print title of tsv if not counting uniques
    if not args.unique:
        print(wrap(title, '-'))
    
    for index, row in df.iterrows():
        if not args.membership or (args.membership and row['are you an ieee member?']):
            if not args.unique or (args.unique and row['preferred email'] not in registrations):
                registrations.add(row['preferred email'])
                if args.comments and not pd.isnull(row['what workshops would you like to see in the future?']):
                    print(f"> {row['what workshops would you like to see in the future?']}")
                elif args.emails:
                    if row['would you like a copy of the slides after the workshop?'] or not args.slides:
                        print(row['preferred email'])
    
    # print current attendance if requested
    if args.attendance and not args.unique:
        print(f'There were {len(df.index)} {attributes()}attendees.')
    
    cumulative_attendance += len(df.index)

# print total attendance if selected
if args.attendance:
    print(wrap('Registration Attendance Summary', '*'))
    print(f'Among all registrations, there were a total of {cumulative_attendance} {attributes()}attendees.')

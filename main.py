import pandas as pd

# List all files in same directory as script
# Could rename to something more meaningful as the filenames
# will appear in the final output.
# run python main.py in terminal to produce output
FILES = [
    'GMT20230324-194446_Recording.transcript.vtt',
    'GMT20230322-230356_Recording.transcript.vtt'
]

# Make sure all of our names are removed
NAMES_TO_SKIP = [
    'Avani Guduri',
    'Cindy Liu', 
    'Jialin Ye',
    'Conrad Borchers'
]

def process_file(f):
    with open(f, 'r') as file:
        lines = [line.rstrip() for line in file]

    # Remove 2 lines preamble
    lines = lines[2:]

    # Sequences are always Number, Time, Name: Speech, Blank
    times, speakers, contents = [], [], []
    for i, line in enumerate(lines):
        if i%4 in [0, 3]:
            continue
        if i%4 == 1:
            times.append(line)
        else:
            elements = line.split(':', 1)
            if len(elements) == 1:
                speakers.append('UNKNOWN')
                contents.append(elements[0])
            else:
                speakers.append(elements[0])
                contents.append(elements[1])

    df = pd.DataFrame({
        'file': [f for _ in range(len(times))],
        'time': times,
        'speaker': speakers,#['Speaker ' + str(hash(s)) for s in speakers], # Anonymizing
        'content': contents
    })

    # Remove conductor and unknown speakers from analysis
    df = df[~df['speaker'].isin(NAMES_TO_SKIP + ['UNKNOWN'])].copy()

    return df

# Export
pd.concat([process_file(f) for f in FILES]).to_csv('transcripts.csv', index = False)

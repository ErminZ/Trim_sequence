import re

exclude_names = set()
trim_names = {}


EXCLUDE_PATTERN = '^Exclude:'
TRIM_PATTERN = '^Trim:'
with open('D:\Xiaolab\SPAdesErmin\SPAdes_127/Contamination_L9.txt','r') as fixup_file:
    in_exclude = False
    in_trim = False
    iterlines = iter(fixup_file.readlines())
    try:
        for line in iterlines:

            if not line.strip():
                continue

            if re.match(EXCLUDE_PATTERN, line):
                in_exclude = True
                _ = next(iterlines)  # Throw out header
                continue

            if re.match(TRIM_PATTERN, line):
                # Assume that "Trim" appears after "Exclude"
                in_trim = True
                in_exclude = False
                _ = next(iterlines)  # Throw out header (seq. name, length, span(s))
                continue

            if in_exclude:
                sequence_name = line.split('\t')[0]  # Split on tab character.
                exclude_names.add(sequence_name)

            if in_trim:
                sequence_name, _, span, _ = line.split('\t')
                trim_names[sequence_name] = span
    except:
        print(line)
        raise


# 2: Open new file to write results to.
# 3: Read lines in "L.reu..." and write the ones you want to keep.
with open('D:\Xiaolab\SPAdesErmin\SPAdes_127\L9_fixed.fasta', 'w') as outfile, open('D:\Xiaolab\SPAdesErmin\SPAdes_127\L9\scaffolds.fasta', 'r') as infile:
    in_exclude = None
    iter_infile = iter(infile.readlines())
    for line in iter_infile:
        if line.startswith('>'):
            in_exclude = False
            sequence_name = line.lstrip('>').strip()
            if sequence_name in exclude_names:
                print('Removing:', sequence_name)
                in_exclude = True
                continue

        if in_exclude:
            continue

        outfile.write(line)
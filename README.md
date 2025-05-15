# FID Spam Label Checker

This script checks a list of FIDs (Farcaster IDs) against a public spam dataset and saves the matching results to a CSV file. It includes label descriptions, status interpretation, and human-readable timestamps.

## Features

- Reads FIDs from a local file (`fid.txt`)
- Downloads spam label data from a public URL (in JSONL format)
- Matches records by FID
- Interprets label values with human-readable descriptions
- Converts UNIX timestamps to UTC datetime format
- Outputs results to a CSV file (`spam_results.csv`) with Cyrillic compatibility (UTF-8 with BOM)
- Prints summary statistics in the console

1. Clone the repository or download the files:
```bash
   git clone https://github.com/encipher88/farcaster_spam_detect.git
   cd farcaster_spam_detect
```
   Alternatively, download this repository as a ZIP and extract it.

2. Create the fid.txt file:

   Create a file named fid.txt in the project directory and list one FID per line:
```bash
   123400
   567800
   901200
```
3. Install dependencies:

   Make sure you're in the project directory and run:
```bash
   pip install requests
```
4. Run the script:
```bash
   python spam_finder.py
```
5. Check the output:

   After execution, the results will be saved to spam_results.csv.

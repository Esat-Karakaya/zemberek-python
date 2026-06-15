import sys
from pathlib import Path
import logging

# Add the parent directory to sys.path to allow importing from the root
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from custom_tokenizer.morph_tokenizer import MorphTokenizer

# Configure logging to hide noisy library messages
logging.basicConfig(level=logging.ERROR)

def run_decode_encode_test():
    xlsx_path = Path(__file__).parent / "TurkishTweets.xlsx"
    
    if not xlsx_path.exists():
        print(f"Error: Could not find TurkishTweets.xlsx at {xlsx_path}")
        sys.exit(1)
        
    print(f"Reading Excel file: {xlsx_path.name}...")
    try:
        df = pd.read_excel(xlsx_path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        print("Please ensure that 'pandas' and 'openpyxl' are installed in your environment.")
        print("To install them, run:")
        print("  ./.venv/bin/pip install pandas openpyxl")
        sys.exit(1)

    # Dynamically find the tweet column (case-insensitive check for 'tweet')
    tweet_col = None
    for col in df.columns:
        if "tweet" in str(col).lower():
            tweet_col = col
            break

    if tweet_col is None:
        tweet_col = df.columns[0]
        print(f"Could not find a column named 'Tweets'. Using the first column: '{tweet_col}'")
    else:
        print(f"Using column: '{tweet_col}'")

    print("Initializing MorphTokenizer...")
    tokenizer = MorphTokenizer("<|", "|>")
    
    mismatches = []
    total_count = 0
    success_count = 0

    print(f"Processing {len(df)} rows for the encode-decode round-trip test...")

    for idx, row in df.iterrows():
        original_tweet = row[tweet_col]
        if pd.isna(original_tweet):
            continue
            
        original_tweet = str(original_tweet)
        total_count += 1
        
        try:
            # Tokenize (Encode)
            tokens = tokenizer.tokenize(original_tweet)
            # Detokenize (Decode)
            decoded_tweet = tokenizer.detokenize(tokens)
            
            if decoded_tweet == original_tweet:
                success_count += 1
            else:
                mismatches.append({
                    "row": idx + 2,  # 1-based index, account for header row (+2)
                    "original": original_tweet,
                    "decoded": decoded_tweet,
                    "tokens": tokens
                })
        except Exception as e:
            mismatches.append({
                "row": idx + 2,
                "original": original_tweet,
                "error": str(e)
            })

    # Output test summary
    print("\n" + "="*40)
    print("           TEST RESULTS SUMMARY           ")
    print("="*40)
    print(f"Total tweets processed:  {total_count}")
    print(f"Successful round-trips:  {success_count}")
    print(f"Failed round-trips:      {len(mismatches)}")
    if total_count > 0:
        success_rate = (success_count / total_count) * 100
        print(f"Success Rate:            {success_rate:.2f}%")
    print("="*40)

    # Print first few failures if any exist
    if mismatches:
        print(f"\nShowing up to the first 10 mismatches out of {len(mismatches)} total failures:")
        for i, m in enumerate(mismatches[:10]):
            print(f"\nMismatch #{i+1} (Excel Row {m['row']}):")
            print(f"  Original:  {repr(m['original'])}")
            if "error" in m:
                print(f"  Error:     {m['error']}")
            else:
                print(f"  Decoded:   {repr(m['decoded'])}")
                print(f"  Tokens:    {m['tokens']}")
    else:
        print("\nAll tweets successfully passed the encode-decode round-trip test!")

    # Write all failures to log file
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file_path = logs_dir / "failed_tests.log"
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_file_path, "w", encoding="utf-8") as f:
        f.write("="*80 + "\n")
        f.write(f"ENCODE-DECODE ROUND-TRIP TEST LOG - {timestamp}\n")
        f.write("="*80 + "\n")
        f.write(f"Total tweets processed:  {total_count}\n")
        f.write(f"Successful round-trips:  {success_count}\n")
        f.write(f"Failed round-trips:      {len(mismatches)}\n")
        if total_count > 0:
            success_rate = (success_count / total_count) * 100
            f.write(f"Success Rate:            {success_rate:.2f}%\n")
        f.write("="*80 + "\n\n")
        
        if mismatches:
            f.write("DETAILED FAILURES:\n")
            f.write("-"*80 + "\n")
            for idx, m in enumerate(mismatches):
                f.write(f"Failure #{idx+1} (Excel Row {m['row']}):\n")
                f.write(f"  Original:  {repr(m['original'])}\n")
                if "error" in m:
                    f.write(f"  Error:     {m['error']}\n")
                else:
                    f.write(f"  Decoded:   {repr(m['decoded'])}\n")
                    f.write(f"  Tokens:    {m['tokens']}\n")
                f.write("-"*80 + "\n")
        else:
            f.write("All tests passed successfully! No mismatches found.\n")

    print(f"\nFailing tests and details written to: {log_file_path}")

if __name__ == "__main__":
    run_decode_encode_test()

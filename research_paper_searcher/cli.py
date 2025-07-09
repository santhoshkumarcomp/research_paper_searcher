# cli.py
import argparse
from pubmed.fetch import get_pubmed_csv 
import csv
def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma-affiliated authors.")
    
    parser.add_argument("query", help="Search query for PubMed articles")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-f", "--file", help="Output CSV filename (default: print to console)")

    args = parser.parse_args()

    # Access arguments like:
    search_query = args.query
    debug_mode = args.debug
    filename = args.file

    if debug_mode:
        print(f"🔍 Query: {search_query}")
        print(f"📁 Output File: {filename or 'stdout'}")

    output = get_pubmed_csv(search_query)
    with open(f"{filename}", "w", encoding="utf-8") as f:
      f.write(output)
      
if __name__ == "__main__":
    main()

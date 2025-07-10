from flask import Flask,request, jsonify,Response
import requests
import xmltodict
import io
import csv
import re

def get_pubmed_csv(search):
  response = requests.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search}')
    
  if response.status_code == 200:
      data = response.content
      parsed_data = xmltodict.parse(data)
      val =[]
      for value in parsed_data["eSearchResult"]["IdList"].values():
          # print(f"{value}")
          val = [*value]
          # print(type(val))
          # print(val)
      
      
      ids = ",".join(val)
      url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
      params = {
          "db": "pubmed",
          "id": ids,
          "retmode": "xml"
          }
      response = requests.get(url, params=params)
      data = xmltodict.parse(response.content) 
      def is_Academic(affiliation):
          keywords = ["university","college","institute"]
          clean_affiliation = re.sub(r'[^\w\s]', '', affiliation).lower()
          return any(keyword in clean_affiliation for keyword in keywords)
      def is_pharma_affiliation(affiliation):
        keywords = ["pharma", "biotech", "therapeutics", "laboratories", "inc", "corp", "company"]
        clean_affiliation = re.sub(r'[^\w\s]', '', affiliation).lower()
        return any(keyword in clean_affiliation for keyword in keywords)
      def email_extract(affiliation):
          email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
          emails = re.findall(email_pattern,affiliation)
          print(emails)
          return emails
      def match_author_to_email(aut, email):
        au = aut.split(',')
        if len(au) < 2:
            return False  # malformed name
        
        last = au[0].strip().lower()     # "doe"
        first = au[1].strip().lower()    # "john"
        first_initial = first[0] if first else ''

        email = email.lower()

        # Create common match patterns
        patterns = [
            f"{first}{last}",        # john.doe
            f"{first}.{last}",
            f"{first}_{last}",
            f"{first_initial}{last}",  # jdoe
            f"{last}{first_initial}",  # doej
            last,                    # just last name
        ]

        # Check if any pattern appears in the email
        for pattern in patterns:
            if pattern in email:
                return True

        return False
      result = []
      row = []
      auths = []
      email = []
      e =[]
      articles = data['PubmedArticleSet']['PubmedArticle']
      if not isinstance(articles, list):
          articles = [articles]

      for article in articles:
          article_meta = article.get('MedlineCitation', {}).get('Article', {})
          author_list = article_meta.get('AuthorList')

          if not author_list:
              print("No authors found for this article.")
              continue

          authors = author_list.get('Author')
          if not authors:
              print("Author key missing inside AuthorList.")
              continue

          if not isinstance(authors, list):
              authors = [authors]  # Normalize single author to list

          for author in authors:
              last = author.get('LastName', '')
              fore = author.get('ForeName', '')
              name = f"{last}, {fore}".strip(", ")

              affil_info = author.get('AffiliationInfo')

              # Case: No affiliation
              if not affil_info:
                  affiliation = "N/A"

              # Case: Single dict
              elif isinstance(affil_info, dict):
                  affiliation = affil_info.get('Affiliation', 'N/A')

              # Case: List of dicts
              elif isinstance(affil_info, list):
                  affiliation = affil_info[0].get('Affiliation', 'N/A')

              else:
                  affiliation = "N/A"


              # print(f"{name} — {affiliation}")
              
              if is_pharma_affiliation(affiliation):
                  result.append(article)
                  pmid = article['MedlineCitation'].get('PMID', {}).get('#text', 'N/A')
                  title = article['MedlineCitation'].get('Article', {}).get('ArticleTitle','N/A')
                  if isinstance(title,dict):
                      title1 = title.get('#text', 'N/A')
                  else:
                      title1 = title
                  journal = article['MedlineCitation'].get('Article', {}).get('Journal', {})
                  journal_issue = article['MedlineCitation'].get('Article',{}).get('Journal', {}).get('JournalIssue',{})
                  jtitle = journal.get('Title', 'N/A')
                  date  = journal_issue.get('PubDate','N/A')
                  Day = date.get('Day','N/A')
                  Month = date.get('Month','N/A')
                  Year = date.get('Year','N/A')
                  d = f'{Day}-{Month}-{Year}'
                  
                  if not is_Academic(affiliation):
                      auths.append(name)
                  emails = email_extract(affiliation)
                  a = (",").join(auths)
                  if(emails):
                      for aut in auths:
                        au = aut.split(',')
                        for email in emails:
                          if match_author_to_email(aut,email):
                              e.append(email)
                      row.append([pmid, title1,jtitle,d,a,(',').join(e)])
                  else:
                      row.append([pmid, title1,jtitle,d,a])
                  
                  break
      
      output = io.StringIO()
      writer = csv.writer(output)
      writer.writerow(["PubmedID", "Title", "Journal", "Publication Date", "Non-academic Author(s)","emails"])
      writer.writerows(row)

      # Move to the beginning of the file
      output.seek(0)

      return output.getvalue()

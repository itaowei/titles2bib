# coding:utf-8
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}

requests.packages.urllib3.disable_warnings()

# search for paper's bibtex URL with the title
# title is a string. e.g. "Reducing Human Effort and Improving Quality in Peer Code Reviews Using Automatic Static Analysis and Reviewer Recommendation"
def search_for(title):
    # search for paper with the title
    url = 'https://dblp.org/search?q='+title 
    
    # get the content from the webpage
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")

    # navigate to the URL corresponding to the second icon in the 1st searched result
    res = soup.select('.publ > ul > li > div > a')
    # print res[1]
    # print type(res[1])
    if len(res) < 2:
        return False
    bibtex_str = res[1]
    res = bibtex_str.get('href')
    # print res
    if 'bibtex' not in res:
        return False
    return res

# get the bibtex information from the web page of URL
# url is a string. e.g. "https://dblp.org/rec/conf/icse/Balachandran13.html?view=bibtex"
def get_bibtex(url, style):
    r= requests.get(url+"&param="+str(style), headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    res = soup.select('#bibtex-section > pre')
    # print(res[0].get_text())
    return res[0].get_text()

if  __name__ == '__main__':
    # get parameters
    parser = argparse.ArgumentParser(description='BibTex Unification of Papers Based on dblp Titles Index')
    parser.add_argument("-in","--input", dest="input_file_path", metavar="papers_titles.csv",
                        help='the path of the input file including papers\' titles', required = True)
    parser.add_argument("-out","--output", dest="output_file_path", metavar="references.bib",
                        help='the path of the output file including papers\' BiTex', required = True)
    parser.add_argument("-m","--mode", dest="output_file_mode", metavar="w", default="w",
                        help='mode you want to open the output file', required = False)
    parser.add_argument("-s","--style", dest="style_of_BibTex", metavar=0, type = int, default=1,
                        help='style of the BibTex, 0: standard; 1: condensed; 2: more condensed', required = False)
    args = parser.parse_args()
    

    file_input_path = args.input_file_path # The path and name of the file e.g. "D:/input.csv"
    file_output_path = args.output_file_path # The path and name of the file e.g. "D:/bibtex.bib"
    mode = args.output_file_mode  # A string, define which mode you want to open the file in:
                # "a" - Append - Opens a file for appending, creates the file if it does not exist
                # "w" - Write - Opens a file for writing, creates the file if it does not exist
                # "x" - Create - Creates the specified file, returns an error if the file exist
    style_n = args.style_of_BibTex # 0: standard; 1: condensed; 2: more condensed (delete string between 'DBLP:' and the 2nd '/' after that)
    if style_n == 1 or style_n == 2:
        style = 0
    else:
        style = 1
        
    # get titles' names
    file = pd.read_csv(file_input_path, encoding = 'utf-8')
    df = pd.DataFrame(file)

    output_file = open(file_output_path, mode)

    n_cmplt, n_fail = 0, 0
    cmplt, fail =[], []

    # search each of titles' names
    for i in df["Title"]:
        print("=== start searching for " + i + " ===")
        url = search_for(i)
        print(url)
        if url != False:
            n_cmplt+=1
            cmplt.append(i)
            bibtex_info = get_bibtex(url,style)
            if style_n == 2: # make BibTex more condensed
                bibtex_info = re.sub('DBLP:[^/]+/[^/]+/', "", bibtex_info, count=1)# delete string between 'DBLP:' and the 2nd '/' after that
            print(bibtex_info)
            output_file.write(bibtex_info)
            print("=== completed searching for " + i + " ===\n")
        else:
            n_fail+=1
            fail.append(i)
            print("===  Sorry! it failed searching for " + i + " ===\n")

    output_file.close()
    
    # output results of search
    print("*"*28)
    if n_cmplt == 0:
        print("No paper can be handled by their titles.")
    elif n_cmplt == 1:
        print(str(n_cmplt) + " paper can be handled by their titles.")
    else:
        print(str(n_cmplt) + " papers can be handled by their titles.")
    if n_fail == 1:
        print(str(n_fail) + " paper cannot be handled including:")
    elif n_fail > 1:
        print(str(n_fail) + " papers cannot be handled including:")
    if n_fail >= 1:
        for i in fail:
            print(i)

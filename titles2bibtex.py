# coding:utf-8
import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

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

    parser = argparse.ArgumentParser(description='BibTex Unification of Papers Based on dblp Titles Index')
    parser.add_argument("-in","--input", dest="input_file_path", metavar="papers_titles.csv",
                        help='the path of the input file including papers\' titles', required = True)
    parser.add_argument("-out","--output", dest="output_file_path", metavar="references.bib",
                        help='the path of the output file including papers\' BiTex', required = True)
    parser.add_argument("-m","--mode", dest="output_file_mode", metavar="w", default="w",
                        help='mode you want to open the output file', required = False)
    parser.add_argument("-s","--style", dest="style_of_BibTex", metavar=0, type = int, default=0,
                        help='style of the BibTex, 0: condensed; 1: standard', required = False)

    args = parser.parse_args()
    ################### Edit Here ###################

    file_input_path = args.input_file_path # The path and name of the file e.g. "D:/input.csv"
    file_output_path = args.output_file_path # The path and name of the file e.g. "D:/bibtex.bib"
    mode = args.output_file_mode  # A string, define which mode you want to open the file in:
                # "a" - Append - Opens a file for appending, creates the file if it does not exist
                # "w" - Write - Opens a file for writing, creates the file if it does not exist
                # "x" - Create - Creates the specified file, returns an error if the file exist
    style = args.style_of_BibTex # 0: condensed; 1: standard

    ################### Edit Here ###################

    file = pd.read_csv(file_input_path, encoding = 'utf-8')
    df = pd.DataFrame(file)

    output_file = open(file_output_path, mode)

    n_cmplt, n_fail = 0, 0
    cmplt, fail =[], []

    for i in df["Title"]:
        print("=== start ===")
        print(i)
        url = search_for(i)
        print(url)
        if url != False:
            n_cmplt+=1
            cmplt.append(i)
            bibtex_info = get_bibtex(url,style)
            print(bibtex_info)
            output_file.write(str(bibtex_info))
            output_file.write('\n')
            print("=== completed ===")
        else:
            n_fail+=1
            fail.append(i)
            print("Sorry! "+ i +" cannot be dealt with (")
            print("===  failed  ===")

    output_file.close()
    print("*"*10)
    print(str(n_cmplt) + " papers can be handled by their titles.")
    print(str(n_fail) + " papers cannot be handled including:")
    for i in fail:
        print(i)

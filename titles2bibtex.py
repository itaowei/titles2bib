# coding:utf-8
from tqdm import tqdm
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


def search_for_conference_or_journal(keywords):

    search_url = "https://dblp.org/search?q={}".format(keywords)

    # get the content from the webpage
    content = requests.get(search_url, headers=header, timeout=12999, verify=False)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, "lxml")

    # navigate to the URL in the 1st searched result
    res = soup.select('.result-list > li > a')
    if len(res) < 1:
        return False
    best_match = res[0]
    list_url = best_match.get('href')
    if 'https://dblp.org' not in list_url:
        return False
    print("Selected {}".format(best_match.get_text()))
    return best_match.get_text(), list_url


def search_for_list_url(conference_or_journal_url, recent_n):

    content = requests.get(conference_or_journal_url, headers=header, timeout=12999, verify=False)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, "lxml")

    res = soup.select('#main > ul > li > a')
    if len(res) < 1:
        res = soup.select('#main > ul > li > cite > a')
        if len(res) < 1:
            return False
    paper_list_urls = list()
    for url_block in res:
        url = str(url_block.get('href'))
        if url.find("https://dblp.org/db/journals") != -1 or url.find("https://dblp.org/db/conf") != -1:
            paper_list_urls.append(url)
    return paper_list_urls[:recent_n]


def matched_title_and_total_papers_num(paper_list_url, include_keywords=None):

    content = requests.get(paper_list_url, headers=header, timeout=12999, verify=False)
    content.encoding = "utf-8"
    soup = BeautifulSoup(content.text, "lxml")

    res = soup.select('.publ-list > li')
    if len(res) < 1:
        return False
    papers_title = [i.select("cite > .title")[0].get_text() for i in res]
    # papers_bibtex = [get_bibtex(i.select("div > a")[1].get('href')) for i in tqdm(res)]
    matched_titles = {keyword:list() for keyword in include_keywords}
    with tqdm(total=len(papers_title),desc=paper_list_url) as pbar:
        for index, title in enumerate(papers_title):
            # pbar.set_description("{}...".format(title[:20]))
            title_word_list = re.findall(r"[\w']+|[.,!?;]", title)
            title_word_list_lowercase = [word.lower() for word in title_word_list]
            for keyword in include_keywords:
                if keyword.lower() in title_word_list_lowercase:
                    bibtex = None
                    for url_block in res[index].select("div > a"):
                        if url_block.get('href').find("https://dblp.org/rec/{}".format("/".join(paper_list_url.split("/")[-3:-1]))) != -1:
                            bibtex = get_bibtex(url_block.get('href'))
                    matched_titles[keyword].append({"title":title,"bibtex":bibtex})
            pbar.update(1)

    return matched_titles,len(papers_title)



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
    if len(res) < 2:
        return False
    bibtex_str = res[1]
    res = bibtex_str.get('href')
    if 'bibtex' not in res:
        return False
    return res

# get the bibtex information from the web page of URL
# url is a string. e.g. "https://dblp.org/rec/conf/icse/Balachandran13.html?view=bibtex"
# style is an int. -1: more condensed, 0: condensed, 1: standard, 2: with crossref
def get_bibtex(url, style=0):
    r= requests.get(url+"&param="+str(style), headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    res = soup.select('#bibtex-section > pre')
    try:
        bibtex_info = res[0].get_text()
    except:
        print("ERROR:",url, res)
        return None
    if style == -1:
        bibtex_info = re.sub('DBLP:[^/]+/[^/]+/', "", bibtex_info, count=1)# delete string between 'DBLP:' and the 2nd '/' after that
    if len(re.findall("= {CoRR}",bibtex_info)) == 1:
        volume_content = bibtex_info.split("\n  volume ")[1].strip().split("{")[1].strip().split("}")[0]
        if volume_content.split("/")[0] == 'abs':
            bibtex_info = re.sub('= {CoRR}', "= {arXiv Preprint}", bibtex_info, count=1)
            bibtex_info = re.sub('\n  volume ', "\n  url    ", bibtex_info, count=1)
            bibtex_info = re.sub(volume_content, "https://arxiv.org/abs/{}".format(volume_content.split("/")[1]), bibtex_info, count=1)
    return bibtex_info

if  __name__ == '__main__':
    # get parameters
    parser = argparse.ArgumentParser(description='BibTex Unification of Papers Based on dblp Titles Index')
    parser.add_argument("-in","--input", dest="input_file_path", metavar="papers_titles.csv",
                        help='the path of the input file including papers\' titles', required = True)
    parser.add_argument("-out","--output", dest="output_file_path", metavar="references.bib",
                        help='the path of the output file including papers\' BiTex', required = True)
    parser.add_argument("-m","--mode", dest="output_file_mode", metavar="w", default="w",
                        help='mode you want to open the output file', required = False)
    parser.add_argument("-s","--style", dest="style_of_BibTex", metavar=0, type = int, default=-1,
                        help='style of the BibTex, -1: more condensed (delete string between \'DBLP:\' and the 2nd \'/\' after that), 0: condensed, 1: standard, 2: with crossref', required = False)
    args = parser.parse_args()
    

    file_input_path = args.input_file_path # The path and name of the file e.g. "D:/input.csv"
    file_output_path = args.output_file_path # The path and name of the file e.g. "D:/bibtex.bib"
    mode = args.output_file_mode  # A string, define which mode you want to open the file in:
                # "a" - Append - Opens a file for appending, creates the file if it does not exist
                # "w" - Write - Opens a file for writing, creates the file if it does not exist
                # "x" - Create - Creates the specified file, returns an error if the file exist
        
    # get titles' names
    file = pd.read_csv(file_input_path, encoding = 'utf-8')
    df = pd.DataFrame(file)

    output_file = open(file_output_path, mode)

    n_cmplt, n_fail = 0, 0
    cmplt, fail =[], []

    # search each of titles' names
    for title in df["Title"]:
        print("=== start searching for {} ===".format(title))
        url = search_for(title)
        print(url)
        if url != False:
            n_cmplt+=1
            cmplt.append(title)
            bibtex_info = get_bibtex(url, args.style_of_BibTex)
            
            print(bibtex_info)
            output_file.write(bibtex_info)
            print("=== completed searching for {} ===\n".format(title))
        else:
            n_fail+=1
            fail.append(title)
            print("=== SORRY! it failed searching for {} ===\n".format(title))

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
        for title in fail:
            print(title)

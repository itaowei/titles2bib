# coding:utf-8
import argparse, json, os
from titles2bibtex import *
import logging.config

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}

requests.packages.urllib3.disable_warnings()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



if  __name__ == '__main__':
    # get parameters
    parser = argparse.ArgumentParser(description='Find papers with keywords in the title at certain conferences and/or journals')
    parser.add_argument("-search","--search_range", metavar="ICSME", nargs='+',
                        help='the conferences and/or journals you want to search inside', required = True)
    parser.add_argument("-key","--key_words", metavar="empirical", nargs='+',
                        help='if a paper\'s title contains at least one of the key words, the paper will be returned', required = True)
    parser.add_argument("-max","--max_list_n", metavar=10, type=int,
                        help='the most recent max_list_n paper_list', required = True)
    parser.add_argument("-out","--output_file_path", metavar="searched_result.json",
                        help='the searched_result(conference_or_journal_name -> paper_list_url -> titles and BibTex info)', required = False)
    parser.add_argument("-s","--style", dest="style_of_BibTex", metavar=0, type = int, default=-1,
                        help='style of the BibTex, -1: more condensed (delete string between \'DBLP:\' and the 2nd \'/\' after that), 0: condensed, 1: standard, 2: with crossref', required = False)
    args = parser.parse_args()
    

    result = dict()
    for each in args.search_range:
        logger.info("Search:{}".format(each))
        conference_or_journal_name, conference_or_journal_url = search_for_conference_or_journal(each)
        result[conference_or_journal_name] = list()
        paper_list_url_list = search_for_list_url(conference_or_journal_url, args.max_list_n)
        for paper_list_url in paper_list_url_list:
            try:
                matched_titles, papers_total_n = matched_title_and_total_papers_num(paper_list_url, args.key_words)
            except:
                logger.info("ERROR:{},{}".format(paper_list_url, args.key_words))
            result[conference_or_journal_name].append({"paper_list_url":paper_list_url,"papers_total_n":papers_total_n,"matched_titles":matched_titles})

    if not args.output_file_path:
        args.key_words.sort()
        args.output_file_path = os.path.join("searched_result", "__".join(args.search_range).replace(" ", "_"), "{}.json".format("_".join(args.key_words).replace(" ","_")));
    os.makedirs(os.path.dirname(args.output_file_path), exist_ok=True)
    json.dump(result, open(args.output_file_path,"w"))

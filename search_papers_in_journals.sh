journal_list=("International Conference on Automated Software Engineering (ASE)" "Empirical Software Engineering" "IEEE Transactions on Neural Networks and Learning Systems")
for journal in "${journal_list[@]}";
do
    for keyword in "empirical" "code" "commit" "diff" "change" "generation" "experimental" "commits" "diffs" "changes";
    do
        python search_papers_with_keywords_in_the_title.py -search "${journal}" -key ${keyword} -max 100 -s -1
    done
done

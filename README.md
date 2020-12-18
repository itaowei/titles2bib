# titles2bibtex
BibTex Unification of Papers Based on the Titles Index at dblp

基于 dblp 索引标题的论文 BibTex 信息统一(中文版说明见后）

## BibTex Unification of Papers Based on the Titles Index at dblp

### Why & What
In the coorperation of papers' writting, multiple people may quote the same reference, but different people may have different BibTex information derived from the same paper, which will result in two citations in a paper. In order to unify BibTex information, based on [dblp](https://dblp.org/), a powerful on-line reference for bibliographic information on major computer science publications,  we can basically export consistent BibTex information of papers by searching their titles. 

What we do can also be regarded as the conversion from `papers' titles` to `their uniform BibTexs`.

### Input
A `.csv` file including many papers' titles which can be exported from reference mangemant app such as Zotero.

For example: `papers_titles.csv` (there must be a column with the title named `Title` in that file)
| Title                                                                                                |   |   |   |
|------------------------------------------------------------------------------------------------------|---|---|---|
| An investigation of cross\-project learning in online just\-in\-time software defect prediction      |   |   |   |
| ARDiff: scaling program equivalence checking via iterative abstraction and refinement of common code |   |   |   |
| CoRA: decomposing and describing tangled code changes for reviewer                                   |   |   |   |
| Boosting neural commit message generation with code semantic analysis                                |   |   |   |


### Parameter
`--input`: the path of the input file including papers\' titles. e.g. `papers_titles.csv`

`--output`: the path of the output file including papers\' BiTex. e.g. `references.bib`

`--mode`[alternative]: mode you want to open the output file, default is `w`.

&nbsp;&nbsp;&nbsp;&nbsp;`a` - Append - Opens a file for appending, creates the file if it does not exist.

&nbsp;&nbsp;&nbsp;&nbsp;`w` - Write - Opens a file for writing, creates the file if it does not exist.

`--style`[alternative]: style of the BibTex, default is `1`.

&nbsp;&nbsp;&nbsp;&nbsp;`0`: standard

&nbsp;&nbsp;&nbsp;&nbsp;`1`: condensed

&nbsp;&nbsp;&nbsp;&nbsp;`2`: more condensed (delete string between 'DBLP:' and the 2nd '/' after that)

### How to use
```
pip install lxml
pip install requests
pip install beautifulsoup4
pip install pandas

python titles2bibtex.py --input papers_titles.csv --output references.bib
```

### Output
A `.bib` file with uniform BibTex information of the papers.

For example: `references.bib`

```
@inproceedings{DBLP:conf/icse/TabassumMFCS20,
  author    = {Sadia Tabassum and
               Leandro L. Minku and
               Danyi Feng and
               George G. Cabral and
               Liyan Song},
  title     = {An investigation of cross-project learning in online just-in-time
               software defect prediction},
  booktitle = {{ICSE}},
  pages     = {554--565},
  publisher = {{ACM}},
  year      = {2020}
}


@inproceedings{DBLP:conf/sigsoft/BadihiA0R20,
  author    = {Sahar Badihi and
               Faridah Akinotcho and
               Yi Li and
               Julia Rubin},
  title     = {ARDiff: scaling program equivalence checking via iterative abstraction
               and refinement of common code},
  booktitle = {{ESEC/SIGSOFT} {FSE}},
  pages     = {13--24},
  publisher = {{ACM}},
  year      = {2020}
}


@inproceedings{DBLP:conf/kbse/WangLZX19,
  author    = {Min Wang and
               Zeqi Lin and
               Yanzhen Zou and
               Bing Xie},
  title     = {CoRA: Decomposing and Describing Tangled Code Changes for Reviewer},
  booktitle = {{ASE}},
  pages     = {1050--1061},
  publisher = {{IEEE}},
  year      = {2019}
}


@inproceedings{DBLP:conf/kbse/Jiang19,
  author    = {Shuyao Jiang},
  title     = {Boosting Neural Commit Message Generation with Code Semantic Analysis},
  booktitle = {{ASE}},
  pages     = {1280--1282},
  publisher = {{IEEE}},
  year      = {2019}
}
```


## 基于 dblp 索引标题的论文 BibTex 信息统一

### 为何
合作撰写论文中，多人可能需要引用同一篇参考文献，而不同人对同一篇文献导出的 BibTex 信息不一致，这样会造成对这篇文献有两个引用。为了统一BibTex信息，基于 [dblp](https://dblp.org/) 强大的平台，通过标题索引的方式，基本能够对计算机领域的论文导出一致的 BibTex 信息，从而实现了 `论文标题集合` 到 `统一格式的 BibTex 集合` 的转换。

### 输入
带有 Title 标题的 csv 文件（该文件可以通过文献管理软件进行导出）

例如：papers_titles.csv (文件中必须有一列的标题为`Title`)
| Title                                                                                                |   |   |   |
|------------------------------------------------------------------------------------------------------|---|---|---|
| An investigation of cross\-project learning in online just\-in\-time software defect prediction      |   |   |   |
| ARDiff: scaling program equivalence checking via iterative abstraction and refinement of common code |   |   |   |
| CoRA: decomposing and describing tangled code changes for reviewer                                   |   |   |   |
| Boosting neural commit message generation with code semantic analysis                                |   |   |   |


### 参数
`--input`: 包含有论文标题集合的CSV输入文件路径. 例如： `papers_titles.csv`

`--output`: 包含有BiTex信息的导出文件. 例如： `references.bib`

`--mode`（可选）: 对于输出文件是重新写入，还是继续添加，默认是 `w`即重新开始.

&nbsp;&nbsp;&nbsp;&nbsp;`a` - 继续添加 - 打开/创建该文件并在已有基础上继续添加.

&nbsp;&nbsp;&nbsp;&nbsp;`w` - 重新写入 - 打开/创建该文件重新写入.

`--style`（可选）: BibTex 的风格, 默认是 `1`.

&nbsp;&nbsp;&nbsp;&nbsp;`0`: 标准

&nbsp;&nbsp;&nbsp;&nbsp;`1`: 精简

&nbsp;&nbsp;&nbsp;&nbsp;`2`: 再精简（删除`DBLP`和其后第二个`/`中间的字符串以精简CiteKey）

### 使用方法
```
pip install lxml
pip install requests
pip install beautifulsoup4
pip install pandas

python titles2bibtex.py --input papers_titles.csv --output references.bib

```


### 输出
带有全部 BibTex 信息的 bib 文件

例如：references.bib
```
@inproceedings{DBLP:conf/icse/TabassumMFCS20,
  author    = {Sadia Tabassum and
               Leandro L. Minku and
               Danyi Feng and
               George G. Cabral and
               Liyan Song},
  title     = {An investigation of cross-project learning in online just-in-time
               software defect prediction},
  booktitle = {{ICSE}},
  pages     = {554--565},
  publisher = {{ACM}},
  year      = {2020}
}


@inproceedings{DBLP:conf/sigsoft/BadihiA0R20,
  author    = {Sahar Badihi and
               Faridah Akinotcho and
               Yi Li and
               Julia Rubin},
  title     = {ARDiff: scaling program equivalence checking via iterative abstraction
               and refinement of common code},
  booktitle = {{ESEC/SIGSOFT} {FSE}},
  pages     = {13--24},
  publisher = {{ACM}},
  year      = {2020}
}


@inproceedings{DBLP:conf/kbse/WangLZX19,
  author    = {Min Wang and
               Zeqi Lin and
               Yanzhen Zou and
               Bing Xie},
  title     = {CoRA: Decomposing and Describing Tangled Code Changes for Reviewer},
  booktitle = {{ASE}},
  pages     = {1050--1061},
  publisher = {{IEEE}},
  year      = {2019}
}


@inproceedings{DBLP:conf/kbse/Jiang19,
  author    = {Shuyao Jiang},
  title     = {Boosting Neural Commit Message Generation with Code Semantic Analysis},
  booktitle = {{ASE}},
  pages     = {1280--1282},
  publisher = {{IEEE}},
  year      = {2019}
}
```


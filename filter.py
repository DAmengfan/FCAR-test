import textwrap
import re
import chardet

import re

def cut_sent(infile, outfile):
  cutLineFlag = ["？", "！", "。","…"] #本文使用的终结符，可以修改
  sentenceList = []
  with open(infile, "r", encoding="UTF-8") as file:
    oneSentence = ""
    for line in file:
      if len(oneSentence)!=0:
        sentenceList.append(oneSentence.strip() + "\r")
        oneSentence=""
      words = line.strip()
      for word in words:
        if word not in cutLineFlag:
          oneSentence = oneSentence + word
        else:
          oneSentence = oneSentence + word
          if oneSentence.__len__() > 4:
            sentenceList.append(oneSentence.strip() + "\r")
          oneSentence = ""
  with open(outfile, "a", encoding="UTF-8") as resultFile:
    print(sentenceList.__len__())
    resultFile.writelines(sentenceList)
    resultFile.close()

  with open ("terminal.txt","a",encoding= "UTF-8") as resultfile:
    search_keywords = ['股权','控股','持股','占股','持有','增持','减持','投资','领投','跟投','合作','收购','旗下','募股','子公司','并购',
                       '介入','投入','入股','客户','交易','供货','出货','承销商','股东','创始人','创立','董事长','董事','监事','CEO','总经理','首席执行官',
                       '主席','副总裁','总监','主任','行长','高管','高级管理人员','研究员','任职','曾任','就任']
    for sentence in sentenceList:
      if (any(map(lambda word: word in sentence, search_keywords))):
        print (sentence)
        resultfile.write(sentence)
    resultfile.close()
if __name__ == '__main__':

    cut_sent('link.txt', 'link1.txt')



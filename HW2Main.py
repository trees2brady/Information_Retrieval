import PreProcessData.TrectextCollection as TrectextCollection
import PreProcessData.TrecwebCollection as TrecwebCollection
import PreProcessData.StopWordRemover as StopWordRemover
import PreProcessData.WordNormalizer as WordNormalizer
import PreProcessData.WordTokenizer as WordTokenizer
import Classes.Path as Path
import datetime
from PreProcessData.PreProcessedCorpusReader import PreProcessedCorpusReader
from MyIndexWriter import MyIndexWriter


def WriteIndex(dataType):
    corpus = PreProcessedCorpusReader()
    output = MyIndexWriter(dataType)
    count = 0
    doc = corpus.NextDocument()
    while doc is not None and len(doc) > 0:
        docno = doc[0]
        content = doc[1]
        output.IndexADocument(docno, content)
        count += 1
        if count % 30000 == 0:
            print("finish " + str(count) + " docs")
        doc = corpus.NextDocument()
    output.close()


def ReadIndex():
    pass
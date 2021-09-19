import PreProcessData.TrectextCollection as TrectextCollection
import PreProcessData.TrecwebCollection as TrecwebCollection
import PreProcessData.StopWordRemover as StopWordRemover
import PreProcessData.WordNormalizer as WordNormalizer
import PreProcessData.WordTokenizer as WordTokenizer
import Classes.Path as Path
import datetime
from PreProcessData.PreProcessedCorpusReader import PreProcessedCorpusReader
from MyIndexWriter import MyIndexWriter
from MyIndexReader import MyIndexReader
from QueryRetrievalModel import QueryRetrievalModel
from ExtractQuery import ExtractQuery

idx_reader = MyIndexReader("trectext")
model = QueryRetrievalModel(idx_reader)
queries = ExtractQuery()

while queries.hasNext():
    aQuery = queries.hasNext()
    print(str(aQuery.GetTopicId()) + "\t" + str(aQuery.GetQueryContent()))
    results = model.retrieveQuery(aQuery, 20)
    if results is not None and len(results) != 0:
        rank = 1
        for result in results:
            print(str(aQuery.GetTopicId()) + " Q0 " + str(result.docno()) + " " + str(rank) + " " + str(result.score()) + " MYRUN")
            rank += 1
    idx_reader.close()
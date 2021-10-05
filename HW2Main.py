import Indexing.PreProcessedCorpusReader as PreprocessedCorpusReader
import Indexing.MyIndexWriter as MyIndexWriter
import Indexing.MyIndexReader as MyIndexReader
import datetime

def WriteIndex(type):
    count = 0
    # Initiate pre-processed collection file reader.
    corpus =PreprocessedCorpusReader.PreprocessedCorpusReader(type)
    # Initiate the index writer.
    indexWriter = MyIndexWriter.MyIndexWriter(type)
    # Build index of corpus document by document.
    while True:
        doc = corpus.nextDocument()
        if doc == None:
            break
        indexWriter.index(doc[0], doc[1])
        count+=1
        if count%30000==0:
            print("finish ", count," docs")
    print("totally finish ", count, " docs")
    indexWriter.close()
    return


def ReadIndex(type, token):
    # Initiate the index file reader.
    index =MyIndexReader.MyIndexReader(type)
    # retrieve the token.
    df = index.DocFreq(token)
    ctf = index.CollectionFreq(token)
    print(" >> the token \""+token+"\" appeared in "+ str(df) +" documents and "+ str(ctf) +" times in total")
    if df>0:
        posting = index.getPostingList(token)
        for docId in posting:
            docNo = index.getDocNo(docId)
            print(str(docNo) +"\t"+str(docId)+"\t"+str(posting[docId]))

startTime = datetime.datetime.now()
WriteIndex("trecweb")
endTime = datetime.datetime.now()
print ("index web corpus running time: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("trecweb", "acow")
endTime = datetime.datetime.now()
print ("load index & retrieve the token running time: ", endTime - startTime)

startTime = datetime.datetime.now()
WriteIndex("trectext")
endTime = datetime.datetime.now()
print ("index web corpus running time: ", endTime - startTime)
startTime = datetime.datetime.now()
ReadIndex("trecweb", "yhoo")
endTime = datetime.datetime.now()
print ("load index & retrieve the token running time: ", endTime - startTime)
from MyIndexReader import MyIndexReader


class QueryRetrievalModel:
    def __init__(self, idx_reader):
        self.MU = 2000.0
        self.indexReader = MyIndexReader()
        self.CORPUS_SIZE = self.indexReader.CorpusSize()

    def retrieveQuery(self, aQuery, TopN):
        results = []
        queryResult = {}
        termFreq = {}
        tokens = aQuery.GetQueryContent().split(" ")

        for token in tokens:
            cf = self.indexReader.CollectionFreq(token)
            termFreq[token] = cf

            if cf == 0:
                print("Token <" + str(token) + "> not found in corpus!")
                continue
            postingList = self.indexReader.getPostingList(token)

            for posting in postingList:
                if not queryResult.get(posting[0]):
                    ttf = {}
                    queryResult[posting[0]] = ttf
                else:
                    queryResult[posting[0]][token] = posting[1]

        lResults = []
        for doc_id in queryResult.keys():
            doclen = 0
            score = 1.0
            try:
                doclen = self.indexReader.docLength(doc_id)
            except Exception as e:
                print(e)

            c1 = doclen / (doclen + self.MU)
            c2 = self.MU / (doclen + self.MU)

            for token in tokens:
                cf = cf = termFreq[token]
                if cf == 0:
                    continue
                tf = queryResult[doc_id].get(token, 0)
                p_doc = float(tf / doclen)
                p_ref = float(cf / self.CORPUS_SIZE)
                score *= (c1 * p_doc + c2 * p_ref)
            tmpDS =  DocScore(doc_id, score)
            lResults.append(tmpDS)

        # sort the List with DocScoreComparator()
        # Collections.sort(lResults, new DocScoreComparator());
        for cnt in range(TopN):
            ds = lResults[cnt]
            doc = None
            try:
                id = ds.getId()
                doc = Document(Integer.toString(id), self.indexReader.getDocno(id), ds.getScore())  # Document 在Classes里
            except Exception as e:
                print(e)
            results.append(doc)
        return results


class DocScore:
    def __init__(self, docid, score):
        return
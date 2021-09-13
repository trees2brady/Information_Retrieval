class MyIndexReader:
    def __init__(self, data_type):
        self.data_type = data_type

        self.file = open("data//" + self.data_type + ".dict")
        self.fis_ID_no = open("data//" + self.data_type + ".idno")

        self.map_dic = {}
        self.mp_ID_no = {}

        string = self.file.readline()
        while string != "":
            s = string.split(",")
            self.map_dic[s[0]] = s[1]
            string = self.file.readline()

        string = self.fis_ID_no.readline()
        while string != "":
            s = string.split(",")
            self.mp_ID_no[s[0]] = s[1]
            self.mp_ID_no[s[1]] = s[0]
            string = self.fis_ID_no.readline()

    def GetDocFreq(self, token):
        string = self.postingOf(token)
        if string != "":
            docs = string.split(";")
            return len(docs)
        return 0

    def GetPostingList(self, token):
        string = self.postingOf(token)
        if string != "":
            docs = string.split(";")
            i = 0
            pl = [[0] * len(docs)] * 2
            for s in docs:
                pl[i][0] = s.split(":")[0]
                pl[i][1] = s.split(":")[1].split(",")[0]
                i += 1
            return pl
        return None

    def GetCollectionFreq(self, token):
        string = self.postingOf(token)
        if string != "":
            docs = string.split(";")
            i_total = 0
            for s in docs:
                i_total += int(s.split(";")[1].split(",")[0])
            return i_total
        return 0

    def GetDocno(self, doc_ID):
        return str(self.mp_ID_no[doc_ID])

    def postingOf(self, token):
        i_line = self.map_dic.get(token, -1)
        fis = open("data//" + self.data_type + ".ridx")
        if i_line is not None and i_line > 0:
            for i in range(i_line):
                fis.readline()
            pos = fis.readline().split("\\s")  #啥意思？可能是空格？
            fis.close()
            return pos[1]
        return None

    def close(self):
        self.file.close()
        self.fis_ID_no.close()
        self.map_dic.clear()
        self.mp_ID_no.clear()

    def CorpusSize(self):
        return
import Classes.Path as Path


# Efficiency and memory cost should be paid with extra attention.
class MyIndexReader:

    def __init__(self, type):
        self.data_type = type

        self.file_dict = open("data//" + self.data_type + ".dict", "r")
        self.fis_ID_no = open("data//" + self.data_type + ".idno", "r")

        self.map_dic = {}
        self.map_ID_no = {}

        string = self.file_dict.readline()
        while string is not None and string != "":
            s = string.split(",")
            self.map_dic[s[0]] = s[1].rstrip("\n")
            string = self.file_dict.readline()

        string = self.fis_ID_no.readline()
        while string is not None and string != "":
            s = string.split(",")
            self.map_ID_no[s[0]] = s[1].rstrip("\n")
            self.map_ID_no[s[1].rstrip("\n")] = s[0]
            string = self.fis_ID_no.readline()
        print("finish reading the index")

    # Return the integer DocumentID of input string DocumentNo.
    def getDocId(self, docNo):
        return -1

    # Return the string DocumentNo of the input integer DocumentID.
    def getDocNo(self, docId):
        return self.map_ID_no[docId] if self.map_ID_no.get(docId) else -1

    # Return DF.
    def DocFreq(self, token):
        string = self.postingOf(token)
        if string is not None and string != "":
            docs = string.split(";")
            return len(docs) - 1 if len(docs) - 1 >= 0 else 0
        return 0

    # Return the frequency of the token in whole collection/corpus.
    def CollectionFreq(self, token):
        string = self.postingOf(token).rstrip("\n")
        if string != "":
            docs = string.split(";")
            i_total = 0
            for posting in docs:
                if posting is not None and len(posting) > 0:
                    i_total += int(posting.split(":")[1].split(",")[0])
            return i_total
        return 0

    # Return posting list in form of {documentID:frequency}.
    def getPostingList(self, token):
        string = self.postingOf(token).rstrip("\n")
        if string is not None and string != "":
            docs = string.split(";")
            posting_list = {}
            for posting in docs:
                if posting is not None and len(posting) > 0:
                    posting_list[posting.split(":")[0]] = posting.split(":")[1].split(",")[0]

            return posting_list
        return None

    def postingOf(self, token):
        """
        find the line number of the token's position
        :param token:
        :return:str type, token's posting list,looks like:term_frequency,position1,position2,position3;doc_ID:term_frequency,position1,position2,position3;
        """
        i_line = int(self.map_dic.get(token, -1).rstrip("\n"))
        fis = open("data//" + self.data_type + ".ridx", "r")
        if i_line is not None and i_line > 0:
            for i in range(i_line):
                fis.readline()
            pos = fis.readline().split(" ")
            fis.close()
            return pos[1]
        return None

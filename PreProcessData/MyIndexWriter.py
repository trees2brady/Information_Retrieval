from Classes import Path

class MyIndexWriter:
    def __init__(self, data_type):
        self.data_type = data_type
        self.file = open("data//" + self.data_type + ".idno", "w", encoding="utf-8")
        self.doc_ID = 0
        self.raw_index = RawIndex()
        self.MAX_NUM_PER_BLOCK = 40000
        self.num_of_idx_in_block = 0
        self.block_id = 0

    def IndexADocument(self, docno, content):
        inverted_dic = {} if self.inverse(content) is None else self.inverse(content)
        self.raw_index.update(inverted_dic)
        self.num_of_idx_in_block += 1
        self.file.write(str(self.doc_ID) + "," + docno + "\n")
        self.doc_ID += 1

        if self.num_of_idx_in_block == self.MAX_NUM_PER_BLOCK:
            self.block_to_disk()

        self.close()

    def inverse(self, content):
        if content is not None and len(content) > 0:
            tokens = content.split(" ")
            inverted_dic = {}
            for token_idx in range(len(tokens)):
                if inverted_dic.get(tokens[token_idx]) is not None:
                    inverted_dic[tokens[token_idx]].append(token_idx)
                    inverted_dic[tokens[token_idx]][1] += 1
                else:
                    inverted_dic[tokens[token_idx]] = [self.doc_ID, 1, token_idx]
            return inverted_dic
        return None

    def block_to_disk(self):
        file = open("data//." + self.data_type + ".ridx" + self.block_id)


    def close(self):
        self.file.close()


class RawIndex:
    def __init__(self):
        self.map_term = {}

    def update(self, inverted_dic):
        if inverted_dic is not None and len(inverted_dic) > 0:
            for key in inverted_dic.keys():
                if self.map_term.get(key) is not None:
                    self.map_term[key].append(inverted_dic[key])
                else:
                    self.map_term[key] = inverted_dic[key]

            return True
        return False

    def clear(self):
        if len(self.map_term) != 0:
            self.map_term.clear()
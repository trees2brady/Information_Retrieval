from Classes import Path
import os


class MyIndexWriter:
    def __init__(self, data_type):
        self.data_type = str(data_type)
        self.temporary_write_file_in_memory= open("data//" + self.data_type + ".idno", "w", encoding="utf-8")
        self.doc_ID = 0
        self.raw_index = RawIndex()
        self.MAX_NUM_PER_BLOCK = 40000
        self.num_of_idx_in_block = 0
        self.block_id = 0

    def IndexADocument(self, docno, content):
        inverted_dic = {} if self.inverse(content) is None else self.inverse(content)
        self.raw_index.update(inverted_dic)
        self.num_of_idx_in_block += 1
        self.temporary_write_file_in_memory.write(str(self.doc_ID) + "," + docno + "\n")
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
        memory_to_disk_file = open("data//." + self.data_type + ".ridx" + str(self.block_id))
        for key in self.raw_index.map_term.keys():
            try:
                memory_to_disk_file.write(str(key) + " ")
                for i in range(len(self.raw_index.map_term[key])):
                    memory_to_disk_file.write(str(self.raw_index.map_term[key][i][0]) + ":" + str(str(self.raw_index.map_term[key][i][1])) + ",")
                    for j in range(len(self.raw_index.map_term[key][i])):
                        string = ":" if j == len(self.raw_index.map_term[key][i]) - 1 else ";"
                        memory_to_disk_file.write(str(self.raw_index.map_term[key][i][j]) + string)
            except Exception as e:
                print(e)
        self.num_of_idx_in_block = 0
        self.block_id += 1
        memory_to_disk_file.close()
        self.raw_index.clear()

    def fuse(self):
        mp = {}
        for i in range(self.block_id):
            file = open("data//." + self.data_type + ".ridx" + str(i))
            str_line = file.readline()
            while str_line is not None and str_line != '':
                sp = str_line.split(" ")
                if mp.get(sp[0]) is None:
                    mp[sp[0]] = sp[1]
                else:
                    mp[sp[0]] = mp[sp[0]] + sp[1]
            file.close()
            os.remove("data//." + self.data_type + ".ridx" + str(i))
        file_idx = open("data//" + self.data_type + ".ridx")
        for key in mp.keys():
            try:
                file_idx.write(str(key) + " " + str(mp[key]) + "\n")
            except Exception as e:
                print(e)
        mp.clear()
        file_idx.close()

    def build_dic(self):
        file_idx = open("data//" + self.data_type + ".ridx")
        file_dic = open("data//" + self.data_type + ".dict")
        str_line = file_idx.readline()
        i_num_of_line = 0
        while str_line is not None and str_line != "":
            term = str_line.split(" ")
            i_num_of_line += 1
            file_dic.write(str(term[0]) + "," + str(i_num_of_line) + "\n")
        file_idx.close()
        file_dic.close()

    def close(self):
        self.block_to_disk()
        self.temporary_write_file_in_memory.close()
        self.raw_index.clear()
        self.fuse()
        self.build_dic()


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
import Classes.Path as Path
import os


# Efficiency and memory cost should be paid with extra attention.
class MyIndexWriter:

    def __init__(self, type):
        self.data_type = type
        self.file_id_no = open("data//" + self.data_type + ".idno", "w", encoding="utf-8")
        self.doc_ID = 0
        self.raw_index = Index()  # temporarily store index file in memory
        self.MAX_NUM_PER_BLOCK = 49590
        self.num_of_idx_in_block = 0
        self.block_id = 0

    def index(self, docNo, content):
        """
        This method build index for each document.
        NT: in your implementation of the index, you should transform your string docno into non-negative integer docids,
        and in MyIndexReader, you should be able to request the integer docid for each docno.
        :param docNo:
        :param content:
        :return:
        """
        inverted_dic = {} if self.inverse(content) is None else self.inverse(content)
        self.raw_index.update(inverted_dic)  # put every document's resulting index into object raw_index
        self.num_of_idx_in_block += 1
        self.file_id_no.write(str(self.doc_ID) + "," + docNo + "\n")
        self.doc_ID += 1

        if self.num_of_idx_in_block == self.MAX_NUM_PER_BLOCK:
            self.block_to_disk()  # write the inverted index stored in memory to disk

    # Close the index writer, and you should output all the buffered content (if any).
    def close(self):
        self.block_to_disk()
        self.file_id_no.close()
        self.raw_index.clear()
        self.fuse()
        self.build_dict()

    def inverse(self, content):
        """
        Create the inverted index for each document
        :param content:
        :return:inverted_dic
        input looks like:
        "februari re earl semant and queryabl name sean b palmer februari re earl semant and queryabl name charl februari"
        inverted_dic is the posting list, which looks like below:
        {term:[doc_ID, term_frequency,position1,position2...]}
        """
        if content is not None and len(content) > 0:
            tokens = content.split(" ")
            inverted_dic = {}
            for token_idx in range(len(tokens)):
                if tokens[token_idx] == "\n":
                    continue
                if inverted_dic.get(tokens[token_idx]) is not None:
                    inverted_dic[tokens[token_idx]].append(token_idx)
                    inverted_dic[tokens[token_idx]][1] += 1
                else:
                    inverted_dic[tokens[token_idx]] = [self.doc_ID, 1, token_idx]
            return inverted_dic
        return None

    def block_to_disk(self):
        """
        write the inverted index stored in memory to disk
        input is like:
        {token:[[term_frequency,position1,position2,...],[term_frequency,position1, position2...]]}
        :return:
        every line looks like below:
        term doc_ID:term_frequency,position1,position2,position3;doc_ID:term_frequency,position1,position2,position3;
        """
        file_raw_idx = open("data//." + self.data_type + ".ridx" + str(self.block_id), "w")
        for key in self.raw_index.map_term.keys():
            try:
                file_raw_idx.write(str(key) + " ")
                for doc in range(len(self.raw_index.map_term[key])):
                    file_raw_idx.write(str(self.raw_index.map_term[key][doc][0]) + ":" + str(str(self.raw_index.map_term[key][doc][1])) + ",")
                    for position in range(2, len(self.raw_index.map_term[key][doc])):
                        string = ";" if position == len(self.raw_index.map_term[key][doc]) - 1 else ","
                        file_raw_idx.write(str(self.raw_index.map_term[key][doc][position]) + string)
                file_raw_idx.write("\n")
            except Exception as e:
                print(e)
        self.num_of_idx_in_block = 0
        self.block_id += 1
        file_raw_idx.close()
        self.raw_index.clear()  # clear the temporary stored index

    def fuse(self):
        """
        merge all segments of index files, output a file with all indices
        :return:
        """
        mp = {}
        for block_id in range(self.block_id):
            open_raw_idx_file = open("data//." + str(self.data_type) + ".ridx" + str(block_id), "r")
            line_str = open_raw_idx_file.readline()
            while line_str is not None and len(line_str) != 0:
                str_split = line_str.split(" ")
                if mp.get(str_split[0]) is None:
                    mp[str_split[0]] = str_split[1].rstrip("\n")
                else:
                    mp[str_split[0]] = mp[str_split[0]] + str_split[1].rstrip("\n")
                line_str = open_raw_idx_file.readline()
            open_raw_idx_file.close()
            os.remove("data//." + str(self.data_type) + ".ridx" + str(block_id))
        file_idx = open("data//" + str(self.data_type) + ".ridx", "w")
        for key in mp.keys():
            try:
                file_idx.write(str(key) + " " + str(mp[key]) + "\n")
            except Exception as e:
                print(e)
        mp.clear()
        file_idx.close()

    def build_dict(self):
        """
        construct the dictionary of vocabulary
        :return:
        """
        file_idx = open("data//" + str(self.data_type) + ".ridx", "r")
        file_dict = open("data//" + str(self.data_type) + ".dict", "w")
        i_line_num = 0
        str_line = file_idx.readline()
        while str_line is not None and len(str_line) != 0:
            term = str_line.split(" ")
            file_dict.write(term[0] + "," + str(i_line_num) + "\n")
            i_line_num += 1
            str_line = file_idx.readline()
        file_idx.close()
        file_dict.close()


class Index:
    """
    A new class called when initializing MyIndexWriter to store index in memory temporarily
    """
    def __init__(self):
        self.map_term = {}

    def update(self, inverted_dic):
        """
        :param inverted_dic:
        :return:
        store index files like:
        {token:[[term_frequency,position1,position2,...],[term_frequency,position1, position2...]]}
        """
        if inverted_dic is not None and len(inverted_dic) > 0:
            for key in inverted_dic.keys():
                if self.map_term.get(key) is not None:
                    self.map_term[key].append(inverted_dic[key])
                else:
                    self.map_term[key] = []
                    self.map_term[key].append(inverted_dic[key])
            return True
        return False

    def clear(self):
        if len(self.map_term) != 0:
            self.map_term.clear()
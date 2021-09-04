import Classes.Path as Path
import re

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class TrecwebCollection:

    def __init__(self, file=Path.DataWebDir):
        # 1. Open the file in Path.DataWebDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.file = open(file, "r", encoding="utf-8")
        self.re_str = "(<(.*?)>)|(\\[(.*?)\\])|(\\&\\#?\\S+( ))|(( )\\S+>( ))"  # Regular expression used to remove html tags in content

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, return null, and close the file.
        # 3. the HTML tags should be removed in document content.
        docNo = ""
        content = ""
        line_str = self.file.readline()
        if line_str != '':
            while line_str != '' and line_str.strip("\n") != "<DOC>":  # Keeping reading until reaching the "<DOC>"
                line_str = self.file.readline()

            while line_str != '' and line_str.strip("\n") == "<DOC>":  # Start to get values of docNo fields
                line_str = self.file.readline()
                docNo = line_str[7:-9]

            while line_str != '' and line_str.strip("\n") != "</DOCHDR>":  # Keeping reading until reaching the start of content
                line_str = self.file.readline()

            line_str = self.file.readline()

            while line_str != '' and line_str.strip("\n") != "</DOC>":  # # Start to get values of content fields
                content += re.sub(self.re_str, " ", line_str).strip("\n")  # Replace html tags and \n with space
                line_str = self.file.readline()


            return [docNo, content]
        self.file.close()
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.


class TrectextCollection:

    def __init__(self, file=Path.DataTextDir):
        # 1. Open the file in Path.DataTextDir.
        # 2. Make preparation for function nextDocument().
        # NT: you cannot load the whole corpus into memory!!
        self.file = open(file, "r", encoding="utf-8")  # Open file and keep file status in Class instance

    def nextDocument(self):
        # 1. When called, this API processes one document from corpus, and returns its doc number and content.
        # 2. When no document left, eturn null, and close the file.
        docNo = ""
        content = ""
        line_str = self.file.readline()  # Read the first line
        if line_str != '':  # In python, when reaching the end of a file, it will return a "''"(empty string) instead of null in Java

            while line_str != '' and line_str.strip("\n") != "<DOC>":  # Keeping reading until reaching the sign of "<DOC>"
                line_str = self.file.readline()

            while line_str != '' and line_str.strip("\n") == "<DOC>":  # Getting to the starting signal and start to get docNo
                line_str = self.file.readline()
                docNo = line_str[7:-9].strip()

            while line_str != '' and line_str.strip("\n") != "<TEXT>":  # Keeping reading until reaching the sign of "<TEXT>"
                line_str = self.file.readline()

            line_str = self.file.readline()

            while line_str != '' and line_str.strip("\n") != "</TEXT>":  # Keeping reading and assign line_str to content until reaching the sign of "</TEXT>"
                content += line_str.replace("\n", " ")  # Replace the \n at the end of each line with a space
                line_str = self.file.readline()

            while line_str != '' and line_str.strip("\n") != "</DOC>":  # Reaching the end of one document
                line_str = self.file.readline()

            return [docNo, content]
        self.file.close()
        return None
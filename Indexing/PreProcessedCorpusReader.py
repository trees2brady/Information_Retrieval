import Classes.Path as Path


class PreprocessedCorpusReader:

    def __init__(self, type):
        self.file = open(Path.ResultHM1 + str(type), "r", encoding="utf-8")  # Open file and keep file status in Class instance

    # Read a line for docNo from the corpus, read another line for the content, and return them in [docNo, content].
    def nextDocument(self):
        line_str = self.file.readline()  # Read the first line
        if line_str != '':  # In python, when reaching the end of a file, it will return a "\'\'"(empty string) instead of null in Java
            docNo = line_str.strip("\n")
            content = self.file.readline()
            return [docNo, content]
        self.file.close()
        return None
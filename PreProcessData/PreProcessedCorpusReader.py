from Classes import Path


class PreProcessedCorpusReader:
    def __init__(self):
        self.file = open(Path.ResultHM1, "r", encoding="utf-8")  # Open file and keep file status in Class instance

    def NextDocument(self):
        line_str = self.file.readline()  # Read the first line
        if line_str != '':  # In python, when reaching the end of a file, it will return a "''"(empty string) instead of null in Java
            docNo = line_str
            content = self.file.readline()
            return [docNo, content]
        self.file.close()
        return None
import Classes.Path as Path

# Efficiency and memory cost should be paid with extra attention.
# Essential private methods or variables can be added.
class StopWordRemover:

    def __init__(self, file=Path.StopwordDir):
        # Load and store the stop words from the fileinputstream with appropriate data structure.
        # NT: address of stopword.txt is Path.StopwordDir.
        self.file = open(file, "r", encoding="utf-8")    # Open file and keep file status in Class instance

    def isStopword(self, word):
        # Return true if the input word is a stopword, or false if not.
        return False

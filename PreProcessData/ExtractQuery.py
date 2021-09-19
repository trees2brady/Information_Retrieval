from Classes import Path
from Classes import Query
from WordTokenizer import WordTokenizer
from StopWordRemover import StopWordRemover
from WordNormalizer import WordNormalizer


class ExtractQuery:
    def __init__(self):
        self.fis = open(Path.TopicDir)
        self.line = self.fis.readline()

    def hasNext(self):
        if self.line:
            return True
        return False  #有一个buffer需要注意

    def next(self):
        qNext = Query()
        title = ""
        title_n = ""
        desc = ""
        desc_n = ""
        narr = ""
        narr_n = ""
        tokenizer_title = WordTokenizer()
        tokenizer_desc = WordTokenizer()
        tokenizer_narr = WordTokenizer()
        stopwordRemover = StopWordRemover()
        normalizer = WordNormalizer()
        if "<top>" not in self.line:
            self.line = self.fis.readline()

        self.line = self.fis.readline()
        qNext.SetTopicId(self.line[self.line.index(":") + 2:len(self.line)])
        self.line = self.fis.readline()
        title = self.line[self.line.index(">") + 2:len(self.line)]
        self.line = self.fis.readline()
        self.line = self.fis.readline()

        while "<narr>" not in self.line:
            desc += self.line
            self.line = self.fis.readline()
        self.line = self.fis.readline()

        while "</top>" not in self.line:
            narr += self.line
            self.line = self.fis.readline()
        # tokenizer_title = WordTokenizer(title.toCharArray())  # 原句是toCharArray
        tokenizer_title = WordTokenizer(title)
        tokenizer_desc = WordTokenizer(desc)
        tokenizer_narr = WordTokenizer(narr)
        stopwordRemover = StopWordRemover()
        normalizer = WordNormalizer()
        # ***********************以上都是toCharArray
        word = tokenizer_title.nextWord()

        while word is not None and len(word) != 0:
            word = normalizer.lowercase(word)
            if not stopwordRemover.isStopword(word):
                title_n += normalizer.stem(word) + " "

        word = tokenizer_desc.nextWord()
        while word is not None and len(word) != 0:
            word = normalizer.lowercase(word)
            if not stopwordRemover.isStopword(word):
                desc_n += normalizer.stem(word) + " "

        word = tokenizer_narr.nextWord()
        while word is not None and len(word) != 0:
            word = normalizer.lowercase(word)
            if not stopwordRemover.isStopword(word):
                narr_n += normalizer.stem(word) + " "

        qNext.setQueryTitle(title_n)
        qNext.setQueryDesc(desc_n)
        qNext.setQueryNarr(narr_n)
        qNext.SetQueryContent(title_n)

        return qNext

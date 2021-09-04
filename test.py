from PreProcessData import TrecwebCollection
from Classes import Path
import re
s = TrecwebCollection.TrecwebCollection()
# x = s.nextDocument()
# x1 = s.nextDocument()
print(s.nextDocument())
print(s.nextDocument())
# s = "asdas<a>asdadasd"
# print(re.sub("<.*?>", " ", s))
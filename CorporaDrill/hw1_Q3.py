# This is only a test
# A seccessfull one 
# need to run this on the actual data

from collections import Counter
words = "apple banana apple strawberry banana banana lemon"
freqs = Counter(words.split())
print(freqs)

sorted_freqs = freqs.most_common()
print(sorted_freqs)

import codecs
outputFileStream = codecs.open("freqlist.txt" , "w", "utf-8")
outputFileStream.writelines(("%s\r\n" % (str(idx + 1) + " " + val[0] + " " + str(val[1])) for idx, val in enumerate(sorted_freqs)))

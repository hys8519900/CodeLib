import os

filepath = 'c:/pk_blank.txt'
fp = open(filepath)
text = fp.read()
text = text.replace(" ","")
print text
fp.close()

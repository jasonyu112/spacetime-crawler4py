import re
import string
#tokenize runs in exponential time because it loops through the file and grabs line by line. In the worst case, the line contains
#the same number of words as the number of lines in the file making this O(n^2).
def tokenize(s):
    #tokenize takes in a string and returns a list of all words separated by punctuation
    returnArr = []
    alparr = re.findall(r"\w*",s)
    for x in range(len(alparr)):
        if alparr[x] != "" and alparr[x][-1] in string.punctuation:
            alparr[x] = alparr[x][:-1]
        if alparr[x] != "" and alparr[x][0] in string.punctuation:
            alparr[x] = alparr[x][1:]
        if alparr[x] != "":
            returnArr.append(alparr[x].lower())
    return returnArr

#ComputeWordFrequencies runs in polynomial time because it loops through an array that contains n elements making it O(n).
def computeWordFrequencies(l):
    d = {}                                                                                  #makes dict and goes through list
    for x in range(len(l)):                                                                 #when the first occurrence of the word appears, it is added to the dict
        if l[x].lower() in d.keys():                                                        #with a value of 1 and other occurrences add to the value
            d[l[x].lower()] += 1
        else:
            d[l[x].lower()] = 1
    return d

#myPrint is O(n*logn) because that is the time complexity of the sorted function.
def myPrint(frequencyMap):
    sortedArr = sorted(frequencyMap.items(), key= lambda x:x[1], reverse=True)              #sorts the dict by decreasing frequency
    for x in range(len(sortedArr)):                                                         #loops and prints the sorted list
        print(f'{sortedArr[x][0]} - {sortedArr[x][1]}')


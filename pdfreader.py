# importing all the required modules
import PyPDF2
import sys
import csv
from operator import itemgetter

def readFile():
  # creating an object 
  print 'This is the name of the script: ', sys.argv[1]
  file = open(sys.argv[1], 'rb')

  # creating a pdf reader object
  fileReader = PyPDF2.PdfFileReader(file)

  fullList = []
  for page in range(fileReader.numPages):
    pageObj = fileReader.getPage(page)
    pageText = pageObj.extractText()
    for word in pageText.split():
      fullList.append(word.encode('utf-8'.strip()))

  file.close()
  returnList = fullList[4:]
  return returnList

def removeGrade(list):
  gradeless = []

  for item in list:
    if '(' in item[0]:
      continue
    if ')' in item[-1]:
      continue
    if '-' in item:
      continue
    gradeless.append(item)
  return gradeless

def removeNoCompetes(list):
  removed = []

  for item in list:
    if item['score'] != 0:
      removed.append(item)
  return removed

def isNumber(item):
    try:
        float(item)
        return True
    except ValueError:
        return False

def isGender(item):
  if item == 'Male' or item == 'Female':
    return True
  return False

def isDifficulty(item):
  if item == 'Beginner' or item == 'Intermediate' or item == 'Advanced' or item == 'Open':
    return True
  return False

def buildDic(list):
  complete = []
  person = dict()

  for i, item in enumerate(list):
    if isGender(item):
      person['gender'] = item
    elif isDifficulty(item):
      person['difficulty'] = item
    elif isNumber(item):
      person['score'] = int(item)
      complete.append(person)
      person = dict()
    elif 'name' in person:
      if item == 'Intro':
        continue
      person['name'] = person['name'] + ' ' + item
    else:
      person['name'] = item
  return complete

def sortByGender(gender, list):
  gendered = []
  sortedGender = []

  for item in list:
    if item['gender'] == gender:
      gendered.append(item)
  sortedGender = sorted(gendered, key=itemgetter('score'), reverse=True)
  return sortedGender

def sortByDifficulty(dif, list):
  diff = []
  sortedByDiff = []
  rank = 1
  for item in list:
    if item['difficulty'] == dif:
      item['rank'] = rank
      diff.append(item)
      rank += 1
  sortedByDiff = sorted(diff, key=itemgetter('score'), reverse=True)
  return sortedByDiff

def writeCSV(title, list):
  with open(title, 'wa') as csvfile:
    fieldnames = ['Rank', 'Name', 'Gender', 'Difficulty', 'Score']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for grouping in list:
      writer.writeheader()
      for person in grouping:
        writer.writerow({'Rank': person['rank'], 'Name': person['name'], 'Gender': person['gender'], 'Difficulty': person['difficulty'], 'Score': person['score']})

fullList = readFile()
unsortedDict = buildDic(removeGrade(fullList))
unsortedDict = removeNoCompetes(unsortedDict)

males = sortByGender('Male', unsortedDict)
females = sortByGender('Female', unsortedDict)

openMale = sortByDifficulty('Open', males)
advancedMale = sortByDifficulty('Advanced', males)
intermediateMale = sortByDifficulty('Intermediate', males)
beginnerMale = sortByDifficulty('Beginner', males)

openFemale = sortByDifficulty('Open', females)
advancedFemale = sortByDifficulty('Advanced', females)
intermediateFemale = sortByDifficulty('Intermediate', females)
beginnerFemale = sortByDifficulty('Beginner', females)

men = [
  openMale,
  advancedMale,
  intermediateMale,
  beginnerMale
]
women = [
  openFemale,
  advancedFemale,
  intermediateFemale,
  beginnerFemale
]
writeCSV('men_results.csv', men)
writeCSV('women_results.csv', women)
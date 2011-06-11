from lxml import etree
import re


xmlns="{http://www.mediawiki.org/xml/export-0.5/}"
outfile = open('test_out3.txt', 'w') 

class WikiArchive: #stores data on the whole archive 	
	def __init__(self):	
		self.pageCount = 0
		self.pageList = {}	
		self.contribCount = 0
		self.contribList = {}
	def TopContribs(self, kind, number): #returns the NUMBER contributors with the most edits or unique pages contributed  
		if kind == "edits":		
			sorted_list = sorted(self.contribList.values(), key=lambda contrib: contrib.editCount, reverse=True)
		elif kind == "pages":
			sorted_list = sorted(self.contribList.values(), key=lambda contrib: len(contrib.pageList), reverse=True)
		else:
			sorted_list = contribList.values()
		return sorted_list[0:number] 
	def TopPages(self, kind, number): #returns the NUMBER pages with the most edits or contributors 	
		if kind == "edits":
			sorted_list = sorted(self.pageList.values(), key=lambda page: page.revisionCount, reverse=True)
		elif kind == "contribs":
			sorted_list = sorted(self.pageList.values(), key=lambda page: page.ReturnContribCount(), reverse=True)
		else:
			sorted_list = pageList.values()
		return sorted_list[0:number]

class WikiPage: #stores data on a single WikiPage	
	def __init__(self, name):	
		self.title = name	
		self.revisionCount = 0
		self.revisionList = []
		self.codes = []
	def RevIncrement(self):
		self.revisionCount = self.revisionCount + 1
	def ReturnContribList(self): #returns a dictionary of contributors and the number of contributions of each
		contribDict = {}		
		for rev in self.revisionList:
			if rev.contributor in contribDict: 
				contribDict[rev.contributor] += 1
			else: 
				contribDict[rev.contributor] = 1
		return contribDict
	def ReturnContribCount(self): #returns total number of contributors
		contribList = []
		contribCount = 0
		for rev in self.revisionList:
			if rev.contributor not in contribList: 
				contribCount += 1
				contribList.append(rev.contributor)
		return contribCount


class WikiContributor:  		
	def __init__(self, handle):	
		self.name = handle	
		self.editCount = 1 #total individual edits
		self.contribDates = [] #datestamp of each edit
		self.contribIDs= [] #just to be sure, this will allow mapping contributors onto revisions, if need be 	
		self.pageCount = 1 #individual pages contributed to 
		self.pageList = {} #dictionary of pages and counts 


class WikiRevision:
	def __init__(self, title):	
		self.pageTitle = title #title of the page being revised
		self.contributor = '' #user name of the contributor responsible 
		self.comment = ''		
		self.revisionID = 0	
		self.year = 0
		self.month = 0 
		self.day = 0
		self.hour = 0
		self.minute = 0 
		self.second = 0
		self.text = ''
	def ReturnStringDate(self):
		dateString = str(self.month).zfill(2) + '/' + str(self.day).zfill(2) + '/' + str(self.year)
		return dateString
	def ReturnStringTime(self):
		timeString = str(self.hour).zfill(2) + ':' + str(self.minute).zfill(2) + ':' + str(self.second).zfill(2)
		return timeString
		

del_test = re.compile(r'The following discussion is an archived debate of the proposed deletion of the article below')

archive = WikiArchive()
for event, element in etree.iterparse('AprilAFD.xml', tag = xmlns + 'page'):
	currentPage = WikiPage(element[0].text)
	for line in element:					
		if line.tag == xmlns + 'revision':					
			currentRevision = WikiRevision(currentPage.title)
			currentRevision.contributor = line[2][0].text
			currentRevision.year = int(line[1].text[0:4])
			currentRevision.month = int(line[1].text[5:7])
			currentRevision.day = int(line[1].text[8:10])
			currentRevision.hour = int(line[1].text[11:13])
			currentRevision.second = int(line[1].text[14:16]) 			
			currentPage.RevIncrement()		
			currentPage.revisionList.append(currentRevision)
			if currentRevision.contributor in archive.contribList: #is this contributor in the list of all contributors in the archive?
				archive.contribList[currentRevision.contributor].editCount += 1
				if currentPage.title in archive.contribList[currentRevision.contributor].pageList: #is
					archive.contribList[currentRevision.contributor].pageList[currentPage.title] += 1
				else:
					archive.contribList[currentRevision.contributor].pageList[currentPage.title] = 1
			else: 
				archive.contribList[currentRevision.contributor] = WikiContributor(currentRevision.contributor)
				archive.contribList[currentRevision.contributor].pageList[currentPage.title] = 1
	archive.pageCount += 1
	archive.pageList[currentPage.title] = currentPage	
	del currentPage	
	element.clear()


#outfile.write("total pages = " + str(archive.pageCount) + '\n')
#for page in archive.pageList.itervalues():
#	outfile.write(page.title + ' with ' + str(page.revisionCount) + 'revisions and ' + str(page.ReturnContribCount()) + 'contributors' + '\n')	
#	contribs = page.ReturnContribList()
#	for element in contribs.items(): 
#		outfile.write("  " + element[0].encode('utf-8') + ":" + str(element[1]) + '\n')	
#	outfile.write('---\n')	
#for test in holdlist:
#	outfile.write(test.encode('utf-8'))

#for contrib in archive.contribList.itervalues():
#	outfile.write(contrib.name.encode('utf-8') + ' with ' + str(contrib.editCount) + ' edits to ' + str(len(contrib.pageList)) + ' pages.\n')
#	for page in contrib.pageList.iteritems(): 
#		outfile.write('   ' + page[0] + ': ' + str(page[1]) + ' edits\n')
#outfile.write("Top Contribs by Total Edits:\n")
#top_contribs = archive.TopContribs("edits", 200)
#for contrib in top_contribs:
#	outfile.write(contrib.name.encode('utf-8') + '\t' + str(contrib.editCount) + '\n')
#outfile.write("\nTop Contribs by Pages Edited:\n")
#top_contribs = archive.TopContribs("pages", 200)
#for contrib in top_contribs:
#	outfile.write(contrib.name.encode('utf-8') + '\t' + str(len(contrib.pageList)) + '\n')
#outfile.write("\nMost Edited Pages:\n")
#top_pages = archive.TopPages("edits", 200)
#for page in top_pages:
#	outfile.write(page.title + '\t' + str(page.revisionCount) + '\n')
#outfile.write("\nPages with most contributors:\n")
top_pages = archive.TopPages("contribs", 200)
for page in top_pages:
	outfile.write(page.title + '\t' + str(page.ReturnContribCount()) + '\n')
throwaway = raw_input("Wait to see if memory is really clear")
print throwaway	

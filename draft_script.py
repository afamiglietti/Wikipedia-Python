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
		



archive = WikiArchive()
for event, element in etree.iterparse('AprilAFD.xml', tag = xmlns + 'page'):
	currentPage = WikiPage(element[0].text)
	#These lines test for deletion or retention of the page. They are a terrible kludge, but they work... code reusers probably don't want these unless they are testing AfD pages (it looks for a pattern specific to them)
	speedyd_test = re.compile('The result was[^\']*[\']{3,3}(S|s)(P|p)(E|e)(E|e)(D|d)(Y|y) (D|d)(E|e)(L|l)(E|e)(T|t)[\']*')	
	speedyd = speedyd_test.search(element[-1][-1].text)	
	del_test = re.compile('The result was[^\']*[\']{3,3}(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)[\']*')	
	gone = del_test.search(element[-1][-1].text)
	merge_test = re.compile('The result was[^\']*[\']{3,3}[^\']*(M|m)(E|e)(R|r)(G|g)(E|e)[^\']*[\']{3,3}')
	merged = merge_test.search(element[-1][-1].text)
	withdrawn_test = re.compile('The result was[^\']*[\']{3,3}[^\']*(W|w)(I|i)(T|t)(H|h)(D|d)(R|r)(A|a)(W|w)[^\']*[\']{3,3}')
	withdrawn = withdrawn_test.search(element[-1][-1].text)	
	keep_test = re.compile('The result was[^\']*[\']{3,3}[^\']*(K|k)(E|e)(E|e|P|p)(P|p|T|t)[^\']*[\']{3,3}')
	retain = keep_test.search(element[-1][-1].text)	
	no_consensus_test = re.compile('The result was[^\']*[\']{3,3}(N|n)(O|o) (C|c)(O|o)(N|n)(S|s)(E|e)(N|n)(S|s)(U|u)(S|s)[\']*')	
	no_consensus = no_consensus_test.search(element[-1][-1].text)	
	redirect_test =	re.compile('The result was[^\']*[\']{3,3}[^\']*(R|r)(E|e)(D|d)(I|i)(R|r)(E|e)(C|c)(T|t)[^\']*[\']{3,3}')
	redirected = redirect_test.search(element[-1][-1].text)
	catch_all_test = re.compile('The result was[^\']*[\']{3,3}[^\']*[\']*')		
	n = catch_all_test.search(element[-1][-1].text)		
	if gone:
		currentPage.codes.append(gone.group())
		currentPage.codes.append("Deleted")
	elif speedyd: 
		currentPage.codes.append(speedyd.group())
		currentPage.codes.append("Speedy Deleted")
	elif merged: 	
		currentPage.codes.append(merged.group())
		currentPage.codes.append("Merged")
	elif retain: 
		currentPage.codes.append(retain.group())
		currentPage.codes.append("Kept")
	elif no_consensus:	
		currentPage.codes.append(no_consensus.group())
		currentPage.codes.append("No Consensus")
	elif redirected:
		currentPage.codes.append(redirected.group())
		currentPage.codes.append("Redirected")
	elif withdrawn:
		currentPage.codes.append(withdrawn.group())
		currentPage.codes.append("Withdrawn")
	elif n:	
		currentPage.codes.append(n.group())
		currentPage.codes.append("No string match")
	else:
		currentPage.codes.append(element[-1][-1].text)
		currentPage.codes.append("Cant find")	
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


outfile.write("page title,revision count,contributor count,status\n")
for page in archive.pageList.itervalues():
	if page.codes[1] == "No string match":	
		outfile.write(page.title + ',' + str(page.revisionCount) + ',' + str(page.ReturnContribCount()) + ',' + page.codes[0].encode('utf-8') + '\n')
	#outfile.write("STATUS: " + page.codes[1].encode('utf-8') + " string found " + page.codes[0].encode('utf-8') + '\n')	
	#contribs = page.ReturnContribList()
	#for element in contribs.items(): 
	#	outfile.write("  " + element[0].encode('utf-8') + ":" + str(element[1]) + '\n')	
	#outfile.write('---\n')	
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
#top_pages = archive.TopPages("contribs", 200)
#for page in top_pages:
#	outfile.write(page.title + '\t' + str(page.ReturnContribCount()) + '\n')
#throwaway = raw_input("Wait to see if memory is really clear")
#print throwaway	

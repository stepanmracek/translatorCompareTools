#! /usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from compareCommon import *

def getText(node):
	result = ''
	for t in node.itertext():
		if type(t) == str:
			result += t
	return result

def getDictFromTMX(xmlRootNode, language):
	langAttr = '{http://www.w3.org/XML/1998/namespace}lang'
	result = {}

	try:
		for tu in xmlRootNode.iter('tu'):
			tuid = tu.attrib['tuid']

			for tuv in tu.iter('tuv'):
				if tuv.attrib[langAttr] == language:
					text = getText(tuv)
					result[tuid] = text
	except Exception:
		sys.exit("Problem occured when parsing source language in original file.")

	return result

def getNotesFromTMX(xmlRootNode):
	result = {}
	try:
		for tu in xmlRootNode.iter('tu'):
			tuid = tu.attrib['tuid']

			noteText = ''
			for note in tu.iter('note'):
				noteText += getText(note)
			if noteText != '':
				result[tuid] = noteText

	except Exception:
		sys.exit("Problem occured when parsing source language in original file.")

	return result


if __name__ == "__main__":
	ok = checkParams(sys.argv,6)
	if not ok:
		sys.exit('Usage:\n' + sys.argv[0] + ' source_language target_language original_file corrected_file output.[csv|xlsx|html]')

	sourceLanguage = sys.argv[1]
	targetLanguage = sys.argv[2]

	originalTree = ET.parse(sys.argv[3])
	originalRoot = originalTree.getroot()

	correctedTree = ET.parse(sys.argv[4])
	correctedRoot = correctedTree.getroot()

	englishDict = getDictFromTMX(originalRoot, sourceLanguage)
	originalDict = getDictFromTMX(originalRoot, targetLanguage)
	correctedDict = getDictFromTMX(correctedRoot, targetLanguage)
	notesDict = getNotesFromTMX(correctedRoot)

	result = compare(englishDict, originalDict, correctedDict, notesDict)
	
	if sys.argv[5].lower().endswith(".xlsx"):
		excelOutput(result, sys.argv[5])
	elif sys.argv[5].lower().endswith(".html"):
		htmlOutput(result, sys.argv[5])
	else:
		csvOutput(result, sys.argv[5])

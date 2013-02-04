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


if __name__ == "__main__":
	ok = checkParams(sys.argv)
	if not ok:
		sys.exit('Usage:\n' + sys.argv[0] + ' original_file corrected_file output.[csv|xlsx|html]')

	originalTree = ET.parse(sys.argv[1])
	originalRoot = originalTree.getroot()

	correctedTree = ET.parse(sys.argv[2])
	correctedRoot = correctedTree.getroot()

	englishDict = getDictFromTMX(originalRoot, 'en')
	originalDict = getDictFromTMX(originalRoot, 'tr')
	correctedDict = getDictFromTMX(correctedRoot, 'tr')
	notesDict = {}

	result = compare(englishDict, originalDict, correctedDict, notesDict)
	
	if sys.argv[3].lower().endswith(".xlsx"):
		excelOutput(result, sys.argv[3])
	elif sys.argv[3].lower().endswith(".html"):
		htmlOutput(result, sys.argv[3])
	else:
		csvOutput(result, sys.argv[3])

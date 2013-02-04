#! /usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
from compareCommon import *

#nsPrefix = "{urn:oasis:names:tc:xliff:document:1.2}"

def processXLF(root, desiredTag, targetDict):
	try:
		for fileNode in root:
			filename = fileNode.attrib['original']
			for body in fileNode:
				if (body.tag.endswith("body")):
					for transUnit in body:
						key = filename + '-' + transUnit.attrib['id']
						for child in transUnit:
							if (child.tag.endswith(desiredTag)):
								result = ''
								for text in child.itertext():
									if type(text) == str:
										result += text
								targetDict[key] = result;
	except Exception:
		return False
	
	return True

if __name__ == "__main__":

	ok = checkParams(sys.argv, 4)
	if not ok:
		sys.exit('Usage:\n' + sys.argv[0] + ' original_file corrected_file output.[csv|xlsx|html]')

	originalTree = ET.parse(sys.argv[1])
	originalRoot = originalTree.getroot()

	correctedTree = ET.parse(sys.argv[2])
	correctedRoot = correctedTree.getroot()

	englishDict = {}
	originalDict = {}
	correctedDict = {}
	notesDict = {}

	ok = processXLF(originalRoot, "source", englishDict)
	if not ok:
		sys.exit("Problem occured when parsing source language in original file.")

	ok = processXLF(originalRoot, "target", originalDict)
	if not ok:
		sys.exit("Problem occured when parsing target language in original file.")

	ok = processXLF(correctedRoot, "target", correctedDict)
	if not ok:
		sys.exit("Problem occured when parsing target language in corrected file.")

	ok = processXLF(correctedRoot, "note", notesDict)
	if not ok:
		sys.exit("Problem occured when parsing notes in corrected file.")

	ok = checkDictKeys([englishDict, originalDict, correctedDict])
	if not ok:
		sys.exit("The original and corrected file contents do not match.")

	result = compare(englishDict, originalDict, correctedDict, notesDict)
	
	if sys.argv[3].lower().endswith(".xlsx"):
		excelOutput(result, sys.argv[3])
	elif sys.argv[3].lower().endswith(".html"):
		htmlOutput(result, sys.argv[3])
	else:
		csvOutput(result, sys.argv[3])

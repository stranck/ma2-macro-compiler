from bs4 import BeautifulSoup
from bs4 import ResultSet, Tag
import argparse
import datetime

COMPILE = True

class MacroLine:
	delay: float = 0
	lineNo: int = 0
	disabled: bool = False
	text: str = None
	info: str = None
	
	def fromXml(tag: Tag):
		line = MacroLine()
		line.lineNo = tag.get("index")
		if (tag.has_attr("delay")):
			line.delay = float(tag.get("delay"))
		if (tag.has_attr("disabled")):
			line.disabled = tag.get("disabled").lower() == "true"
		text: Tag = tag.find("text")
		if (text is not None):
			line.text = text.getText()
		info: Tag = tag.find("info")
		if (info is not None):
			line.info = info.getText()
		return line
	
	def fromString(value: str, lineNo: int):
		line = MacroLine()
		line.lineNo = lineNo
		
		commentSp = value.split("//")
		if (len(commentSp) > 1):
			commentSp = ["//".join(commentSp[:-1]), commentSp[-1]]
		delaySp = commentSp[0].split("!")
		if (len(delaySp) > 1):
			delaySp = ["!".join(delaySp[:-1]), delaySp[-1]]
		text = delaySp[0].strip()
		
		if (len(commentSp) > 1):
			line.info = commentSp[1].strip()
		if (len(delaySp) > 1):
			line.delay = float(delaySp[1].strip())
		
		if (text.startswith("#")):
			text = text[1:]
			line.disabled = True
		line.text = text
		return line
	
	def toXml(self, soup: BeautifulSoup) -> Tag:
		tagAttrs = {"index": self.lineNo}
		if (self.delay > 0):
			tagAttrs["delay"] = self.delay
		if (self.disabled):
			tagAttrs["disabled"] = "true"
		tag = soup.new_tag("Macroline", **tagAttrs)
		if (self.text is not None):
			textTag = soup.new_tag("text")
			textTag.string = self.text
			tag.insert(1, textTag)
		if (self.info is not None):
			infoTag = soup.new_tag("info")
			infoTag.string = self.info
			tag.insert(2, infoTag)
		return tag
	
	def toCodeString(self) -> str:
		t = f"#" if self.disabled else ""
		if (self.text is not None):
			t += f" {self.text}"
		if (self.delay > 0):
			t += f" !{self.delay}"
		if (self.info is not None):
			t += f" //{self.info}"
		return t.strip()
	
	def __str__(self) -> str:
		return f"MacroLine{{lineNo={self.lineNo}, delay={self.delay}, disabled={self.disabled}, info={self.info}, val={self.text}}}"

def decompile(fileName: str) -> str:
	with open(fileName, 'r') as f:
		#data = f.read()
		data = f.readlines()
	data = "\n".join(data[1:])
	macroFile = BeautifulSoup(data, "xml")
	#for e in macroFile:
	#    print("Aaaaa")
	#    if isinstance(e, ProcessingInstruction):
	#        print("suca")
	#        e.extract()
	#        break
	textMacros: list[str] = []
	macros: ResultSet = macroFile.find_all("Macro")
	macro: Tag
	for macro in macros:
		lines = macro.find_all("Macroline")
		line: Tag
		parsedLines: list[MacroLine] = []
		for line in lines:
			parsedLines.append(MacroLine.fromXml(line))
		parsedLines.sort(key=lambda l: l.lineNo)
		textLines = [l.toCodeString() for l in parsedLines]
		textMacros.append(f"\n_macro \"{macro.get('name')}\" {{\n\t" + "\n\t".join(textLines) + "\n}\n")
	return "\n".join(textMacros)

			
	
def compile(fileName: str) -> str:
	with open(fileName, 'r') as f:
		data = f.readlines()
	baseXml = f'<MA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.malighting.de/grandma2/xml/MA" xsi:schemaLocation="http://schemas.malighting.de/grandma2/xml/MA http://schemas.malighting.de/grandma2/xml/3.9.60/MA.xsd" major_vers="3" minor_vers="9" stream_vers="60"><Info datetime="{datetime.datetime.now().replace(microsecond=0).isoformat()}" showfile="" /></MA>'
	macroFile = BeautifulSoup(baseXml, "xml")
	maTag = macroFile.find("MA")
	macroLine = 0
	macroIndex = 0
	currentMacroTag: Tag = None
	line: str
	for line in data:
		line = line.strip()
		if currentMacroTag is None:
			if line.startswith("_macro") and line.endswith("{"):
				macroName = line.split("_macro")[1].split("{")[0].strip()
				if macroName.startswith('"'):
					macroName = macroName[1:]
				if macroName.endswith('"'):
					macroName = macroName[:-1]
				currentMacroTag = Tag(builder=macroFile.builder, name="Macro", attrs={"index": macroIndex, "name": macroName})
				macroLine = 0
		else:
			if line == "}":
				maTag.insert(macroIndex + 1, currentMacroTag)
				currentMacroTag = None
				macroIndex += 1
			else:
				line: MacroLine = MacroLine.fromString(line, macroLine)
				currentMacroTag.insert(macroLine, line.toXml(macroFile))
				macroLine += 1
	return macroFile.prettify()

if __name__ == "__main__":
	parser = argparse.ArgumentParser("GrandMA2 macro xml compiler/decompiler, made by https://stranck.ovh")
	parser.add_argument('-f', '--file', nargs=1, required=True)
	parser.add_argument('-o', '--output', nargs=1, required=False)
	parser.add_argument('-c', '--compile', action='store_true', required=False)
	parser.add_argument('-d', '--decompile', action='store_true', required=False)
	args = parser.parse_args()

	if args.compile:
		output = compile(args.file[0])
	elif args.decompile:
		output = decompile(args.file[0])
	else: 
		print("You have to chose if you want to compile or decompile!")
		exit(1)

	if (args.output is not None):
		with open(args.output[0], 'w') as f:
			f.write(output)
	else:
		print(output)
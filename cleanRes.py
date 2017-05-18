# !/usr/bin/python3

from xml.dom.minidom import parse
import xml.dom.minidom

import os

currentPath = os.getcwd()
print(currentPath)

# 分析文件解析
DOMTree = xml.dom.minidom.parse(currentPath + "/file/AndroidLintUnusedResources.xml")
collection = DOMTree.documentElement
problems = collection.getElementsByTagName("problem")

filePaths = os.listdir(currentPath + "/res")

result = {}
for filePath in filePaths:
    result[filePath] = []

for problem in problems:
    itemFilePath = problem.getElementsByTagName("file")[0].childNodes[0].data.split("/")[-2]
    entry_point = problem.getElementsByTagName("entry_point")[0]
    if itemFilePath.startswith("drawable"):
        picName = entry_point.getAttribute("FQNAME").split("/")[-1]
        #         处理图片 这里存储名字
        result.get(itemFilePath).append(picName)
    elif itemFilePath.startswith("values"):
        strLine = currentLine = problem.getElementsByTagName("line")[0].childNodes[0].data
        # 处理字符串 这里存储 需要处理的字符串所在行数
        result.get(itemFilePath).append(strLine)

print(result)

for itemDir in result:
    if itemDir.startswith("drawable"):
        for picName in result.get(itemDir):
            if os.path.exists(currentPath + "/res/" + itemDir + "/" + picName):
                print("删除无用资源" + picName)
                os.remove(currentPath + "/res/" + itemDir + "/" + picName)
    elif itemDir.startswith("values"):
        print(result.get(itemDir))
        strFile = open(currentPath + "/res/" + itemDir + "/strings.xml", "r", encoding="utf-8")
        tmpLines = strFile.readlines()

        for itemStrFile in result.get(itemDir):
            tmpLines[int(itemStrFile)-1] = "\n"
        newFile = open(currentPath + "/res/" + itemDir + "/strings.xml", "w", encoding="utf-8")
        newFile.write("".join(tmpLines))
        newFile.close()


print("清理完成")

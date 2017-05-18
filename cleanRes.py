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

defaultLines = []
defaultFile = open(currentPath + "/res/values/strings.xml", "r", encoding="utf-8")
for itemDefaultLine in defaultFile.readlines():
    defaultLines.append(itemDefaultLine)

zhLines = []
zhFile = open(currentPath + "/res/values-zh-rCN/strings.xml", "r", encoding="utf-8")
for itemZhline in zhFile.readlines():
    zhLines.append(itemZhline)

for problem in problems:
    # 是否为无用的资源
    problem_class = problem.getElementsByTagName("problem_class")[0]
    # 文件类型 是字符串还是图片
    entry_point = problem.getElementsByTagName("entry_point")[0]
    if problem_class.childNodes[0].data == "Unused resources":
        currentLine = problem.getElementsByTagName("line")[0].childNodes[0].data
        # 如果是字符串 且是默认字符串
        if entry_point.getAttribute("FQNAME").endswith("/values/strings.xml"):
            # 为了保持多次运行处理 不会误删除 设置值为 \n
            defaultLines[int(currentLine)] = "\n"
        # 处理图片
        elif entry_point.getAttribute("FQNAME").endswith(".png"):
            currentImgName = entry_point.getAttribute("FQNAME").split("/")[-1]
            if os.path.exists(currentPath + "/res/drawable-mdpi/" + currentImgName):
                print("删除无用资源" + currentImgName)
                os.remove(currentPath + "/res/drawable-mdpi/" + currentImgName)
        # 处理中文字符串
        if entry_point.getAttribute(
                "FQNAME") == "file://$PROJECT_DIR$/../XCTSPProxy/src/main/res/values-zh-rCN/strings.xml":
            zhLines[int(currentLine) - 1] = "\n"

s = ''.join(defaultLines)
valueStr = open(currentPath + "/res/values/strings.xml", "w", encoding="utf-8")
valueStr.write(s)
valueStr.close()

zhResult = ''.join(zhLines)
zhStr = open(currentPath + "/res/values-zh-rCN/strings.xml", "w", encoding="utf-8")
zhStr.write(zhResult)
zhStr.close()

print("清理完成")

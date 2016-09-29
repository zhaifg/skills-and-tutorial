#coding:utf-8
from xml.etree import ElementTree

with open('a.xml','rt') as f:
    tree = ElementTree.parse(f)


# 遍历所有的节点
for node in tree.iter():
    ## node.tag是节点的标签名, attrib是标签的属性
    # 通过attrib是一个字典,
    print node.tag, node.attrib
    print node.attrib.get('name')
print "------------"

for node in tree.iter('service'):
    # print node.tag, node.attrib
     print node.attrib.get('name')

## findall查找接到 目录结构类似于linux的结构
##
chains = tree.findall("service/chain")
print chains

## findall,iter放回的是一个Element对象

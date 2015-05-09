#!/usr/bin/python
import sys
import os
import CppHeaderParser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False)
parser.add_option("-c", "--class-name", dest="classname")
parser.add_option("-t", "--target-path", dest="targetpath")
parser.add_option("-s", "--source-object", dest="sourceobject")
parser.add_option("-e", "--header-suffix", dest="headersuffix")
parser.add_option("-v", "--only-virtual", dest="onlyvirtual", default="true")
parser.add_option("-p", "--public", dest="public", default="true")
parser.add_option("-r", "--protected", dest="protected", default="false")
parser.add_option("-i", "--private", dest="private", default="false")
(options, args) = parser.parse_args()

newFileName = str(options.classname).lower() + '.' + options.headersuffix

if options.dryrun:
    print newFileName + ',openeditor\n'
    exit(0)

accessors = []
if options.public == 'true':
    accessors.append('public')
if options.protected == 'true':
    accessors.append('protected')
if options.private == 'true':
    accessors.append('private')

try:
    cppHeader = CppHeaderParser.CppHeader(options.sourceobject)
except CppHeaderParser.CppParseError as e:
    print(e)
    sys.exit(1)

newFilePath = options.targetpath + '/' + newFileName
newFile = open(newFilePath, 'w')
newFile.write('#ifndef %s_H\n' % str(options.classname).upper())
newFile.write('#define %s_H\n' % str(options.classname).upper())

newFile.write('\n#include "gmock/gmock.h"\n')
newFile.write('#include "%s"\n' % os.path.basename(options.sourceobject))

for className in cppHeader.classes:
    if '::' in className:
        continue
    newFile.write('\n/**\n');
    newFile.write(' * @brief Automatically generated Mock object for %s\n' % className);
    newFile.write(' */\n');
    newFile.write('class %s : public %s\n' %(options.classname, className))
    newFile.write('{\n')
    newFile.write('public:\n')
    
    classObj = cppHeader.classes[className]
    for accessor in accessors:
        for method in classObj["methods"][accessor]:
            if method['static'] or method['constructor'] or method['destructor']:
                continue
            if options.onlyvirtual == 'true' and not method['virtual']:
                continue

            mockMethod = 'MOCK_CONST_METHOD' if method['const'] else 'MOCK_METHOD'
            paramsCount = len(method['parameters'])
            methodName = method['name']
            rtnType = method['rtnType']
            params = []
            for parameter in method['parameters']:
                params.append('%s %s' % (parameter['type'], parameter['name']))
            newFile.write('    %s%s(%s, %s(%s));\n' %(mockMethod, paramsCount, methodName, rtnType, ', '.join(params)))

    newFile.write('};\n')

newFile.write('\n#endif // %s_H\n' % str(options.classname).upper())
newFile.close()

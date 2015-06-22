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
parser.add_option("-E", "--source-suffix", dest="sourcesuffix")
parser.add_option("-v", "--only-virtual", dest="onlyvirtual", default="true")
parser.add_option("-p", "--public", dest="public", default="true")
parser.add_option("-r", "--protected", dest="protected", default="false")
parser.add_option("-i", "--private", dest="private", default="false")
parser.add_option("-S", "--faster-build", dest="fasterbuild", default="false")
(options, args) = parser.parse_args()

newFileNameH = str(options.classname).lower() + '.' + options.headersuffix
newFileNameCpp = str(options.classname).lower() + '.' + options.sourcesuffix

if options.dryrun:
    print newFileNameH + ',openeditor\n'
    if options.fasterbuild:
        print newFileNameCpp + ',openeditor\n'
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

newFilePathH = options.targetpath + '/' + newFileNameH
newFileH = open(newFilePathH, 'w')
newFileH.write('#ifndef %s_H\n' % str(options.classname).upper())
newFileH.write('#define %s_H\n' % str(options.classname).upper())
newFileH.write('\n#include "gmock/gmock.h"\n')
newFileH.write('#include "%s"\n' % os.path.basename(options.sourceobject))

for className in cppHeader.classes:
    if '::' in className:
        continue
    newFileH.write('\n/**\n');
    newFileH.write(' * @brief Automatically generated Mock object for %s\n' % className);
    newFileH.write(' */\n');
    newFileH.write('class %s : public %s\n' %(options.classname, className))
    newFileH.write('{\n')
    newFileH.write('public:\n')
    if options.fasterbuild:
        newFileH.write('    %s();\n' % options.classname)
        newFileH.write('    virtual ~%s();\n\n' % options.classname)
    
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
            newFileH.write('    %s%s(%s, %s(%s));\n' %(mockMethod, paramsCount, methodName, rtnType, ', '.join(params)))

    newFileH.write('};\n')

newFileH.write('\n#endif // %s_H\n' % str(options.classname).upper())
newFileH.close()

if options.fasterbuild:
    newFilePathCpp = options.targetpath + '/' + newFileNameCpp
    newFileCpp = open(newFilePathCpp, 'w')
    newFileCpp.write('#include "%s"\n\n' % newFileNameH)
    newFileCpp.write('%s::%s()\n{\n}\n\n' % (options.classname, options.classname))
    newFileCpp.write('%s::~%s()\n{\n}\n' % (options.classname, options.classname))
    newFileCpp.close()

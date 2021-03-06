# Dev: 3mjms
#
# helper class to save results in mongodb
# save : saves to a mongodb
#
from pprint import pprint as pp
import json
import os

import io


class IO_json(object):
    # get the file path and file name
    # append '/' to file path to complete the path folder
    # append .json as file extension
    def __init__(self, fPath, fName):
        self.fPathName = fPath + '/' + fName + '.json'

    def save(self, data):
        if os.path.isfile(self.fPathName):
            # append existing file
            mode = 'a'
        else:
            # create new file
            mode = 'w'

        with io.open(self.fPathName, mode, encoding='utf-8') as outFile:
            outFile.write(unicode(json.dumps(data, ensure_ascii=False)))  # python 2.7
            # new line to keep order
            outFile.write(u'\u000A')
            # outFile.write(json.dumps(data, ensure_ascii=False))  # python 3
            outFile.close()

    def savePP(self, data):
        if os.path.isfile(self.fPathName):
            # append existing file
            mode = 'a'
        else:
            # create new file
            mode = 'w'
        with open(self.fPathName, mode) as outFile:
            pp(data, stream=outFile)

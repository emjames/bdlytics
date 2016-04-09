# Dev: 3mjms
#
# helper class to save results in mongodb
# save : saves to a mongodb
#

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
            # outFile.write(json.dumps(data, ensure_ascii=False))  # python 3

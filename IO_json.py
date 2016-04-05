# Dev: 3mjms
#
# helper class to save results in mongodb
# save : saves to a mongodb
#

import json


class IO_json(object):
    # get the file path and file name
    # append '/' to file path to complete the path folder
    # append .json as file extension
    def __init__(self, fPath, fName):
        self.fPathName = fPath + '/' + fName + '.json'

    def save(self, data):
        # w+ trunkates the file
        with open(self.fPathName, 'w+') as outFile:
            json.dump(data, outFile)

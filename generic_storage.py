import os
import sys
from typing import Generic
import yaml

from pycti import get_config_variable

class GenericStorageHelper:
    def __init__(self, root_storage_location, root_queue_location, dir):
        self.root_storage_location = root_storage_location
        self.root_queue_location = root_queue_location
        self.dir = dir

    def store(self, file_name, data):
        endpoints = [self.root_storage_location, self.root_queue_location]
        for location in endpoints:
            file_path = os.path.join(os.path.join(location, self.dir), file_name)
            os.makedirs(os.path.join(location, self.dir), exist_ok=True)
            with open(file_path, "wb") as file:
                file.write(data)
        return(file_name)

    def does_next_file_exist(self):
        location = os.path.join(self.root_queue_location, self.dir)
        return(len([f for f in os.listdir(location) if (os.path.isfile(os.path.join(location,f)) and str(f)[0] != '.')])) #check if there is another, non-hidden, file in the queue

    def pick_up_next(self):
        file_ref = self.get_next_file_ref()
        with open(file_ref, 'rb') as file:
            data = file.read()
        # SPACE TO ADD ERROR CHECKING AGAINST FILE <TO DO>
        os.remove(file_ref)
        return(data)

    def get_next_file_ref(self):
        location = os.path.join(self.root_queue_location, self.dir)
        next_file = [f for f in os.listdir(location) if (os.path.isfile(os.path.join(location, f)) and str(f)[0] != '.')][0] #return first file found in doirectory that doesnt start with a '.' (ie not a hidden file)
        next_file_ref = os.path.join(location, next_file)
        return(str(next_file_ref))

    def remove_file_by_ref(self, file_ref):
        os.remove(file_ref)

if __name__ == "__main__":
    GenericStorageHelper(sys.argv[1], sys.argv[2], sys.argv[3])


import base64
import hashlib
import json

from fuzzywuzzy import process

class ApartmentDatabase:
    def __init__(self, path):
        self.path = path

        # TODO: do some checking here if the file exists or if it is wrong format
        with open(path, "r") as f:
            self.data = json.load(f)

        # mapping of apartment number to row number
        self.apt_to_row_num = {row["apt"]: i for i, row in enumerate(self.data)}
    
    def get_row_num_from_apt(self, apt):
        if apt in self.apt_to_row_num:
            return self.apt_to_row_num[apt]
        print(f"error: room '{apt}' does not exist")
        quit()


    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def save(self):
        with open(self.path, "w+") as f:
            f.write(json.dumps(self.data))

    # returns the list of rows in descending order of similarity along with its similarity value
    def query(self, query, limit=5):
        results = process.extract(str(query), self.data, limit=limit)
        print(f"query: {query}")
        print("results:")
        for result in results:
            print(result)
        return results

    def remove_person(self, key, apt, name):
        row_num = self.get_row_num_from_apt(apt)
        visitors = self.data[row_num][key]

        if name in visitors:
            visitors.remove(name)
            self.data[row_num][key] = visitors
        else:
            print(f":: error: '{name}' not in '{key}' for '{apt}'")
            quit()

    def add_person(self, key, apt, name):
        row_num = self.get_row_num_from_apt(apt)

        if name not in self.data[row_num][key]:
            self.data[row_num][key].append(name)
        else:
            print(f"duplicate name in '{key}' but ignoring for now") # TODO: make this edge case better

    def add_visitor(self, apt, name):
        self.add_person("visitors", apt, name)

    def remove_vistor(self, apt, name):
        self.remove_person("visitors", apt, name)
    
    def add_tenant(self, apt, name):
        self.add_person("tenants", apt, name)

    def remove_tenant(self, apt, name):
        self.remove_person("tenants", apt, name)

# TODO: Implement this fully
class CredentialsDatabase:
    def __init__(self, path):
        self.path = path
        with open(path, "r") as f:
            self.data = json.load(f)

    def hash(self, passwd):
        return base64.b64encode(hashlib.scrypt(
            password=passwd,
            salt=b"salt",
            n=1<<15,            # Hardness factor
            r=8,                # block size
            p=1,                # parallelization factor
            maxmem=2147483647,  # ~2.15 GB
        ))
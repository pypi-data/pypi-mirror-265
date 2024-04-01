import pickle,csv,io, re
from RTSDataBase.typotest import TypoTest
from .exceptions import *
# <...> = required
# [...] = optional

class RTSDB:
    def __init__(self, filename):
        self.filename = filename + ".rtsdb"
        self.data = []
        self.load()

    def load(self):
    
        try:
            with open(self.filename, 'rb') as f:
                self.header,self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = []
            self.header = None

    def dump(self):
        return (self.header,self.data)

    def dump_data(self):
        return self.data
    
    def dump_header(self):
        return self.header
    
    def formated_dump(self, format):
        #self.data
        if format == "csv":
            fieldnames = [key for key in self.data[0].keys() if key != '__id']
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            data_without_id = [{k: v for k, v in item.items() if k != '__id'} for item in self.data]
            writer.writerows(data_without_id)
            return output.getvalue()

    # Used only by Internal functions  
    def validate_types(self, field, record):
        type_map = {
            '__any': None,
            'nostr': (str, type(None)),
            'nolist': (list, type(None)),
            'nodict': (dict, type(None)),
            'nobool': (bool, type(None)),
            'nofloat': (float, type(None)),
            'noint': (int, type(None)),
            'str': str,
            'list': list,
            'dict': dict,
            'bool': bool,
            'float': float,
            'int': int
        }

        field_type = self.header['format'][self.header['fields'].index(field)]

        if type == '__any':
            print(f"Field {field} is type any")
            return

        if not isinstance(record[field], type_map[field_type]):
            raise InvalidType(f'⛔ InvalidType: "{field}" does not match typerule "{field_type}" in: {record}')
        return

    # Used only by Internal functions
    def validate_create(self, record):
        if not isinstance(record, dict):
            raise ValueError(f"⚠️  ValueError: not a dict in {record}")

        # Check if there are extra fields in the record
        if not set(record.keys()).issubset(set(self.header["fields"])):
            raise FieldsNotInHeader(f'⛔ FieldsNotInHeader: The record contains fields that are not in the header {record}')

        for field, type, state in zip(self.header["fields"], self.header['format'], self.header['states']):
            if field == '__id':
                continue
            if state != 'loose':
                if field not in record:
                    raise MissingField(f'⛔ MissingField: "{field}" is missing in: {record}')   
                else:
                    self.validate_types(field, record)
    
    # Used only by Internal functions
    def validate_update(self, record):
        if not isinstance(record, dict):
            return False

        for field, value in record.items():
            if field not in self.header["fields"]:
                return False
            type = self.header["format"][self.header["fields"].index(field)]
            return self.validate_types(field, record)
        return True

    # self.create(<{"fieldname":knowndata,...}>)
    # Does: creates a new record with the given data
    # Input: record = {fieldname:knowndata,...}
    # Does not return anything
    def create(self, record):
        try:
            if self.header is None:
                raise NotImplementedError(r"⚠️ ERROR: No header set. 'Database.setHeader({...})'")

            unique_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in  ["unique", "ul"]]
            index_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state == "index"]
            print("Unique fields: ",unique_fields)
            print("Index fields: ",index_fields)
            for ex_record in self.data:
                for u_field in unique_fields:
                    if record.get(u_field) is not None and record.get(u_field) == ex_record[u_field]:
                        raise ValueError(f"⚠️  Warning: Record with >>> {u_field}={record[u_field]} <<< already exists")

                for i_field in index_fields:
                    if record.get(i_field) is not None and record.get(i_field) == ex_record[i_field]:
                        raise ValueError(f"⚠️  Warning: Record with the value >>> {record[i_field]} <<< already exists in index field")
            
            self.validate_create(record)
            
            existing_ids = [record["__id"] for record in self.data]
            new_id = 1 if not existing_ids else max(existing_ids) + 1
            record["__id"] = new_id

            self.data.append(record)
            self.save()
        except NotImplementedError as e:
            print(e)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)

    def update(self, selector, field, value):
        #print("Updating > Selector: ",selector, "Field: ",field, "Value: ",value)
        #USER_DB.update({"clientID": "+Vq0tFnnt52kpy4SKhEIP4zfrJ2Rj5Xl"}, "email", "adm@randomtime.tv")
        #USER_DB.update({"clientID": "+Vq0tFnnt52kpy4SKhEIP4zfrJ2Rj5Xl"}, "accountlinks:twitch.client.access_token", "8ewa16w28a1ecf21aef2ae4fc112ae")
        
        try:
            

            record_to_update = None
            found = False
            for record in self.data:
                if found:
                    break
                for f, v in selector.items():
                    if record.get(f) == v:
                        record_to_update = record
                        found = True
                        break
            if record_to_update is None:
                raise ValueError("⚠️  ValueError: No record found to update")
            if ":" in field:
                field, path = field.split(":")
                if isinstance(record_to_update[field], dict):
                    print("Field is dict")
                    if "." in path:
                        path = path.split(".")
                    else:
                        path = [path]

                    def roam_and_replace(dic, path, replacewith):
                        if len(path) == 1:
                            dic[path[0]] = replacewith
                        else:
                            if not dic.get(path[0]):
                                dic[path[0]] = {}
                                roam_and_replace(dic[path[0]], path[1:], replacewith)
                        return dic   
                        
                    print(path)
                    value = roam_and_replace(record_to_update[field], path, value)
                    print("Final Value: ",value)


    
            modular_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state == "modular"]
            unique_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in ["unique"]]
            locked_fields = [field for field, state in zip(self.header["fields"], self.header["states"]) if state in ["locked", "index"]]
    
            #print("valuetype: ",str(type(value)))
            #print("fieldtype: ",str(type(field)))
            if field not in locked_fields and field in self.header["fields"] and self.validate_update({field:value}):
                if field in unique_fields and value is not None and any(record.get(field) == value for record in self.data if record is not record_to_update):
                    
                    raise DataNotUnique(f'⛔ DataNotUnique: "{field}" must contain a unique value among all records.')
                print(f"Updating field {field} to value {value}")
                record_to_update[field] = value
            else:
                if field in locked_fields:
                    raise LockedField(f'🔒 LockedField: "{field}" can not be updated.')
                elif self.validate_update({field:value}):
                    raise InvalidField(f'⛔ InvalidField: "{field}" is not in the header')
                elif not any(record.get(field) == value for record in self.data if record is not record_to_update):
                    raise DataNotUnique(f'⛔ DataNotUnique: "{field}" must contain a unique value among all records.')
                else:
                    raise Exception('⚠️  UnknownError: You are not suposed to encounter this message, may report this issue to the developer.')
            self.save()
        except Exception as e:
            print(e)


    # Example: self.setHeaders({"fields":["prename"], "format":["str"], "states":[""]})
    # Does: sets the header of the database
    # Input: header = {"fields":[fieldname], "format":[format], "states":[state]}
    # fields = fieldname
    # format = str, int, float, bool, list, dict
    # states = locked, unique, modular, index, loose, ul (unique and locked)
    #       locked = field can not be changed after creation
    #       unique = field must be unique
    #       modular = field can be updated at any time
    #       index = field is indexed
    #       loose = field can be missing
    #       ul = field must be unique and is locked after creation
    def setHeader(self, header):
        if self.header is None:
            self.header = header
        else:
            for field, format, state in zip(header["fields"], header["format"], header["states"]):
                if field not in self.header["fields"]:
                    self.header["fields"].append(field)
                    self.header["format"].append(format)
                    self.header["states"].append(state)
        if "__id" not in self.header["fields"]:
            self.header["fields"].insert(0, "__id")
            self.header["format"].insert(0, "int")
            self.header["states"].insert(0, "index")
        self.save()

    # Example: self.delete(self.read({"fieldname":"exactdata"}, "__id")
    # Does: deletes a record with the given __id
    
    def delete(self, id):
        self.data = [record for record in self.data if record.get('__id') != id]
        self.save()

    # self.find("query", ["fieldname"=string], [case_sensitiv=<True|False>], [allow_typo=<True|False>])
    # Does: lookup all records that match the query
    # Input: <query = string>, [fieldname = string], [case_sensitiv = boolean], [allow_typo = boolean]
    # Returns: list of matching records

    def find(self, query, fieldname="__any", case_sensitiv=True, allow_typo=False):
        print("Finding > Query: ",query, "Fieldname: ",fieldname, "Case sensitiv: ",case_sensitiv, "Allow typo: ",allow_typo)
        matches = []
        for record in self.data:
            # fieldname = "__any" means that the query will be searched in all fields except "__id"
            # if fieldname is not "__any" the query will be searched in the specified field except "__id"
            if fieldname == "__any":
                fields = [field for field in record if field != "__id"]
            elif fieldname == "__id":
                raise ValueError("⚠️  ValueError: Fieldname '__id' is not allowed")
            else:
                fields = [fieldname]

            for field in fields:
                value = str(record[field])
                if not case_sensitiv:
                    value = value.lower()
                    query = query.lower()

                if not allow_typo:
                    if re.search(f".*{query}.*", value):
                        matches.append(record)
                elif allow_typo:
                    if TypoTest(query, value) < 3:
                        matches.append(record)

        return matches
    
    # Example: self.exists({"fieldname": "exactvalue"})
    # Does: tests if it can find a record with the exact fieldname and the exact value
    # Input: selector = {fieldname:exactvalue}
    # Returns: boolean
    def exists(self, selector):
        for record in self.data:
            if all(record.get(k) == v for k, v in selector.items()):
                return True
        return False
    
    # Example: self.read(<{"fieldname":"exactdata"}>, <"fieldname2"=string>)
    # Does: lookup a record like self.exists() but returns the value of the fieldname2
    # Input: selector = {fieldname:exactdata}, field = fieldname_to_return
    # Returns: value of fieldname2
    def read(self, selector, field="__any"):
        for record in self.data:
            if all(record[k] == v for k, v in selector.items()):
                if field == "__any":
                    return record
                elif ":" in field:
                    field, path = field.split(":")
                    content = record.get(field)
                    if isinstance(record[field], dict):
                        if "." in path:
                            path = path.split(".")
                        else:
                            path = [path]
                    def roam(d,path):
                        if len(path) == 1:
                            return d.get(path[0])
                        elif len(path) > 1 and d.get(path[0]):
                            return roam(d.get(path[0]), path[1:])
                    return roam(content, path)
                else:
                    return record.get(field)
        return None
    
    # Does not need to be manually called
    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump((self.header,self.data), f)
            

    
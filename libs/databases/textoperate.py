import json
import re


class TextOperator:
    def __init__(self, filepath: str):
        self.filepath = filepath

    """ Count """

    def text_count(self, condition: dict):
        try:
            searchresults = self.text_read(condition)
            return len(searchresults)
        except Exception:
            raise Exception("text count exception")

    """ Find  """

    def text_read(self, condition: dict) -> list:
        try:
            condition_array = [t for t in condition.items()]
            with open(self.filepath) as f:
                readdata = f.read()
                # All cases: will be a tuple of length 0
                dataarray = json.loads(readdata) if readdata else []
                if len(condition_array) == 0:
                    results = [item for item in dataarray]
                    return results
                if len(condition_array) == 1:
                    key, value = condition_array[0]
                    if isinstance(value, list):
                        # Multiple conditions
                        if "$and" in key:
                            temp_dataarray = []
                            for condition in value:
                                if isinstance(condition, dict):
                                    ckey = list(condition.keys())[0]
                                    cvalue = list(condition.values())[0]
                                    temp_dataarray = dataarray
                                    dataarray = self.search_generator(
                                        dataarray, ckey, cvalue
                                    )
                                if len(dataarray) == 0:
                                    dataarray = temp_dataarray
                            result = dataarray
                    else:
                        # Single condition
                        result = self.search_generator(dataarray, key, value)
                else:
                    # Handle other cases here if needed
                    result = []
                return result
        except Exception:
            raise Exception("text read exception")

    def search_generator(self, dataarray, key, conditions) -> list:
        # Generate condition
        try:
            if isinstance(conditions, dict):
                if "$ne" in conditions.keys():
                    return [
                        item
                        for item in dataarray
                        if key in item and item[key] != conditions["$ne"]
                    ]
                elif "$gt" in conditions.keys():
                    return [
                        item
                        for item in dataarray
                        if key in item and item[key] > conditions["$gt"]
                    ]
                elif "$lt" in conditions.keys():
                    return [
                        item
                        for item in dataarray
                        if key in item and item[key] < conditions["$lt"]
                    ]
                elif "$gte" in conditions.keys():
                    return [
                        item
                        for item in dataarray
                        if key in item and item[key] >= conditions["$gte"]
                    ]
                elif "$lte" in conditions.keys():
                    return [
                        item
                        for item in dataarray
                        if key in item and item[key] <= conditions["$lte"]
                    ]
                elif "$regex" in conditions.keys():
                    keyword = re.compile(conditions["$regex"])
                    return [
                        item
                        for item in dataarray
                        if key in item and keyword.match(item[key])
                    ]
                else:
                    return []

            eq = "="
            inequalitysign = eq
            if inequalitysign == eq:
                return [item for item in dataarray if item.get(key) == conditions]
        except Exception:
            raise Exception("search genarate exception")

    """ Insert """

    def text_create(self, data: list):
        try:
            with open(self.filepath, mode="r+") as f:
                try:
                    insertdatas = json.load(f)
                except json.JSONDecodeError:
                    insertdatas = []

                if not insertdatas:
                    insertdatas = data
                else:
                    insertdatas.extend(data)
                f.seek(0)
                json.dump(insertdatas, f, ensure_ascii=False)
                f.truncate()
        except Exception:
            raise Exception("text create exception")

    """ update """

    def text_update(self, criteria: dict, updates: dict):
        results = []
        try:
            findresults = self.text_read(criteria)
            updatetargets = self.text_read(criteria)
            updateresults = []

            if len(findresults) == 0:
                return
            elif len(findresults) >= 1:
                for ukey, uval in updates["$set"].items():
                    findresults = [
                        {**result_dict, ukey: uval} for result_dict in findresults
                    ]
                updateresults.extend(findresults)
            # updates and adjust the order
            num = 0
            with open(self.filepath) as f:
                dataarray = json.load(f)

            for data in dataarray:
                if data not in updatetargets:
                    results.append(data)
                else:
                    results.append(updateresults[num])
                    num += 1

            # Write update results
            with open(self.filepath, mode="w") as f:
                json.dump(results, f, ensure_ascii=False)
                f.truncate()

        except Exception:
            raise Exception("text update exception")

    """ delete """

    def text_delete(self, condition: dict):
        try:
            results = []

            # All cases: will be a tuple of length 0
            if not condition:
                with open(self.filepath, mode="w") as f:
                    f.truncate(0)
            else:
                # Set Conditions param
                with open(self.filepath) as f:
                    dataarray = json.load(f)
                    delete_results = self.text_read(condition)
                    for data in dataarray:
                        if data not in delete_results:
                            results.append(data)
            # Write delete results
            with open(self.filepath, mode="w") as f:
                json.dump(results, f, ensure_ascii=False)
                f.truncate()
        except Exception:
            raise Exception("text delete exception")

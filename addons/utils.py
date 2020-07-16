"""
   This file provide every common function needed by all Classes of Functions
"""

import json
from datetime import datetime, timedelta
import aiohttp


def mongo_list_to_dict(mongo_resp):
    """
        Converts List data from MongoDB response into a dictionary
    """

    result = []
    list_data = json.loads(mongo_resp)
    for data in list_data:
        data = mongo_dict_to_dict(data, is_dict=True)
        result.append(data)
    return result


def mongo_dict_to_dict(mongo_resp, is_dict=False):
    """
        Casts Fields from MongoDB response into simpler dictionary; Casted keys are:
        1. From `["id"]["$oid"]` into ["id"]
        2. From `["created_at"]["$date"]` into ["created_at"]
        3. From `["updated_at"]["$date"]` into ["updated_at"]
    """

    if is_dict:
        data = mongo_resp
    else:
        data = json.loads(mongo_resp)

    data["id"] = data["_id"]["$oid"]
    data.pop("_id")

    if "created_at" in data and \
            data["created_at"] is not None and \
            "$date" in data["created_at"]:
        data["created_at"] = datetime.fromtimestamp(int(str(data["created_at"]["$date"])[:-3])).strftime("%Y-%m-%d, "
                                                                                                         "%H:%M:%S")

    if "updated_at" in data and \
            data["updated_at"] is not None and \
            "$date" in data["updated_at"]:
        data["updated_at"] = datetime.fromtimestamp(int(str(data["updated_at"]["$date"])[:-3])).strftime("%Y-%m-%d, "
                                                                                                         "%H:%M:%S")

    if "work_datetime" in data and \
            data["work_datetime"] is not None and \
            "$date" in data["work_datetime"]:
        data["work_datetime"] = datetime.fromtimestamp(int(str(data["work_datetime"]["$date"])[:-3])).strftime("%Y-%m-%d, "
                                                                                                         "%H:%M:%S")

    return data


def json_load_str(str_json, data_type="list"):
    """
        Converts `String` data into either `List` or `Dict`
    """
    if len(str_json) > 0:
        return json.loads(str_json)
    else:
        if data_type == "list":
            return []
        elif data_type == "dict":
            return {}
        else:
            return []


def get_json_template(response=False, results=None, total=0, message=None, status=200):
    """
        Sets and standardizes default response of every response
    """

    result = {
        "success": response,
        "message": message,
        "data": results,
        "total": total,
        "status": status
    }

    if results == -1:
        result.pop('results', None)
    else:
        if total == 0 and isinstance(results, (list,)):
            result["total"] = len(results)

        if results is None:
            result["message"] = "Data Not Found."
            if message:
                result["message"] = message
                # else:
        #     result["response"]      = True

    if total == -1:
        result.pop('total', None)
    if message is None:
        result.pop('message', None)
    return result


def get_unprocessable_request():
    """
        Sets and standardizes default response of every invalid-expected response
    """

    return aiohttp.web.Response(
        text=json.dumps(get_unprocessable_request_json(), indent=4),
        status=422,
        content_type='application/json'
    )


def get_unprocessable_request_json():
    """
        Default format for `get_unprocessable_request()` Function
    """

    return {
        "status": 422,
        "message": "Unprocessable Entity",
    }


def get_synced_date(date_str, reduced_day=1):
    """
        Converts `String` date data into `Date` format
    """

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    date_obj_new = date_obj - timedelta(days=reduced_day)
    date_time = date_obj_new.strftime("%Y-%m-%d")
    return date_time


def pop_if_any(data, key):
    try:
        if key in data:
            data.pop(key)
    except:
        pass
    return data

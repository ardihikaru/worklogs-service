"""
   This is a Controller class to manage any action related with /api/worklogs endpoint
"""

from addons.utils import get_json_template, get_synced_date, json_load_str
from database.work_logs.work_logs import WorkLogsModel as DataModel
from database.work_logs.work_logs_functions import get_data, del_data_by_id, upd_data_by_id, \
    get_data_by_id, insert_new_data, get_data_between_date
import asab
from addons.redis.my_redis import MyRedis
from multidict import MultiDictProxy


class WorkLogs(MyRedis):
    def __init__(self):
        super().__init__(asab.Config)
        self.status_code = 200
        self.resp_status = None
        self.resp_data = None
        self.total_records = 0
        self.msg = None
        self.password_hash = None

    def set_status_code(self, code):
        self.status_code = code

    def set_resp_status(self, status):
        self.resp_status = status

    def set_resp_data(self, json_data):
        self.resp_data = json_data

    def set_msg(self, msg):
        self.msg = msg

    def trx_register(self, json_data):
        msg = "Registering a new data is succeed."

        #  inserting
        is_valid, inserted_data, msg = insert_new_data(DataModel, json_data, msg)

        self.set_resp_status(is_valid)
        self.set_msg(msg)
        self.set_resp_data(json_data)

    def register(self, json_data):
        self.trx_register(json_data)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_data(self, args):
        is_valid, users, self.total_records = get_data(DataModel, args)
        self.set_resp_status(is_valid)
        self.set_msg("No data found")
        self.set_resp_data(None)

        if is_valid:
            self.set_msg("Collecting data success.")
            self.set_resp_data(users)

    def __extract_get_args(self, get_args):
        if get_args is not None:
            if not isinstance(get_args, MultiDictProxy):
                if "filter" in get_args:
                    get_args["filter"] = json_load_str(get_args["filter"], "dict")
                if "range" in get_args:
                    get_args["range"] = json_load_str(get_args["range"], "list")
                if "sort" in get_args:
                    get_args["sort"] = json_load_str(get_args["sort"], "list")

        return get_args

    def get_data(self, args=None):
        args = self.__extract_get_args(args)
        self.trx_get_data(args=args)
        return get_json_template(response=self.resp_status, results=self.resp_data, message=self.msg,
                                 total=self.total_records)

    def trx_del_data_by_id(self, _id):
        is_valid, user_data, msg = get_data_by_id(DataModel, _id)
        if is_valid:
            is_valid, msg = del_data_by_id(DataModel, _id)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Deleting data success.")

    def delete_data_by_id(self, _id):
        self.trx_del_data_by_id(_id)
        resp_data = {}
        if self.resp_status:
            resp_data = "Deleted ids: {}".format(_id)
        return get_json_template(response=self.resp_status, results=resp_data, total=-1, message=self.msg)

    def trx_upd_data_by_id(self, _id, json_data):
        is_valid, user_data, msg = upd_data_by_id(DataModel, _id, new_data=json_data)
        self.set_resp_status(is_valid)
        self.set_msg(msg)
        if is_valid:
            self.set_msg("Updating data success.")

        self.set_resp_data(user_data)

    def update_data_by_id(self, _id, json_data):
        self.trx_upd_data_by_id(_id, json_data)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_data_by_id(self, _id):
        is_valid, user_data, _ = get_data_by_id(DataModel, _id)
        self.set_resp_status(is_valid)
        self.set_msg("Fetching data failed.")
        if is_valid:
            self.set_msg("Collecting data success.")

        self.set_resp_data(user_data)

    def get_data_by_id(self, _id):
        self.trx_get_data_by_id(_id)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=-1, message=self.msg)

    def trx_get_data_between(self, start_date_str, end_date_str):
        try:
            start_date = get_synced_date(start_date_str, 0)
            end_date = get_synced_date(end_date_str, -1)

            is_valid, user_data, msg, self.total_records = get_data_between_date(DataModel, start_date, end_date)
            self.set_resp_status(is_valid)
            self.set_msg(msg)
            if is_valid:
                self.set_msg("Collecting data success.")

            self.set_resp_data(user_data)
        except:
            self.set_resp_status(False)
            self.set_msg("Unprocessable Entity")
            self.set_resp_data({})
            self.set_status_code(422)

    def get_data_between(self, start_date, end_date):
        self.trx_get_data_between(start_date, end_date)
        return get_json_template(response=self.resp_status, results=self.resp_data, total=self.total_records,
                                 message=self.msg, status=self.status_code)

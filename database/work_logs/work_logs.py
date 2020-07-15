"""
    Class Model for `WorkLogs` Collections
"""

from mongoengine import Document, StringField, DateTimeField, IntField
import datetime


class WorkLogsModel(Document):
    meta = {'collection': 'WorkLogs'}
    task = StringField(required=True)
    description = StringField(required=True)
    work_hours = IntField(required=True)
    work_datetime = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update(self, **kwargs):
        kwargs["updated_at"] = datetime.datetime.now()
        return super(WorkLogsModel, self).update(**kwargs)

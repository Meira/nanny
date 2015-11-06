# -*- coding: utf-8 -*-
import threading
import db_adapter as db


class Nanny(threading.Thread):
    """
    Derive your app-specific nannies from this class
    """
    LOG_TABLE = None
    LOG_TABLE_COLS = ','.join(['"task_id" VARCHAR', '"task_name" VARCHAR'])

    def __init__(self, task, uid):
        super(Nanny, self).__init__()
        self._task = task
        self._uid = uid
        self._init_log_table()

    def _init_log_table(self):
        db.make_table(db.get_connection(db.DB_NAME), self.LOG_TABLE, self.LOG_TABLE_COLS)

    @classmethod
    def _get_task_data(cls, task):
        """
        :type task: str
        :rtype: list or None
        """
        entries = db.select(db.get_connection(db.DB_NAME), cls.LOG_TABLE, 'task_name', task)
        return entries

    def log(self, *log_data):
        cursor = db.get_connection(db.DB_NAME)
        db.insert_values(cursor, self.LOG_TABLE, log_data)
        cursor.close()

    def run(self):
        """
        Main method for performing actions
        """
        raise NotImplementedError('Subclasses must implement run()')

    @classmethod
    def stat(cls, task):
        """
        Returns statistics data for a given task in a readable format
        None if no task was found
        :type task: str
        :rtype: str or None
        """
        raise NotImplementedError('Subclasses must implement stat()')

    @classmethod
    def json(cls, task):
        """
        Statistics in a machine-readable format
        :type task: str
        :rtype: json or None
        """
        raise NotImplementedError('Subclasses must implement json()')

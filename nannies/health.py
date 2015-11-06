# -*- coding: utf-8 -*-
import subprocess as sub
import json
from datetime import datetime
from nanny_util import warn, info, parse_time
import generic


class HealthNanny(generic.Nanny):
    """
    HealthNanny restarts your task when dead and logs process lifecycle data
    """

    LOG_TABLE = 'health'
    LOG_TABLE_COLS = ','.join([generic.Nanny.LOG_TABLE_COLS,
                               '"time_start" DATETIME',
                               '"time_end" DATETIME',
                               '"pid" INTEGER',
                               '"exit_code" INTEGER'])

    def _start_process(self):
        """
        :rtype: (Popen, datetime)
        """
        return sub.Popen(['python', self._task]), datetime.now()

    def run(self):
        process, t = self._start_process()
        while True:
            error = process.wait()
            values = (self._uid, self._task, t, datetime.now(), process.pid, process.returncode)
            self.log(*values)

            if error:
                warn('Nanny> Process terminated with non-zero code, restarting...')
            else:
                info('Nanny> Process finished, restarting...')
            process, t = self._start_process()

    @classmethod
    def stat(cls, task):
        json_data = cls.json(task)
        if json_data is None:
            return None
        data = json.loads(json_data)
        s = []
        for name, runs in data.items():
            s.append(name)
            for id_, sessions in runs.items():
                s.append('   {0}'.format(id_))
                for time_start, time_end, exit_code in sessions:
                    t1, t2 = parse_time(time_start), parse_time(time_end)
                    t_delta = t2 - t1
                    s.append('\t{0} - {1} (ran for {2}, exit code {3})'.format(t1, t2, t_delta, exit_code))
        return '\n'.join(s)

    @classmethod
    def json(cls, task):
        """
        Format
        {
            task1:
                {
                    run1: [session1, session2...],
                    run2: [session1, session2...],
                },
        }
        """
        entries = cls._get_task_data(task)
        if not entries:
            return None
        result = {}
        for task_id, name, time_start, time_end, pid, exit_code in entries:
            session_info = (time_start, time_end, exit_code)
            if name in result:
                if task_id in result[name]:
                    result[name][task_id].append(session_info)
                else:
                    result[name][task_id] = [session_info]
            else:
                result[name] = {task_id: [session_info]}
        return json.dumps(result)

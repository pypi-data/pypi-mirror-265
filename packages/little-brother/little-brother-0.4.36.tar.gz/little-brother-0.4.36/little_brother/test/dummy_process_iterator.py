#    Copyright (C) 2019  Marcus Rickert
#
#    See https://github.com/marcus67/little_brother
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import collections

from little_brother.persistence.session_context import SessionContext

uids_tuple = collections.namedtuple('uids', ['real', 'effective'])


class DummyProcess(object):

    def __init__(self, p_pinfo, p_uid):
        self._pinfo = p_pinfo
        self._uid = p_uid

    def uids(self):
        return uids_tuple(real=self._uid, effective=self._uid)

    def name(self):
        return self._pinfo.processname.split('/')[-1]

    def cmdline(self):
        if self._pinfo.cmd_line:
            return self._pinfo.cmd_line

        else:
            return [self._pinfo.processname]


    def create_time(self):
        return self._pinfo.start_time.timestamp()

    @property
    def pid(self):
        return self._pinfo.pid


class DummyProcessFactory(object):

    def __init__(self, p_processes, p_login_mapping, p_session_context:SessionContext):
        self._processes = p_processes
        self._login_mapping = p_login_mapping
        self._reference_time = None
        self._session_context = p_session_context

    def set_reference_time(self, p_reference_time):
        self._reference_time = p_reference_time

    def process_iter(self):
        if self._reference_time is None:
            raise RuntimeError("_reference_time is None")

        return [DummyProcess(p, self._login_mapping.get_uid_by_login(p_session_context=self._session_context,
                                                                     p_login=p.username)) for p in self._processes
                if self._reference_time >= p.start_time and (
                        p.end_time is None or self._reference_time < p.end_time)].__iter__()

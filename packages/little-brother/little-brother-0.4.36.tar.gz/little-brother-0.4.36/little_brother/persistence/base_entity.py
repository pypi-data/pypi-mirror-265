# -*- coding: utf-8 -*-
# Copyright (C) 2019-2024  Marcus Rickert
#
# See https://github.com/marcus67/little_brother
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from typing import Optional

from little_brother.persistence.session_context import SessionContext
from python_base_app import log_handling


class BaseEntity:

    def __init__(self):
        self._logger = log_handling.get_logger(self.__class__.__name__)
        self.id: Optional[int] = None

    def populate_test_data(self, p_session_context: SessionContext):
        pass  # default action: none

# SPDX-FileCopyrightText: 2024-present Trenton H <rda0128ou@mozmail.com>
#
# SPDX-License-Identifier: MPL-2.0

import sys
from dataclasses import dataclass

if sys.version_info < (3, 10):
    slots_dataclass_decorator = dataclass()
    frozen_slots_dataclass_decorator = dataclass(frozen=True)
else:
    slots_dataclass_decorator = dataclass(slots=True)
    frozen_slots_dataclass_decorator = dataclass(slots=True, frozen=True)

# coding=utf-8
#
# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)
#
# Most of this work is copyright (C) 2013-2015 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# https://github.com/DRMacIver/hypothesis/blob/master/CONTRIBUTING.rst for a
# full list of people who may hold copyright, and consult the git log if you
# need to determine who owns an individual contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import division, print_function, absolute_import

import hypothesis.strategies as st
from hypothesis import find, given

x = st.shared(st.integers())


@given(x, x)
def test_sharing_is_by_instance_by_default(a, b):
    assert a == b


@given(
    st.shared(st.integers(), key='hi'), st.shared(st.integers(), key='hi'))
def test_different_instances_with_the_same_key_are_shared(a, b):
    assert a == b


def test_different_instances_are_not_shared():
    find(
        st.tuples(st.shared(st.integers()), st.shared(st.integers())),
        lambda x: x[0] != x[1]
    )


def test_different_keys_are_not_shared():
    find(
        st.tuples(
            st.shared(st.integers(), key=1),
            st.shared(st.integers(), key=2)),
        lambda x: x[0] != x[1]
    )


def test_keys_and_default_are_not_shared():
    find(
        st.tuples(
            st.shared(st.integers(), key=1),
            st.shared(st.integers())),
        lambda x: x[0] != x[1]
    )
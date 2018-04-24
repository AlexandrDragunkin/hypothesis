=========
Настройки
=========

Hypothesis пытается использовать приемлемые значения в умолчаниях для своего поведения, но иногда этого недостаточно, и вам требуется настроить его.

Механизм для этого - объект :class:`~hypothesis.settings`. Вы можете изменить базовые настройки теста на основе :func:`@given <hypothesis.given>` с помощью декоратора настроек:

:func:`@given <hypothesis.given>`данный вызов выглядит следующим образом:

.. code:: python

    from hypothesis import given, settings

    @given(integers())
    @settings(max_examples=500)
    def test_this_thoroughly(x):
        pass

При этом используется объект :class:`~hypothesis.settings`, который приводит к тому, что тест получает гораздо больший набор примеров, чем обычный.

Он может быть применено либо до, либо после *given*. Это не повлияет на результаты. В точности эквивалентен предыдущему следующий пример:

.. code:: python

    from hypothesis import given, settings

    @settings(max_examples=500)
    @given(integers())
    def test_this_thoroughly(x):
        pass

-------------------
Доступные установки
-------------------
`class hypothesis.settings(parent=None, **kwargs)`

.. autoclass:: hypothesis.settings
    :members:
    :exclude-members: register_profile, get_profile, load_profile

.. _phases:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Управление тем, что выполняется
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Hypothesis делит тесты на четыре логически различные фазы:

1. Выполнение явных примеров :ref:`provided with the @example decorator <providing-explicit-examples>`.
2. Повторный запуск выборки ранее неудачных примеров для воспроизведения ранее замеченной ошибки.
3. Создание новых примеров.
4. Попытка сжать пример, найденный на этапах 2 или 3, до более управляемого (явные примеры не могут быть сжаты).
   
Настройка фаз обеспечивает точный контроль над тем, какая из них выполняется, при этом каждая фаза соответствует значению в перечислении :class:`~hypothesis._settings.Phase` :

1. ``Phase.explicit`` управляет выполнением явных примеров.
2. ``Phase.reuse`` управляет повторным использованием предыдущих примеров.
3. ``Phase.generate`` определяет, будут ли создаваться новые примеры.
4. ``Phase.shrink`` управляет сокращением (сжатием) примеров.

Аргумент phases принимает коллекцию с любым их подмножеством. например, ``settings(phases=[Phase.generate, Phase.shrink])`` будет генерировать новые примеры и сжимать их, но не будет запускать явные примеры или повторно использовать предыдущие сбои, в то время как ``settings(phases=[Phase.explicit])`` будут выполняться только явные примеры.

.. _verbose-output:

~~~~~~~~~~~~~~~~~~~~~~~~~~
Просмотр промежуточного результата
~~~~~~~~~~~~~~~~~~~~~~~~~~

Чтобы увидеть, что происходит, пока Hypothesis выполняет ваши тесты, вы можете включить в настройке Verbosity. Она работает, как с :func:`~hypothesis.core.find`, так и с :func:`@given <hypothesis.given>`.

.. doctest::

    >>> from hypothesis import find, settings, Verbosity
    >>> from hypothesis.strategies import lists, integers
    >>> find(lists(integers()), any, settings=settings(verbosity=Verbosity.verbose))
    Tried non-satisfying example []
    Found satisfying example [-1198601713, -67, 116, -29578]
    Shrunk example to [-67, 116, -29578]
    Shrunk example to [116, -29578]
    Shrunk example to [-29578]
    Shrunk example to [-115]
    Shrunk example to [115]
    Shrunk example to [-57]
    Shrunk example to [29]
    Shrunk example to [-14]
    Shrunk example to [-7]
    Shrunk example to [4]
    Shrunk example to [2]
    Shrunk example to [1]
    [1]

Четыре уровня: quiet (тихий), normal (нормальный), verbose (подробный) и debug (отладочный). normal-это значение по умолчанию, в то время как в quiet режиме Hypothesis не будет ничего печатать, даже окончательный пример фальсификации. debug по сути это то тот же  verbose, но немного подробнее. Вы, наверное, не хотите этого.

При использовании pytest также может потребоваться :doc:`disable output capturing for passing tests <pytest:capture>` (запись выходных данных для прохождения тестов).	
	
-------------------------
Building settings objects
-------------------------

Settings can be created by calling :class:`~hypothesis.settings` with any of the available settings
values. Any absent ones will be set to defaults:

.. doctest::

    >>> from hypothesis import settings
    >>> settings().max_examples
    100
    >>> settings(max_examples=10).max_examples
    10

You can also pass a 'parent' settings object as the first argument,
and any settings you do not specify as keyword arguments will be
copied from the parent settings:

.. doctest::

    >>> parent = settings(max_examples=10)
    >>> child = settings(parent, deadline=200)
    >>> parent.max_examples == child.max_examples == 10
    True
    >>> parent.deadline
    not_set
    >>> child.deadline
    200

----------------
Default settings
----------------

At any given point in your program there is a current default settings,
available as ``settings.default``. As well as being a settings object in its own
right, all newly created settings objects which are not explicitly based off
another settings are based off the default, so will inherit any values that are
not explicitly set from it.

You can change the defaults by using profiles (see next section), but you can
also override them locally by using a settings object as a :ref:`context manager <python:context-managers>`


.. doctest::

    >>> with settings(max_examples=150):
    ...     print(settings.default.max_examples)
    ...     print(settings().max_examples)
    150
    150
    >>> settings().max_examples
    100

Note that after the block exits the default is returned to normal.

You can use this by nesting test definitions inside the context:

.. code:: python

    from hypothesis import given, settings

    with settings(max_examples=500):
        @given(integers())
        def test_this_thoroughly(x):
            pass

All settings objects created or tests defined inside the block will inherit their
defaults from the settings object used as the context. You can still override them
with custom defined settings of course.

Warning: If you use define test functions which don't use :func:`@given <hypothesis.given>`
inside a context block, these will not use the enclosing settings. This is because the context
manager only affects the definition, not the execution of the function.

.. _settings_profiles:

~~~~~~~~~~~~~~~~~
settings Profiles
~~~~~~~~~~~~~~~~~

Depending on your environment you may want different default settings.
For example: during development you may want to lower the number of examples
to speed up the tests. However, in a CI environment you may want more examples
so you are more likely to find bugs.

Hypothesis allows you to define different settings profiles. These profiles
can be loaded at any time.

Loading a profile changes the default settings but will not change the behavior
of tests that explicitly change the settings.

.. doctest::

    >>> from hypothesis import settings
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings().max_examples
    100
    >>> settings.load_profile("ci")
    >>> settings().max_examples
    1000

Instead of loading the profile and overriding the defaults you can retrieve profiles for
specific tests.

.. doctest::

    >>> with settings.get_profile("ci"):
    ...     print(settings().max_examples)
    ...
    1000

Optionally, you may define the environment variable to load a profile for you.
This is the suggested pattern for running your tests on CI.
The code below should run in a `conftest.py` or any setup/initialization section of your test suite.
If this variable is not defined the Hypothesis defined defaults will be loaded.

.. doctest::

    >>> import os
    >>> from hypothesis import settings, Verbosity
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings.register_profile("dev", max_examples=10)
    >>> settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
    >>> settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))

If you are using the hypothesis pytest plugin and your profiles are registered
by your conftest you can load one with the command line option ``--hypothesis-profile``.

.. code:: bash

    $ pytest tests --hypothesis-profile <profile-name>


~~~~~~~~
Timeouts
~~~~~~~~

The timeout functionality of Hypothesis is being deprecated, and will
eventually be removed. For the moment, the timeout setting can still be set
and the old default timeout of one minute remains.

If you want to future proof your code you can get
the future behaviour by setting it to the value ``hypothesis.unlimited``.

.. code:: python

    from hypothesis import given, settings, unlimited
    from hypothesis import strategies as st

    @settings(timeout=unlimited)
    @given(st.integers())
    def test_something_slow(i):
        ...

This will cause your code to run until it hits the normal Hypothesis example
limits, regardless of how long it takes. ``timeout=unlimited`` will remain a
valid setting after the timeout functionality has been deprecated (but will
then have its own deprecation cycle).

There is however now a timing related health check which is designed to catch
tests that run for ages by accident. If you really want your test to run
forever, the following code will enable that:

.. code:: python

    from hypothesis import given, settings, unlimited, HealthCheck
    from hypothesis import strategies as st

    @settings(timeout=unlimited, suppress_health_check=[
        HealthCheck.hung_test
    ])
    @given(st.integers())
    def test_something_slow(i):
        ...

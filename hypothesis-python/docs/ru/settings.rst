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
Сборка settings objects
-------------------------

Settings могут быть созданы путем вызова :class:`~hypothesis.settings` с любым из доступных значений settings. Любые отсутствующие будут установлены по умолчанию:

.. doctest::

    >>> from hypothesis import settings
    >>> settings().max_examples
    100
    >>> settings(max_examples=10).max_examples
    10

В качестве первого аргумента можно также передать объект - "родительский" settings, и любые параметры, не указанные в качестве именованных аргументов, будут скопированы из родительских параметров:	
	
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
Настройка settings
----------------

В любой момент в вашей программе есть текущие настройки по умолчанию, доступные в качестве ``settings.default``. Помимо того, что объект settings сам по себе, все вновь созданные объекты settings, которые явно не основаны на других настройках, основаны на значении по умолчанию, поэтому будут наследовать любые значения, которые явно не установлены из него.

Значения по умолчанию можно изменить с помощью профилей (См. следующий раздел), но их также можно переопределить локально с помощью объекта параметров в качестве :ref:`context manager <python:context-managers>`

.. doctest::

    >>> with settings(max_examples=150):
    ...     print(settings.default.max_examples)
    ...     print(settings().max_examples)
    150
    150
    >>> settings().max_examples
    100

Обратите внимание, что после выхода из блока значение по умолчанию возвращается в нормальное состояние.

Это можно использовать, вложив определения тестов в контекст:

.. code:: python

    from hypothesis import given, settings

    with settings(max_examples=500):
        @given(integers())
        def test_this_thoroughly(x):
            pass

Все созданные объекты settings или тесты, определенные внутри блока, наследуют значения по умолчанию от объекта settings, используемого в качестве контекста. Вы, конечно, все еще можете переопределить их с помощью пользовательских настроек.

Внимание!: Если вы используете определение тестовых функции, которые не используют :func:`@given <hypothesis.given>` внутри блока контекста, они не будут использовать вложенные  параметры. Это происходит потому, что менеджер контекста влияет только на определение, а не на выполнение функции.			
			
.. _settings_profiles:

~~~~~~~~~~~~~~~~~
settings Profiles
~~~~~~~~~~~~~~~~~

В зависимости от окружения могут потребоваться различные параметры по умолчанию. Например: во время разработки вы можете уменьшить количество примеров, чтобы ускорить тесты. Однако в среде CI может потребоваться больше примеров, чтобы с большей вероятностью найти ошибки.

Hypothesis позволяет определить различные настройки профилей. Эти профили могут быть загружены в любое время.

Загрузка профиля изменяет параметры по умолчанию, но не изменяет поведение тестов, которые явно изменяют параметры.

.. doctest::

    >>> from hypothesis import settings
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings().max_examples
    100
    >>> settings.load_profile("ci")
    >>> settings().max_examples
    1000

Вместо загрузки профиля и переопределения значений по умолчанию можно получить профили для определенных тестов.

.. doctest::

    >>> with settings.get_profile("ci"):
    ...     print(settings().max_examples)
    ...
    1000

При необходимости можно определить переменную окружения для загрузки профиля. Это Рекомендуемый шаблон для выполнения тестов в CI. Приведенный ниже код должен выполняться в `conftest.py` или любой раздел setup/initialization комплекта тестов. Если эта переменная не определена, будут загружены значения по умолчанию, определенные Hypothesis.
	

.. doctest::

    >>> import os
    >>> from hypothesis import settings, Verbosity
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings.register_profile("dev", max_examples=10)
    >>> settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
    >>> settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))

Если вы используете плагин hypothesis pytest и ваши профили зарегистрированы вашим conftest вы можете загрузить один с опцией командной строки ``--hypothesis-profile``.

.. code:: bash

    $ pytest tests --hypothesis-profile <profile-name>


~~~~~~~~
Timeouts
~~~~~~~~

Функционал timeout Hypothesis является устаревшим и будет удален. На данный момент парметры timeout все еще может быть назначены, и старое умолчание таймаут одна минута остается.

Если вы хотите в будущем использовать свой код, вы можете оценить будущее поведение, установив timeout в ``hypothesis.unlimited``.

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

Это приведет к тому, что ваш код будет выполняться до тех пор, пока он не достигнет нормальных пределов примера Hypothesis, независимо от того, сколько времени это займет. ``timeout=unlimited`` останется допустимым параметром после отказа от функции timeout (но затем будет иметь свой собственный цикл старения).

Существует, однако, в настоящее время сроки, связанные с health check, который предназначен, чтобы отловить тесты, которые  готовы работать случайно на века . Если вы действительно хотите, чтобы ваш тест выполнялся вечно, следующий код позволит это:

.. code:: python

    from hypothesis import given, settings, unlimited, HealthCheck
    from hypothesis import strategies as st

    @settings(timeout=unlimited, suppress_health_check=[
        HealthCheck.hung_test
    ])
    @given(st.integers())
    def test_something_slow(i):
        ...

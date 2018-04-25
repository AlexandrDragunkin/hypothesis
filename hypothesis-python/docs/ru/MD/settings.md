
settings
=========

Hypothesis пытается использовать приемлемые значения в умолчаниях для своего поведения, но иногда этого недостаточно, и вам требуется настроить его.

Механизм для этого - объект `hypothesis.settings`. Вы можете изменить базовые настройки теста на основе `@given` с помощью декоратора настроек:

`@given` данный вызов выглядит следующим образом:



    from hypothesis import given, settings

    @given(integers())
    @settings(max_examples=500)
    def test_this_thoroughly(x):
        pass

При этом используется объект `hypothesis.settings`, который приводит к тому, что тест получает гораздо больший набор примеров, чем обычный.

Он может быть применено либо до, либо после *given*. Это не повлияет на результаты. В точности эквивалентен предыдущему следующий пример:



    from hypothesis import given, settings

    @settings(max_examples=500)
    @given(integers())
    def test_this_thoroughly(x):
        pass


Доступные установки
-------------------

**`class hypothesis.settings(parent=None, **kwargs)`**

Объект settings управляет множеством параметров, используемых при фальсификации. Они могут контролировать как стратегию фальсификации, так и детали генерируемых данных.

Значения по умолчанию выбираются из объекта  *settings.default* и изменения будут подхвачены во вновь созданные настройки.

> ***classmethod define_setting(name, description, default, options=None, validator=None, show_default=True, future_default=not_set, deprecation_message=None, hide_repr=not_set)*** [[source]](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/_settings.html#settings)

Добавление нового setting.

- **name**-имя свойства, которое будет использоваться для доступа к настройке. Это должен быть действительный идентификатор python.
- **description**-описание появится в *docstring* свойства
- **default**-используется значение по умолчанию. Это может быть функция с нулевым аргументом, в этом случае она вычисляется, и ее результат сохраняется при первом обращении к ней для любого заданного объекта settings.


> **buffer_size**

The size of the underlying data used to generate examples. If you need to generate really large examples you may want to increase this, but it will make your tests slower.

default value: 8192

> **database**

An instance of hypothesis.database.ExampleDatabase that will be used to save examples to and load previous examples from. May be None in which case no storage will be used, :memory: for an in-memory database, or any path for a directory-based example database.

default value: (dynamically calculated)

> **database_file**

The file or directory location to save and load previously tried examples; :memory: for an in-memory cache or None to disable caching entirely.

default value: (dynamically calculated)

The database_file setting is deprecated in favor of the database setting, and will be removed in a future version. It only exists at all for complicated historical reasons and you should just use database instead.

> **deadline**

If set, a time in milliseconds (which may be a float to express smaller units of time) that each individual example (i.e. each time your test function is called, not the whole decorated test) within a test is not allowed to exceed. Tests which take longer than that may be converted into errors (but will not necessarily be if close to the deadline, to allow some variability in test run time).

Set this to None to disable this behaviour entirely.

In future this will default to 200. For now, a HypothesisDeprecationWarning will be emitted if you exceed that default deadline and have not explicitly set a deadline yourself.

default value: not_set

> **derandomize**

If this is True then hypothesis will run in deterministic mode where each falsification uses a random number generator that is seeded based on the hypothesis to falsify, which will be consistent across multiple runs. This has the advantage that it will eliminate any randomness from your tests, which may be preferable for some situations. It does have the disadvantage of making your tests less likely to find novel breakages.

default value: False

> **max_examples**

Once this many satisfying examples have been considered without finding any counter-example, falsification will terminate.

default value: 100

> **max_iterations**

This doesn’t actually do anything, but remains for compatibility reasons.

default value: not_set

The max_iterations setting has been disabled, as internal heuristics are more useful for this purpose than a user setting. It no longer has any effect.

> **max_shrinks**

Once this many successful shrinks have been performed, Hypothesis will assume something has gone a bit wrong and give up rather than continuing to try to shrink the example.

default value: 500

> **min_satisfying\_examples**

This doesn’t actually do anything, but remains for compatibility reasons.

default value: not_set

The min_satisfying_examples setting has been deprecated and disabled, due to overlap with the filter_too_much healthcheck and poor interaction with the max_examples setting.

> **perform_health\_check**

If set to True, Hypothesis will run a preliminary health check before attempting to actually execute your test.

default value: not_set

This setting is deprecated, as perform_health_check=False duplicates the effect of suppress_health_check=HealthCheck.all(). Use that instead!

> **phases**

Control which phases should be run. See the full documentation for more details

default value: (<Phase.explicit: 0>, <Phase.reuse: 1>, <Phase.generate: 2>, <Phase.shrink: 3>)

> **print_blob**

Determines whether to print blobs after tests that can be used to reproduce failures.

See the documentation on @reproduce_failure for more details of this behaviour.

default value: <PrintSettings.INFER: 1>

> **stateful\_step\_count**

Number of steps to run a stateful program for before giving up on it breaking.

default value: 50

> **strict**

Strict mode has been deprecated in favor of Python’s standard warnings controls. Ironically, enabling it is therefore an error - it only exists so that users get the right type of error!

default value: False

Strict mode is deprecated and will go away in a future version of Hypothesis. To get the same behaviour, use warnings.simplefilter(‘error’, HypothesisDeprecationWarning).

> **suppress\_health\_check**

A list of health checks to disable.

default value: ()

> **timeout**
Once this many seconds have passed, falsify will terminate even if it has not found many examples. This is a soft rather than a hard limit - Hypothesis won’t e.g. interrupt execution of the called function to stop it. If this value is <= 0 then no timeout will be applied.

default value: 60

The timeout setting is deprecated and will be removed in a future version of Hypothesis. To get the future behaviour set timeout=hypothesis.unlimited instead (which will remain valid for a further deprecation period after this setting has gone away).

> **use_coverage**

Whether to use coverage information to improve Hypothesis’s ability to find bugs.

You should generally leave this turned on unless your code performs poorly when run under coverage. If you turn it off, please file a bug report or add a comment to an existing one about the problem that prompted you to do so.

default value: True

> **verbosity**

Control the verbosity level of Hypothesis messages

default value: Verbosity.normal


## Controlling What Runs ##


Hypothesis делит тесты на четыре логически различные фазы:

1. Выполнение явных примеров `provided with the @example decorator`.
2. Повторный запуск выборки ранее неудачных примеров для воспроизведения ранее замеченной ошибки.
3. Создание новых примеров.
4. Попытка сжать пример, найденный на этапах 2 или 3, до более управляемого (явные примеры не могут быть сжаты).
   
Настройка фаз обеспечивает точный контроль над тем, какая из них выполняется, при этом каждая фаза соответствует значению в перечислении `hypothesis._settings.Phase` :

1. ``Phase.explicit`` управляет выполнением явных примеров.
2. ``Phase.reuse`` управляет повторным использованием предыдущих примеров.
3. ``Phase.generate`` определяет, будут ли создаваться новые примеры.
4. ``Phase.shrink`` управляет сокращением (сжатием) примеров.

Аргумент phases принимает коллекцию с любым их подмножеством. например, ``settings(phases=[Phase.generate, Phase.shrink])`` будет генерировать новые примеры и сжимать их, но не будет запускать явные примеры или повторно использовать предыдущие сбои, в то время как ``settings(phases=[Phase.explicit])`` будут выполняться только явные примеры.


## Просмотр промежуточного результата ##


Чтобы увидеть, что происходит, пока Hypothesis выполняет ваши тесты, вы можете включить в настройке Verbosity. Она работает, как с `~hypothesis.core.find`, так и с `@given`.

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

При использовании pytest также может потребоваться `disable output capturing for passing tests` (запись выходных данных для прохождения тестов).	
	

Сборка settings objects
-------------------------

Settings могут быть созданы путем вызова `hypothesis.settings` с любым из доступных значений settings. Любые отсутствующие будут установлены по умолчанию:


    >>> from hypothesis import settings
    >>> settings().max_examples
    100
    >>> settings(max_examples=10).max_examples
    10

В качестве первого аргумента можно также передать объект - "родительский" settings, и любые параметры, не указанные в качестве именованных аргументов, будут скопированы из родительских параметров:	
	

    >>> parent = settings(max_examples=10)
    >>> child = settings(parent, deadline=200)
    >>> parent.max_examples == child.max_examples == 10
    True
    >>> parent.deadline
    not_set
    >>> child.deadline
    200


Настройка settings
----------------

В любой момент в вашей программе есть текущие настройки по умолчанию, доступные в качестве ``settings.default``. Помимо того, что объект settings сам по себе, все вновь созданные объекты settings, которые явно не основаны на других настройках, основаны на значении по умолчанию, поэтому будут наследовать любые значения, которые явно не установлены из него.

Значения по умолчанию можно изменить с помощью профилей (См. следующий раздел), но их также можно переопределить локально с помощью объекта параметров в качестве `context manager`



    >>> with settings(max_examples=150):
    ...     print(settings.default.max_examples)
    ...     print(settings().max_examples)
    150
    150
    >>> settings().max_examples
    100

Обратите внимание, что после выхода из блока значение по умолчанию возвращается в нормальное состояние.

Это можно использовать, вложив определения тестов в контекст:



    from hypothesis import given, settings

    with settings(max_examples=500):
        @given(integers())
        def test_this_thoroughly(x):
            pass

Все созданные объекты settings или тесты, определенные внутри блока, наследуют значения по умолчанию от объекта settings, используемого в качестве контекста. Вы, конечно, все еще можете переопределить их с помощью пользовательских настроек.

Внимание!: Если вы используете определение тестовых функции, которые не используют `@given` внутри блока контекста, они не будут использовать вложенные  параметры. Это происходит потому, что менеджер контекста влияет только на определение, а не на выполнение функции.			
			



## settings Profiles ##


В зависимости от окружения могут потребоваться различные параметры по умолчанию. Например: во время разработки вы можете уменьшить количество примеров, чтобы ускорить тесты. Однако в среде CI может потребоваться больше примеров, чтобы с большей вероятностью найти ошибки.

Hypothesis позволяет определить различные настройки профилей. Эти профили могут быть загружены в любое время.

Загрузка профиля изменяет параметры по умолчанию, но не изменяет поведение тестов, которые явно изменяют параметры.

    >>> from hypothesis import settings
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings().max_examples
    100
    >>> settings.load_profile("ci")
    >>> settings().max_examples
    1000

Вместо загрузки профиля и переопределения значений по умолчанию можно получить профили для определенных тестов.

    >>> with settings.get_profile("ci"):
    ...     print(settings().max_examples)
    ...
    1000

При необходимости можно определить переменную окружения для загрузки профиля. Это Рекомендуемый шаблон для выполнения тестов в CI. Приведенный ниже код должен выполняться в `conftest.py` или любой раздел setup/initialization комплекта тестов. Если эта переменная не определена, будут загружены значения по умолчанию, определенные Hypothesis.
	

    >>> import os
    >>> from hypothesis import settings, Verbosity
    >>> settings.register_profile("ci", max_examples=1000)
    >>> settings.register_profile("dev", max_examples=10)
    >>> settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)
    >>> settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))

Если вы используете плагин hypothesis pytest и ваши профили зарегистрированы вашим conftest вы можете загрузить один с опцией командной строки `--hypothesis-profile`.


    $ pytest tests --hypothesis-profile



## Timeouts ##


Функционал timeout Hypothesis является устаревшим и будет удален. На данный момент парметры timeout все еще могут быть назначены, и старое умолчание timeout в одну минуту остается.

Если вы хотите в будущем использовать свой код, вы можете оценить его поведение в будущем, установив timeout в ``hypothesis.unlimited``.



    from hypothesis import given, settings, unlimited
    from hypothesis import strategies as st

    @settings(timeout=unlimited)
    @given(st.integers())
    def test_something_slow(i):
        ...

Это приведет к тому, что ваш код будет выполняться до тех пор, пока он не подберет обычный пример в рамках Hypothesis, независимо от того, сколько времени это займет. ``timeout=unlimited`` останется допустимым параметром после отказа от функции timeout (но затем будет иметь свой собственный цикл старения).

Тем не менее, теперь существует проверка работоспособности, связанная со сроками и health check, который предназначен, чтобы отловить тесты, которые  готовы работать веками. Если вы действительно хотите, чтобы ваш тест выполнялся вечно, следующий код позволит это:



    from hypothesis import given, settings, unlimited, HealthCheck
    from hypothesis import strategies as st

    @settings(timeout=unlimited, suppress_health_check=[
        HealthCheck.hung_test
    ])
    @given(st.integers())
    def test_something_slow(i):
        ...

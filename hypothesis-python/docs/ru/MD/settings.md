
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

Размер исходных данных, используемых для генерации примеров. Если вам нужно создать действительно большие примеры, вы можете увеличить это значение, но это сделает ваши тесты медленнее.

Значение по умолчанию: 8192

> **database**

Экземпляр hypothesis.database.ExampleDatabase, который будет использоваться для сохранения примеров и загрузки предыдущих примеров.  Может быть None, в этом случае хранилище не будет использоваться, *:memory:* для базы данных в памяти или любой путь для базы данных примеров на основе каталогов.

Значение по умолчанию: (dynamically calculated)

> **database_file**


Расположение файла или каталога для сохранения и загрузки ранее опробованных примеров; *:memory:* для кэша в памяти или None, чтобы полностью отключить кэширование.

Значение по умолчанию: (dynamically calculated)

Параметр *database_file* устарел в пользу параметра *database* и будет удален в следующей версии. Он существует только для сложных исторических причин, и вам настоятельно рекомендуется использовать database вместо него.

> **deadline**

Если задано, то это время в миллисекундах (значение может быть числом с плавающей точкой для выражения меньших единиц времени), которое не может превышать каждый отдельный пример (т. е. каждый раз, когда вызывается тестовая функция, а не весь оформленный тест) в тесте. Тесты, которые занимают больше времени, чем это значение могут быть преобразованы в ошибки (но это не обязательно будет происходить всегда, если значение близко к крайнему сроку, чтобы позволить  внести некоторую гибкость во время выполнения теста).

Установите значение None, чтобы полностью отключить это поведение.

В будущем это значение будет по умолчанию до 200. На данный момент выдается HypothesisDeprecationWarning, если вы превысите этот крайний срок по умолчанию и не указали явный срок.

Значение по умолчанию: not_set

> **derandomize**

Если True, то hypothesis будет работать в детерминированном режиме, где каждая фальсификация использует генератор случайных чисел на основе гипотезы фальсификации, которые будут согласованы на нескольких прогонах. Это имеет преимущество в том, что будет устранена любая случайность из ваших тестов, что может быть предпочтительнее для некоторых ситуаций. У этого есть недостаток, делающий ваши тесты менее вероятными для поиска новых аварийных ситуаций.

Значение по умолчанию: False

> **max_examples**

Как только это множество удовлетворяющих условиям примеров будет рассмотрено, не найдя никакого встречного примера, фальсификация прекратится.

Значение по умолчанию: 100

> **max_iterations**

По факту ничего не делает, но остается по соображениям совместимости.

Значение по умолчанию: not_set

Параметр max_iterations отключен, поскольку для этой цели более эффективны внутренние эвристики, чем пользовательская настройка. Это уже не имеет никакого эффекта.

> **max_shrinks**

Контролирует число выполненных успешных сокращений примера. При превышении этого порога Hypothesis предположит, что что-то пошло немного не так, и прекратит попытки уменьшить пример.

Значение по умолчанию: 500

> **min_satisfying\_examples**

По факту ничего не делает, но остается по соображениям совместимости.

Значение по умолчанию: not_set

Параметр *min\_satisfying\_examples* устарел и отключен из-за перекрытия с параметром *filter\_too\_much healthcheck* и плохого взаимодействия с параметром *max_examples*.

> **perform_health\_check**

Если задано значение True, Hypothesis выполнит предварительную проверку работоспособности перед попыткой фактического выполнения теста.

Значение по умолчанию: not_set

Этот параметр устарел, так как *perform_health_check=False *дублирует эффект *suppress_health_check=HealthCheck.all()* Используйте его вместо этого!

> **phases**

Контролирует, какие фазы должны быть запущены. Дополнительную информацию смотрите в полной документации

Значение по умолчанию: (<Phase.explicit: 0>, <Phase.reuse: 1>, <Phase.generate: 2>, <Phase.shrink: 3>)

> **print_blob**

Определяет, следует ли печатать BLOB (большие двоичные объекты) после тестов, которые можно использовать для воспроизведения ошибок.

Более подробную информацию об этом поведении смотрите в документации по `@reproduce_failure`.

Значение по умолчанию: <PrintSettings.INFER: 1>

> **stateful\_step\_count**

Количество шагов для запуска программы с отслеживанием состояния перед тем, как отказаться от её декомпозиции.

Значение по умолчанию: 50

> **strict**

*strict* (строгий) режим был объявлен устаревшим в пользу стандартных  предупреждений Python. По иронии судьбы, включение этой функции является ошибкой - она ​​существует только для того, чтобы пользователи получали правильный тип ошибок!

Значение по умолчанию: False

Строгий режим устарел и исчезнет в будущей версии Hypothesis. Чтобы получить такое же поведение, используйте *warnings.simplefilter(‘error’, HypothesisDeprecationWarning)*.


> **suppress\_health\_check**

A list of health checks to disable.

Значение по умолчанию: ()

> **timeout**
Once this many seconds have passed, falsify will terminate even if it has not found many examples. This is a soft rather than a hard limit - Hypothesis won’t e.g. interrupt execution of the called function to stop it. If this value is <= 0 then no timeout will be applied.

Значение по умолчанию: 60

The timeout setting is deprecated and will be removed in a future version of Hypothesis. To get the future behaviour set timeout=hypothesis.unlimited instead (which will remain valid for a further deprecation period after this setting has gone away).

> **use_coverage**

Whether to use coverage information to improve Hypothesis’s ability to find bugs.

You should generally leave this turned on unless your code performs poorly when run under coverage. If you turn it off, please file a bug report or add a comment to an existing one about the problem that prompted you to do so.

Значение по умолчанию: True

> **verbosity**

Control the verbosity level of Hypothesis messages

Значение по умолчанию: Verbosity.normal


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

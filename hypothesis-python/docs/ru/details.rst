===============================
Детали и дополнительные функции
===============================

В этой части рассмотрим менее распространенные особенности Hypothesis, которые вам не нужны для того что бы начать его использовать, но, тем не менее, облегчат вашу жизнь.

---------------------------
Дополнительный  test output
---------------------------

Обычно результат неудачного теста выглядит примерно так:

.. code::

    Falsifying example: test_a_thing(x=1, y="foo")

Будет напечатано с ``repr`` каждого именованного аргумента.

Иногда этого недостаточно, потому что у вас есть значения с ``repr``, который не очень описателен или потому, вам нужно увидеть результат некоторых промежуточных шагов вашего теста. Вот в чем заключается функция ``note``:

.. doctest::

    >>> from hypothesis import given, note, strategies as st
    >>> @given(st.lists(st.integers()), st.randoms())
    ... def test_shuffle_is_noop(ls, r):
    ...     ls2 = list(ls)
    ...     r.shuffle(ls2)
    ...     note("Shuffle: %r" % (ls2))
    ...     assert ls == ls2
    ...
    >>> try:
    ...     test_shuffle_is_noop()
    ... except AssertionError:
    ...     print('ls != ls2')
    Falsifying example: test_shuffle_is_noop(ls=[0, 1], r=RandomWithSeed(18))
    Shuffle: [1, 0]
    ls != ls2

Примечание печатается в последнем запуске теста, чтобы включить любую дополнительную информацию, которая может понадобиться в тесте.


.. _statistics:

---------------
Test Statistics
---------------

Если вы используете :pypi:`pytest` вы можете увидеть ряд статистических данных о выполненных тестах
передавая аргумент командной строки ``--hypothesis-show-statistics``. Что позволит включить
некоторые общие статистические данные о тесте:

Например, если вы выполнили следующее с ``--hypothesis-show-statistics``:

.. code-block:: python

  from hypothesis import given, strategies as st

  @given(st.integers())
  def test_integers(i):
      pass


Вы увидите:

.. code-block:: none

  test_integers:

    - 100 passing examples, 0 failing examples, 0 invalid examples
    - Typical runtimes: ~ 1ms
    - Fraction of time spent in data generation: ~ 12%
    - Stopped because settings.max_examples=100

Заключительная строка "Stopped because" особенно важна для note: она сообщает вам значение настройки, которое определяет, когда тест должен прекратить пробовать новые примеры. Это может быть полезно для понимания поведения тестов. В идеале всегда хочется иметь :obj:`~hypothesis.settings.max_examples`.

В некоторых случаях (например, в фильтрах и рекурсивных стратегиях) вы увидите события, которые описывают некоторые аспекты генерации данных:

.. code-block:: python

  from hypothesis import given, strategies as st

  @given(st.integers().filter(lambda x: x % 2 == 0))
  def test_even_integers(i):
      pass

В итоге получите что-то вроде:

.. code-block:: none

  test_even_integers:

      - 100 passing examples, 0 failing examples, 36 invalid examples
      - Typical runtimes: 0-1 ms
      - Fraction of time spent in data generation: ~ 16%
      - Stopped because settings.max_examples=100
      - Events:
        * 80.88%, Retried draw from integers().filter(lambda x: <unknown>) to satisfy filter
        * 26.47%, Aborted test because unable to satisfy integers().filter(lambda x: <unknown>)

Можно также отметить пользовательские события в тесте с помощью функции ``event``:

.. autofunction:: hypothesis.event

.. code:: python

  from hypothesis import given, event, strategies as st

  @given(st.integers().filter(lambda x: x % 2 == 0))
  def test_even_integers(i):
      event("i mod 3 = %d" % (i % 3,))


Тогда вы увидите результат:

.. code-block:: none

  test_even_integers:

    - 100 passing examples, 0 failing examples, 38 invalid examples
    - Typical runtimes: 0-1 ms
    - Fraction of time spent in data generation: ~ 16%
    - Stopped because settings.max_examples=100
    - Events:
      * 80.43%, Retried draw from integers().filter(lambda x: <unknown>) to satisfy filter
      * 31.88%, i mod 3 = 0
      * 27.54%, Aborted test because unable to satisfy integers().filter(lambda x: <unknown>)
      * 21.74%, i mod 3 = 1
      * 18.84%, i mod 3 = 2

Аргументы ``event`` могут быть любого типа, но два события будут считаться одинаковыми, если они совпадают при преобразовании в строку с :obj:`python:str`.

------------------------
Использование assumptions
------------------------
Иногда Hypothesis не дает вам точно правильный *тот самый* вид данных, который вы хотите - это в основном правильные формы. Это не особенно страшно, но некоторые примеры при этом будут сбоить, а вы не хотите заботиться о них. Вы *можете* просто игнорировать эти случаи, прервав тест раньше, но при этом возникает риск случайно упустить важное и испытать намного меньше, чем вы расчитывали. Также было бы неплохо потратить меньше времени на плохие примеры - если вы используете 100 примеров на тест (по умолчанию), и получается, что 70 из этих примеров не соответствуют вашим потребностям, получается что очень много времени потрачено впустую.

.. autofunction:: hypothesis.assume

Например, предположим, что у вас был следующий код:


.. code:: python

  @given(floats())
  def test_negation_is_self_inverse(x):
      assert x == -(-x)


Выполнение его даст нам:

.. code::

  Falsifying example: test_negation_is_self_inverse(x=float('nan'))
  AssertionError

Это раздражает. Мы (возможно) знаем что то о NaN, но в данном эпизоде нам не хотелось бы о нем вспоминать и как то обрабатывать эту ситуацию, но как только Hypothesis найдет пример NaN, он  всё бросит и поспешит рассказать нам об этом. Тест провалится и испортит нам всю статистику, а мы хотим его пройти.

Так что давайте блокировать этот конкретный пример:

.. code:: python

  from math import isnan

  @given(floats())
  def test_negation_is_self_inverse_for_non_nan(x):
      assume(not isnan(x))
      assert x == -(-x)

Этот вариант кода уже проходит без проблем.

In order to avoid the easy trap where you assume a lot more than you intended, Hypothesis will fail a test when it can't find enough examples passing the assumption.

В целях исключения легкого предполагаемого перехвата вы можете предположить гораздо больше, чем намеревались и Hypothesis не удастся тест если он не сможет найти достаточно примеров, проходящих assumption (предположение).

Если бы мы написали:

.. code:: python

  @given(floats())
  def test_negation_is_self_inverse_for_non_nan(x):
      assume(False)
      assert x == -(-x)

Тогда при запуске у нас получилось бы исключение:

.. code::

  Unsatisfiable: Unable to satisfy assumptions of hypothesis test_negation_is_self_inverse_for_non_nan. Only 0 examples considered satisfied assumptions  (*Невозможно выполнить (assumptions) предположения hypothesis test_negation_is_self_inverse_for_non_nan. Только 0 примеров считаются удовлетворенными предположениями (assumptions)*)

~~~~~~~~~~~~~~~~~~~~~~
Как правильно assume-ить?
~~~~~~~~~~~~~~~~~~~~~~

Hypothesis имеет адаптивную стратегию разведки, чтобы попытаться избежать случаев, которые фальсифицируют assumptions и, как правило, приводит к тому, что все еще можно найти examples (примеры) в труднодоступных ситуациях.

Предположим, у нас было следующее:


.. code:: python

  @given(lists(integers()))
  def test_sum_is_positive(xs):
    assert sum(xs) > 0

Неудивительно, что такой тест потерпит неудачу и выдаст фальсифицирующий пример ``[]``.

Добавление ``assume(xs)`` к этому удалит тривиальный пустой пример и дает нам ``[0]``.

Добавим ``assume(all(x > 0 for x in xs))`` и, о, чудо! он проходит! Действительно, сумма положительных больше нуля!

Удивительное не в том, что он не находит встречный пример, но что он находит достаточно примеров на всех.

Чтобы убедиться, что происходит что-то интересное,  попробуем это на длинных списках. Например,  добавим ``assume(len(xs) > 10)``. В принципе, это никогда не должно быть example: примитивная стратегия найдет меньше одного из тысячи примеров, потому что, если каждый элемент списка отрицателен с вероятностью наполовину, вам придется получить десять из них, случайно. В конфигурации по умолчанию гипотеза сдается задолго до того, как она попробовала 1000 примеров (по умолчанию она пробует 200).

Вот что произойдет, если мы попытаемся запустить это:

.. code:: python

  @given(lists(integers()))
  def test_sum_is_positive(xs):
      assume(len(xs) > 10)
      assume(all(x > 0 for x in xs))
      print(xs)
      assert sum(xs) > 0

  In: test_sum_is_positive()
  [17, 12, 7, 13, 11, 3, 6, 9, 8, 11, 47, 27, 1, 31, 1]
  [6, 2, 29, 30, 25, 34, 19, 15, 50, 16, 10, 3, 16]
  [25, 17, 9, 19, 15, 2, 2, 4, 22, 10, 10, 27, 3, 1, 14, 17, 13, 8, 16, 9, 2...
  [17, 65, 78, 1, 8, 29, 2, 79, 28, 18, 39]
  [13, 26, 8, 3, 4, 76, 6, 14, 20, 27, 21, 32, 14, 42, 9, 24, 33, 9, 5, 15, ...
  [2, 1, 2, 2, 3, 10, 12, 11, 21, 11, 1, 16]

Как видим, Hypothesis не находит *много* примеров, но некоторые - вполне достаточны, чтобы получить благополучный результат.

В общем, если вы можете себе позволить точнее формировать свои стратегии для своих тестов, то вы должны это использовать - например :py:func:`integers(1, 1000) <hypothesis.strategies.integers>` намного лучше, чем ``assume(1 <= x <= 1000)``.

---------------------
Определение стратегий
---------------------

Тип объекта, который используется для изучения примеров, предоставленных вашей тестовой функции, называется :class:`~hypothesis.SearchStrategy`.
Они создаются с использованием функций, открытых в модуле:mod:`hypothesis.strategies`.

Многие из этих стратегий предоставляют различные аргументы, которые можно использовать для настройки генерации. Например, для целых чисел вы можете указать ``min`` и ``max`` значения целых чисел, которые вам требуются. Если вы хотите увидеть, что именно выдаст стратегия, вы можете запросить пример:

.. doctest::

    >>> integers(min_value=0, max_value=10).example()
    1

Многие стратегии построены из других стратегий. Например, если вы хотите определить кортеж, нужно сказать, что происходит в каждом элементе:

.. doctest::

    >>> from hypothesis.strategies import tuples
    >>> tuples(integers(), integers()).example()
    (-24597, 12566)

Дополнительная информация :doc:`available in a separate document <data>`.

------------------------------------------
Углубленные сведения о заданных параметрах
------------------------------------------

.. autofunction:: hypothesis.given

Декоратор :func:`@given <hypothesis.given>` может использоваться для указания того, какие аргументы функции должны быть параметризованы. Вы можете использовать аргументы позиционного или именованного вида или их микс.

Например, все приведенные ниже действительны:

.. code:: python

  @given(integers(), integers())
  def a(x, y):
    pass

  @given(integers())
  def b(x, y):
    pass

  @given(y=integers())
  def c(x, y):
    pass

  @given(x=integers())
  def d(x, y):
    pass

  @given(x=integers(), y=integers())
  def e(x, **kwargs):
    pass

  @given(x=integers(), y=integers())
  def f(x, *args, **kwargs):
    pass


  class SomeTest(TestCase):
      @given(integers())
      def test_a_thing(self, x):
          pass

Следующие нет:

.. code:: python

  @given(integers(), integers(), integers())
  def g(x, y):
      pass

  @given(integers())
  def h(x, *args):
      pass

  @given(integers(), x=integers())
  def i(x, y):
      pass

  @given()
  def j(x, y):
      pass

Правила определения того, что является допустимым использованием ``given``, следующие:

1. Вы можете передать любой  именованный аргумент ``given``.
2. Позиционные аргументы ``given`` эквивалентны самым правым именованным аргументам для тестовой функции.
3. Позиционные аргументы не могут использоваться, если базовая тестовая функция имеет аргументы переменной длины-(varargs), произвольные ключевые слова или аргументы, предназначенные только для ключевых слов.
4. Функции, протестированные с ``given``, могут не иметь значений по умолчанию.

Причина поведения "крайних правых именованных аргументов" заключается в том, что :func:`@given <hypothesis.given>`  с помощью методов экземпляра: ``self`` будет передано функции как нормальное и не будет параметризоваться.

Функция, возвращенная given, имеет все те же аргументы, что и исходный тест, за вычетом тех, которые заполнены:func:`@given <hypothesis.given>`.

-----------------------------------
Выполнение пользовательских функций
-----------------------------------

Hypothesis предоставляет вам средство, которое позволяет вам контролировать, как он запускает примеры.

Это позволяет выполнять такие действия, как настройка и разборка каждого примера, выполнение примеров в подпроцессе, преобразование тестов сопрограмм в обычные тесты и т. д. Например, :class:`~hypothesis.extra.django.TransactionTestCase` в
Django extra запускается каждый пример в отдельной транзакции базы данных.

Таким образом, вводя понятие executor или по русски *исполнителя*. executor-это, по сути, функция, которая берет блок кода и запускает его. По умолчанию executor-ом является:

.. code:: python

    def default_executor(function):
        return function()

Вы определяете исполнителей, определив метод ``execute_example`` в классе. Любые методы тестирования используемые в этом классе с  декоратором :func:`@given <hypothesis.given>` будут использовать ``self.execute_example`` как исполнителя теста. Например, следующий executor выполняет весь свой код дважды:

.. code:: python

    from unittest import TestCase

    class TestTryReallyHard(TestCase):
        @given(integers())
        def test_something(self, i):
            perform_some_unreliable_operation(i)

        def execute_example(self, f):
            f()
            return f()

Примечание: функции, которые вы используете в map и т.п. Будут работать *внутри* исполнителя. т.е. они не будут вызываться до вызова функции перешедшей к ``execute_example``.

Исполнитель должен уметь обрабатывать передаваемую функцию, которая возвращает None, иначе он не сможет запускать обычные тестовые случаи. Например, следующий исполнитель недействителен:

.. code:: python

    from unittest import TestCase

    class TestRunTwice(TestCase):
        def execute_example(self, f):
            return f()()

и должны быть переписаны как:

.. code:: python

    from unittest import TestCase

    class TestRunTwice(TestCase):
        def execute_example(self, f):
            result = f()
            if callable(result):
                result = result()
            return result

--------------------------------------------
Использование Hypothesis для поиска значений
--------------------------------------------

Вы можете использовать функции исследования данных Hypothesis, чтобы найти значения, удовлетворяющие некоторому предикату (условию отбора). Это обычно полезно для изучения пользовательских стратегий, определенных с помощью: :func:`@composite <hypothesis.strategies.composite>`, или экспериментировать с условиями фильтрации данных.

.. autofunction:: hypothesis.find

.. doctest::

    >>> from hypothesis import find
    >>> from hypothesis.strategies import sets, lists, integers
    >>> find(lists(integers()), lambda x: sum(x) >= 10)
    [10]
    >>> find(lists(integers()), lambda x: sum(x) >= 10 and len(x) >= 3)
    [0, 0, 10]
    >>> find(sets(integers()), lambda x: sum(x) >= 10 and len(x) >= 3)
    {0, 1, 9}

Первый аргумент :func:`~hypothesis.find` описывает данные обычным способом для аргумента :func:`~hypothesis.given`, и поддерживает :doc:`all the same data types <data>`. Второй-это предикат, который он должен удовлетворить.

Конечно, не все условия выполняются. Если вы запросите у Hypothesis пример с условием, которое всегда ложно, это вызовет ошибку:

.. doctest::

    >>> find(integers(), lambda x: False)
    Traceback (most recent call last):
        ...
    hypothesis.errors.NoSuchExample: No examples of condition lambda x: <unknown>

(``lambda x: unknown`` связано с тем, что Hypothesis не может получить исходный код лямбда-выражения из интерактивной консоли python. )

.. _type-inference:

-------------------
Inferred Strategies
-------------------

В некоторых случаях гипотеза может решить, что делать, когда вы опускаете аргументы. Это основано на самоанализе, а не на магии, и поэтому имеет четко определенные пределы.

:func:`~hypothesis.strategies.builds` проверят сигнатуру ``target`` (using :func:`~python:inspect.getfullargspec`). 
Если есть обязательные аргументы с аннотациями типа и стратегия не была передана :func:`~hypothesis.strategies.builds`, то
:func:`~hypothesis.strategies.from_type` используется для их заполнения. Вы также можете передать специальное значение :const:`hypothesis.infer` в качестве аргумента, чтобы запихнуть в этот вывод аргументы со значением по умолчанию.

.. doctest::

    >>> def func(a: int, b: str):
    ...     return [a, b]
    >>> builds(func).example()
    [-6993, '']


:func:`@given <hypothesis.given>` не выполняет никакого неявного вывода для требуемых аргументов, поскольку это нарушило бы совместимость с функционалом pytest. 
:const:`~hypothesis.infer` может использоваться в качестве аргумента ключевого слова для явного заполнения аргумента из аннотации типа.

.. code:: python

    @given(a=infer)
    def test(a: int): pass
    # is equivalent to
    @given(a=integers())
    def test(a): pass

~~~~~~~~~~~
Ограничения
~~~~~~~~~~~

Аннотации типа :pep:`3107` не поддерживаются в Python 2, и Hypothesis не проверяет комментарии типа :pep:`484` во время выполнения.
В то время как :func:`~hypothesis.strategies.from_type` будет работать как обычно, вывод в 
:func:`~hypothesis.strategies.builds` и :func:`@given <hypothesis.given>` будет работать, только если вы вручную создадите атрибут ``__annotations__`` (например, с помощью  декораторов @annotations(...) и @returns(...)). 

Модуль :mod:`python:typing` полностью поддерживается на Python 2, Если у вас установлен backport.

Модуль :mod:`python:typing` является временным и имеет ряд внутренних изменений между Python 3.5.0 и 3.6.1, в том числе во второстепенных версиях. Все они поддерживаются, но могут возникнуть проблемы со старой версией модуля. Пожалуйста, сообщите нам о них и рассмотрите возможность обновления до более новой версии Python в качестве обходного пути.

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
Выполнение предположений
------------------------
Иногда Hypothesis не дает вам точно правильный *тот самый* вид данных, которые вы хотите - это в основном правильные формы. Это не особенно страшно, но некоторые примеры при этом будут сбоить, а вы не хотите заботиться о них. Вы *можете* просто игнорировать эти случаи, прервав тест раньше, но при этом возникает риск случайно упустить важное и испытать намного меньше, чем вы расчитывали. Также было бы неплохо потратить меньше времени на плохие примеры - если вы используете 100 примеров на тест (по умолчанию), и получается, что 70 из этих примеров не соответствуют вашим потребностям, получается что очень много времени потрачено впустую.

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

Hypothesis has an adaptive exploration strategy to try to avoid things which falsify assumptions, which should generally result in it still being able to find examples in hard to find situations.

Hypothesis имеет адаптивную стратегию разведки, чтобы попытаться избежать случаев, которые фальсифицируют предположения и, как правило, приводит к тому, что все еще можно найти examples (примеры) в труднодоступных ситуациях.

Предположим, у нас было следующее:


.. code:: python

  @given(lists(integers()))
  def test_sum_is_positive(xs):
    assert sum(xs) > 0

Неудивительно, что это потерпит неудачу и выдаст фальсифицирующий пример ``[]``.

Добавление ``assume(xs)`` к этому удаляет тривиальный пустой пример и дает нам ``[0]``.

Добавление ``assume(all(x > 0 for x in xs))`` и он проходит: сумма списка положительных целых чисел положительна.

Удивительное не в том, что он не находит встречный пример, но что он находит достаточно примеров на всех.

In order to make sure something interesting is happening, suppose we wanted to try this for long lists. e.g. suppose we added an assume(len(xs) > 10) to it. This should basically never find an example: a naive strategy would find fewer than one in a thousand examples, because if each element of the list is negative with probability one-half, you'd have to have ten of these go the right way by chance. In the default configuration Hypothesis gives up long before it's tried 1000 examples (by default it tries 200).

Чтобы убедиться, что происходит что-то интересное,  попробуем это для длинных списков. Например,  добавим к нему ``assume(len(xs) > 10)``. В принципе, это никогда не должно быть example: примитивная стратегия найдет меньше одного из тысячи примеров, потому что, если каждый элемент списка отрицателен с вероятностью наполовину, вам придется получить десять из них, случайно. В конфигурации по умолчанию гипотеза сдается задолго до того, как она попробовала 1000 примеров (по умолчанию она пробует 200).

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

As you can see, Hypothesis doesn't find *many* examples here, but it finds some - enough to
keep it happy.

In general if you *can* shape your strategies better to your tests you should - for example :py:func:`integers(1, 1000) <hypothesis.strategies.integers>` is a lot better than ``assume(1 <= x <= 1000)``, but ``assume`` will take you a long way if you can't.

Как видим, Hypothesis не находит *много* примеров, но некоторые - вполне достаточны, чтобы получить благополучный результат.

В общем, если вы можете себе позволить точнее формировать свои стратегии для своих тестов, то вы должны использовать - например :py:func:`integers(1, 1000) <hypothesis.strategies.integers>` намного лучше, вместо ``assume(1 <= x <= 1000)``.

---------------------
Определение стратегий
---------------------

Тип объекта, который используется для изучения примеров, предоставленных вашей тестовой функции, называется :class:`~hypothesis.SearchStrategy`.
Они создаются с использованием функций, открытых в модуле:mod:`hypothesis.strategies`.

Many of these strategies expose a variety of arguments you can use to customize
generation. For example for integers you can specify ``min`` and ``max`` values of
integers you want.
If you want to see exactly what a strategy produces you can ask for an example:

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

------------------------------------
The gory details of given parameters Сведения о заданных параметрах
------------------------------------

.. autofunction:: hypothesis.given

The :func:`@given <hypothesis.given>` decorator may be used
to specify which arguments of a function should
be parametrized over. You can use either positional or keyword arguments or a mixture
of the two.

For example all of the following are valid uses:

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

The following are not:

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


The rules for determining what are valid uses of ``given`` are as follows:

1. You may pass any keyword argument to ``given``.
2. Positional arguments to ``given`` are equivalent to the rightmost named
   arguments for the test function.
3. Positional arguments may not be used if the underlying test function has
   varargs, arbitrary keywords, or keyword-only arguments.
4. Functions tested with ``given`` may not have any defaults.

The reason for the "rightmost named arguments" behaviour is so that
using :func:`@given <hypothesis.given>` with instance methods works: ``self``
will be passed to the function as normal and not be parametrized over.

The function returned by given has all the same arguments as the original
test, minus those that are filled in by :func:`@given <hypothesis.given>`.

-------------------------
Custom function execution
-------------------------

Hypothesis provides you with a hook that lets you control how it runs
examples.

This lets you do things like set up and tear down around each example, run
examples in a subprocess, transform coroutine tests into normal tests, etc.
For example, :class:`~hypothesis.extra.django.TransactionTestCase` in the
Django extra runs each example in a separate database transaction.

The way this works is by introducing the concept of an executor. An executor
is essentially a function that takes a block of code and run it. The default
executor is:

.. code:: python

    def default_executor(function):
        return function()

You define executors by defining a method ``execute_example`` on a class. Any
test methods on that class with :func:`@given <hypothesis.given>` used on them will use
``self.execute_example`` as an executor with which to run tests. For example,
the following executor runs all its code twice:

.. code:: python

    from unittest import TestCase

    class TestTryReallyHard(TestCase):
        @given(integers())
        def test_something(self, i):
            perform_some_unreliable_operation(i)

        def execute_example(self, f):
            f()
            return f()

Note: The functions you use in map, etc. will run *inside* the executor. i.e.
they will not be called until you invoke the function passed to ``execute_example``.

An executor must be able to handle being passed a function which returns None,
otherwise it won't be able to run normal test cases. So for example the following
executor is invalid:

.. code:: python

    from unittest import TestCase

    class TestRunTwice(TestCase):
        def execute_example(self, f):
            return f()()

and should be rewritten as:

.. code:: python

    from unittest import TestCase

    class TestRunTwice(TestCase):
        def execute_example(self, f):
            result = f()
            if callable(result):
                result = result()
            return result


-------------------------------
Using Hypothesis to find values
-------------------------------

You can use Hypothesis's data exploration features to find values satisfying
some predicate.  This is generally useful for exploring custom strategies
defined with :func:`@composite <hypothesis.strategies.composite>`, or
experimenting with conditions for filtering data.

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

The first argument to :func:`~hypothesis.find` describes data in the usual way for an argument to
:func:`~hypothesis.given`, and supports :doc:`all the same data types <data>`. The second is a
predicate it must satisfy.

Of course not all conditions are satisfiable. If you ask Hypothesis for an
example to a condition that is always false it will raise an error:

.. doctest::

    >>> find(integers(), lambda x: False)
    Traceback (most recent call last):
        ...
    hypothesis.errors.NoSuchExample: No examples of condition lambda x: <unknown>

(The ``lambda x: unknown`` is because Hypothesis can't retrieve the source code
of lambdas from the interactive python console. It gives a better error message
most of the time which contains the actual condition)


.. _type-inference:

-------------------
Inferred Strategies
-------------------

In some cases, Hypothesis can work out what to do when you omit arguments.
This is based on introspection, *not* magic, and therefore has well-defined
limits.

:func:`~hypothesis.strategies.builds` will check the signature of the
``target`` (using :func:`~python:inspect.getfullargspec`).
If there are required arguments with type annotations and
no strategy was passed to :func:`~hypothesis.strategies.builds`,
:func:`~hypothesis.strategies.from_type` is used to fill them in.
You can also pass the special value :const:`hypothesis.infer` as a keyword
argument, to force this inference for arguments with a default value.

.. doctest::

    >>> def func(a: int, b: str):
    ...     return [a, b]
    >>> builds(func).example()
    [-6993, '']

:func:`@given <hypothesis.given>` does not perform any implicit inference
for required arguments, as this would break compatibility with pytest fixtures.
:const:`~hypothesis.infer` can be used as a keyword argument to explicitly
fill in an argument from its type annotation.

.. code:: python

    @given(a=infer)
    def test(a: int): pass
    # is equivalent to
    @given(a=integers())
    def test(a): pass

~~~~~~~~~~~
Limitations
~~~~~~~~~~~

:pep:`3107` type annotations are not supported on Python 2, and Hypothesis
does not inspect :pep:`484` type comments at runtime.  While
:func:`~hypothesis.strategies.from_type` will work as usual, inference in
:func:`~hypothesis.strategies.builds` and :func:`@given <hypothesis.given>`
will only work if you manually create the ``__annotations__`` attribute
(e.g. by using ``@annotations(...)`` and ``@returns(...)`` decorators).
The :mod:`python:typing` module is fully supported on Python 2 if you have
the backport installed.

The :mod:`python:typing` module is provisional and has a number of internal
changes between Python 3.5.0 and 3.6.1, including at minor versions.  These
are all supported on a best-effort basis, but you may encounter problems with
an old version of the module.  Please report them to us, and consider
updating to a newer version of Python as a workaround.

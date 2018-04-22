===================
Краткое руководство
===================

Этот документ должен рассказать вам обо всем, что вам нужно, чтобы начать работу с hypothesis.

----------
Пример
----------

Предположим, мы написали `run length encoding <https://en.wikipedia.org/wiki/Run-length_encoding>`_ систему, и хотим проверить, что она умеет.

У нас есть следующий код, который я взял прямо из `Rosetta Code <http://rosettacode.org/wiki/Run-length_encoding>`_ wiki (ОК, я
удалил какой-то прокомментированный код и исправил форматирование, но не модифицировал функции):


.. code:: python

  def encode(input_string):
      count = 1
      prev = ''
      lst = []
      for character in input_string:
          if character != prev:
              if prev:
                  entry = (prev, count)
                  lst.append(entry)
              count = 1
              prev = character
          else:
              count += 1
      else:
          entry = (character, count)
          lst.append(entry)
      return lst


  def decode(lst):
      q = ''
      for character, count in lst:
          q += character * count
      return q


Мы хотим написать тест для этой пары функций, который проверит некоторый инвариант из их должностных обязанностей.

Инвариант, когда у вас есть такого рода encoding / decoding заключается в том, что если вы кодируете что-то, а затем декодируете это, то получаете то же самое значение назад.  

Давайте посмотрим, как это можно сделаетье с помощью Hypothesis:


.. code:: python

  from hypothesis import given
  from hypothesis.strategies import text

  @given(text())
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

(Для этого примера мы просто позволим pytest обнаружить и запустить тест. Мы расскажем о
других способах, которыми вы могли бы запустить его, позже).

Функция text возвращает то, что Hypothesis называет стратегией поиска. Объект с методами которые описывают, как произвести и упростить некоторые виды значений. Затем  декоратор :func:`@given <hypothesis.given>` берет наш тест функции и превращает его в
параметризованный, который при вызове будет выполнять тестовую функцию по широкому диапазону совпадающих данных из этой стратегии.

Во всяком случае, этот тест сразу находит ошибку в коде:

.. code::

  Falsifying example: test_decode_inverts_encode(s='')

  UnboundLocalError: local variable 'character' referenced before assignment

*Прим*: Локальная переменная 'character', упоминается до присвоения

Hypothesis правильно указывает на то, что этот код просто неправильный, если он вызван
для пустой строки.

Если мы исправим это, просто добавив следующий код в начало функции
тогда Hypothesis скажет нам, что код правильный (ничего не делая, как вы и ожидали
проходя тест).

.. code:: python


    if not input_string:
        return []

Если бы мы хотели убедиться, что этот пример всегда будет проверяться, мы могли бы добавить его
явно:

.. code:: python

  from hypothesis import given, example
  from hypothesis.strategies import text

  @given(text())
  @example('')
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

Вам не обязательно этого делать, но это может быть полезно: как для ясности, так и для надежного поиска примеров. Также в рамках локального "обучения", в любом случае, Hypothesis будет помнить и повторно использовать примеры, но вот для обмена данными в вашей ситеме непрерывной интеграции (CI) в настоящее время нет приемлемого хорошего рабочего процесса.

Также стоит отметить, что аргументы ключевых слов example, и given могут быть как именованными, так и позиционными. Следующий код сработал бы так же хорошо:

.. code:: python

  @given(s=text())
  @example(s='')
  def test_decode_inverts_encode(s):
      assert decode(encode(s)) == s

Предположим, у нас была более интересная ошибка и мы забыли перезагрузить счетчик
в цикле. Скажем, мы пропустили строку в нашем методе ``encode``:

.. code:: python

  def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (prev, count)
                lst.append(entry)
            # count = 1  # Отсутствует операция сброса
            prev = character
        else:
            count += 1
    else:
        entry = (character, count)
        lst.append(entry)
    return lst

Hypothesis быстро проинформирует нас в следующем примере:

.. code::

  Falsifying example: test_decode_inverts_encode(s='001')

Обратите внимание, что представленный пример действительно очень прост. Hypothesis не просто
находит *любой* попавшийся пример для ваших тестов, он знает, как упростить примеры
которые он находит для создания маленьких и легко понятных. В этом случае два идентичных
значений достаточно, чтобы установить счетчик на число, отличное от одного, за которым следует
другое значение, которое должно было бы сбросить счет, но в этом случае
не сделало.

Примеры Hypothesis представляют собой действительный код Python, который вы можете запустить. Любые аргументы, которые вы явно указываете при вызове функции, не генерируются Hypothesis-ом, и если вы явно предоставляете *all* аргументы, Hypothesis просто вызовет базовую функцию один раз, а не будет запускать ее несколько раз.

----------
Установка
----------

Hypothesis является :pypi:`available on pypi as "hypothesis" <hypothesis>`. Вы можете установить его с помощью:

.. code:: bash

  pip install hypothesis

Если вы хотите установить непосредственно из исходного кода (например, потому что вы хотите
внести изменения и установить измененную версию) вы можете сделать это с:

.. code:: bash

  pip install -e .

Вы, вероятно, должны сначала запустить тесты, чтобы убедиться, что ничего не сломано. Вы можете сделать это так:

.. code:: bash

  python setup.py test

Обратите внимание, что если они еще не установлены, будет предпринята попытка установить тестовые зависимости.

Вы можете сделать все это в `virtualenv <https://virtualenv.pypa.io/en/latest/>`_. Например:

.. code:: bash

  virtualenv venv
  source venv/bin/activate
  pip install hypothesis

Создаст изолированную среду для вас, чтобы попробовать Hypothesis, не затрагивая установленные пакеты системы.

-------------
Running tests
-------------

In our example above we just let pytest discover and run our tests, but we could
also have run it explicitly ourselves:

.. code:: python

  if __name__ == '__main__':
      test_decode_inverts_encode()

We could also have done this as a :class:`python:unittest.TestCase`:

.. code:: python

  import unittest

  class TestEncoding(unittest.TestCase):
      @given(text())
      def test_decode_inverts_encode(self, s):
          self.assertEqual(decode(encode(s)), s)

  if __name__ == '__main__':
      unittest.main()

A detail: This works because Hypothesis ignores any arguments it hasn't been
told to provide (positional arguments start from the right), so the self
argument to the test is simply ignored and works as normal. This also means
that Hypothesis will play nicely with other ways of parameterizing tests. e.g
it works fine if you use pytest fixtures for some arguments and Hypothesis for
others.

-------------
Writing tests
-------------

A test in Hypothesis consists of two parts: A function that looks like a normal
test in your test framework of choice but with some additional arguments, and
a :func:`@given <hypothesis.given>` decorator that specifies
how to provide those arguments.

Here are some other examples of how you could use that:


.. code:: python

    from hypothesis import given
    import hypothesis.strategies as st

    @given(st.integers(), st.integers())
    def test_ints_are_commutative(x, y):
        assert x + y == y + x

    @given(x=st.integers(), y=st.integers())
    def test_ints_cancel(x, y):
        assert (x + y) - y == x

    @given(st.lists(st.integers()))
    def test_reversing_twice_gives_same_list(xs):
        # This will generate lists of arbitrary length (usually between 0 and
        # 100 elements) whose elements are integers.
        ys = list(xs)
        ys.reverse()
        ys.reverse()
        assert xs == ys

    @given(st.tuples(st.booleans(), st.text()))
    def test_look_tuples_work_too(t):
        # A tuple is generated as the one you provided, with the corresponding
        # types in those positions.
        assert len(t) == 2
        assert isinstance(t[0], bool)
        assert isinstance(t[1], str)


Note that as we saw in the above example you can pass arguments to :func:`@given <hypothesis.given>`
either as positional or as keywords.

--------------
Where to start
--------------

You should now know enough of the basics to write some tests for your code
using Hypothesis. The best way to learn is by doing, so go have a try.

If you're stuck for ideas for how to use this sort of test for your code, here
are some good starting points:

1. Try just calling functions with appropriate random data and see if they
   crash. You may be surprised how often this works. e.g. note that the first
   bug we found in the encoding example didn't even get as far as our
   assertion: It crashed because it couldn't handle the data we gave it, not
   because it did the wrong thing.
2. Look for duplication in your tests. Are there any cases where you're testing
   the same thing with multiple different examples? Can you generalise that to
   a single test using Hypothesis?
3. `This piece is designed for an F# implementation
   <https://fsharpforfunandprofit.com/posts/property-based-testing-2/>`_, but
   is still very good advice which you may find helps give you good ideas for
   using Hypothesis.

If you have any trouble getting started, don't feel shy about
:doc:`asking for help <community>`.

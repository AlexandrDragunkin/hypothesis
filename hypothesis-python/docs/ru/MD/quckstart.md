Краткое руководство
===================

Этот документ должен рассказать вам обо всем, что вам нужно, чтобы начать работу с hypothesis.


Пример
----------

Предположим, мы написали [run length encoding](https://en.wikipedia.org/wiki/Run-length_encoding)  систему, и хотим проверить, что она умеет.

У нас есть следующий код, который я взял прямо из [Rosetta Code wiki](http://rosettacode.org/wiki/Run-length_encoding) (ОК, я
удалил какой-то прокомментированный код и исправил форматирование, но не модифицировал функции):


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

Инвариант, когда у вас есть такого рода `encoding/decoding` заключается в том, что если вы кодируете что-то, а затем декодируете это, то получаете то же самое значение назад.  

Давайте посмотрим, как это можно сделать с помощью Hypothesis:


	  from hypothesis import given
	  from hypothesis.strategies import text
	
	  @given(text())
	  def test_decode_inverts_encode(s):
	      assert decode(encode(s)) == s

(Для этого примера мы просто позволим *pytest* обнаружить и запустить тест. О других способах, которыми вы могли бы запустить его, мы расскажем позже).

Функция text возвращает то, что Hypothesis называет стратегией поиска. Объект с методами которые описывают, как произвести и упростить некоторые виды значений. Затем  декоратор `@given` берет наш тест функции и превращает его в
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
Выполнение тестов
-------------

В нашем примере выше мы просто позволяем pytest обнаружить и запустить наши тесты, но мы также могли бы запустить его явно сами:

.. code:: python

  if __name__ == '__main__':
      test_decode_inverts_encode()

Или так :class:`python:unittest.TestCase`:

.. code:: python

  import unittest

  class TestEncoding(unittest.TestCase):
      @given(text())
      def test_decode_inverts_encode(self, s):
          self.assertEqual(decode(encode(s)), s)

  if __name__ == '__main__':
      unittest.main()

Примечание: это работает, потому что Hypothesis игнорирует любые аргументы, которые ему не было сказано предоставить (позиционные аргументы начинаются справа), поэтому аргумент self для теста просто игнорируется и работает как обычно. Это также означает, что Hypothesis будет хорошо играть с другими способами параметризации тестов. Например, он отлично работает, если вы используете приспособления pytest для некоторых аргументов и Hypothesis для других.

----------------
Написание тестов
----------------

A test in Hypothesis consists of two parts: A function that looks like a normal test in your test framework of choice but with some additional arguments, and a :func:`@given <hypothesis.given>` decorator that specifies how to provide those arguments.

Here are some other examples of how you could use that:

Тест в Hypothesis состоит из двух частей: функции, которая выглядит как обычный тест в выбранной тестовой структуре, но с некоторыми дополнительными аргументами, и декоратора :func:`@given <hypothesis.given>`, который указывает, как предоставить эти аргументы.

Вот некоторые другие примеры того, как можно это использовать:


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


Обратите внимание, что, как мы видели в приведенном выше примере, вы можете передать аргументы :func:`@given <hypothesis.given>` как позиционные или именованные.

--------------
С чего начать
--------------

Теперь вы знаете достаточно об основах, чтобы написать какие то тесты для вашего кода с помощью Hypothesis. Лучший способ учиться - это сделать, так что попробуйте.

Если у вас туговато с идеями о том, как использовать этот вид теста для вашего кода, вот несколько подсказок:

1. Попробуйте просто вызвать функции с соответствующими случайными данными и получите в них сбой. Вы возможно будете удивлены, как часто это работает. Например, обратите внимание, что первая ошибка, которую мы обнаружили в примере кодирования, даже не дошла до нашего утверждения: она потерпела крах, потому что она не смогла обработать данные, которые мы дали, а не потому, что произошло что то не правильное.
2. Поищите дублирование в своих тестах. Есть ли случаи, когда вы тестируете одно и то же с несколькими разными примерами? Можете ли вы обобщить это в один тест, используя Hypothesis?
3. `Эта часть предназначена для реализации на F#
   <https://fsharpforfunandprofit.com/posts/property-based-testing-2/>`_, но по-прежнему очень полезна для помощи в поиске хороших идеи для использования Hypothesis.

Если у вас возникли проблемы с запуском, не стесняйтесь и обращайтесь
:doc:`asking for help <community>`.
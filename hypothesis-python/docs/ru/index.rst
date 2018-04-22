==============================
Добро пожаловать в Hypothesis!
==============================

`Hypothesis <http://hypothesis.works>`_ 
представляет собой библиотеку Python для создания модульных тестов, которые попроще писать и более эффективны при запуске, обнаруживая граничные случаи в коде, который вы бы не подумали искать. Он стабильный, мощный и легко добавляется в любой существующий набор тестов.

Алгоритм его работы, позволяя вам писать тесты, которые утверждают, что что-то должно быть истинным для каждого случая, а не только то, о чём вы догадались подумать.

Нормальный модульный тест - это что-то вроде следующего:

1. Подготовте некоторые данные.
2. Выполнените некоторыеоперации с данными.
3. Подтвердите результат.

Hypothesis позволяет писать тесты, которые выглядят следующим образом:

1. Для всех данных, соответствующих некоторым спецификациям.
2. Выполните некоторые операции с данными.
3. Подтвердите результат.

Это часто называют property based testing, и было популяризировано в библиотеке Haskell `Quickcheck <https://hackage.haskell.org/package/QuickCheck>`_.


It works by generating random data matching your specification and checking
that your guarantee still holds in that case. If it finds an example where it doesn't,
it takes that example and cuts it down to size, simplifying it until it finds a
much smaller example that still causes the problem. It then saves that example
for later, so that once it has found a problem with your code it will not forget
it in the future.

Writing tests of this form usually consists of deciding on guarantees that
your code should make - properties that should always hold true,
regardless of what the world throws at you. Examples of such guarantees
might be:

* Your code shouldn't throw an exception, or should only throw a particular type of exception (this works particularly well if you have a lot of internal assertions).
* If you delete an object, it is no longer visible.
* If you serialize and then deserialize a value, then you get the same value back.

Now you know the basics of what Hypothesis does, the rest of this
documentation will take you through how and why. It's divided into a
number of sections, which you can see in the sidebar (or the
menu at the top if you're on mobile), but you probably want to begin with
the :doc:`Quick start guide <quickstart>`, which will give you a worked
example of how to use Hypothesis and a detailed outline
of the things you need to know to begin testing your code with it, or
check out some of the
`introductory articles <http://hypothesis.works/articles/intro/>`_.


.. toctree::
  :maxdepth: 1
  :hidden:

  quickstart
  details
  settings
  data
  extras
  django
  numpy
  healthchecks
  database
  stateful
  supported
  examples
  community
  manifesto
  endorsements
  usage
  strategies
  changes
  development
  support
  packaging
  reproducing

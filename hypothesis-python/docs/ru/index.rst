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


Он работает путем генерации случайных данных, соответствующих вашей спецификации и проверки
что ваша функция или метод все еще держится и не падает в этом случае. Если он найдет пример, где это не так,
он примет этот пример и сократит его размер, упрощая его, пока не найдет
гораздо меньший пример, который все еще вызывает проблему. Затем он сохранит этот пример
для последующего, так что как только он нашел проблему с вашим кодом он не забудет
этого в будущем.

Написание тестов в такой форме обычно состоит из решения о гарантиях, по которым ваш код должен делать make - properties, которые должны всегда иметь значение true, независимо от того, что мир преподнесет вам. Примерами таких гарантий могут быть:

* Ваш код не должен генерировать исключение или должен вызывать только особый тип исключения (это работает особенно хорошо, если у вас много внутренних assert-ов).
* При удалении объекта он больше не отображается.
* Если вы сериализуете и затем десериализуете значение, вы получите то же значение обратно.

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

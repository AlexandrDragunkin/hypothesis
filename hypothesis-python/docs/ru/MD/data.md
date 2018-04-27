# Что можно генерировать и как #
*Большинство объектов самых разных типов должно быть легко сгенерированы, и все должно быть возможно.*

Для поддержки этого принципа Hypothesis предоставляет стратегии для большинства встроенных типов с аргументами для ограничения или корректировки вывода, а также стратегий более высокого порядка, которые могут быть скомпонованы для создания более сложных типов.

Этот документ является руководством к тому, какие стратегии доступны для генерации данных и как их создавать. Стратегии имеют множество других важных внутренних функций, например, как упрощать, но данные, которые они могут генерировать, являются единственной публичной частью их API.

Функции для построения стратегий доступны в модуле hypothesis.strategies. Основные функции из него заключаются в следующем:

> **hypothesis.strategies.nothing()**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#nothing)]

Эта стратегия никогда не будет успешно использовать значение и всегда будет отклоняться при попытке привлечь.

Примеры из этой стратегии не сокращаются (потому что их нет).

> **hypothesis.strategies.just(value)**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#just)]

Возвращает стратегию, которая генерирует только значение.

***Примечание:*** значение не копируется. Будьте осторожны при использовании изменяемых значений.

Если value является результатом callable, вы можете использовать `builds(callable)` вместо `just(callable())`, чтобы каждый раз получать новое значение.

Примеры из этой стратегии не сжимаются (потому что существует один в единственном экземпляре).

> **hypothesis.strategies.none()**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#none)]

Возвращает стратегию, которая генерирует только None.

Примеры из этой стратегии не сжимаются (потому что существует один в единственном экземпляре).

> **hypothesis.strategies.one_of(*args)**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#one_of)]

Возвращает стратегию, которая генерирует значения из любой стратегии аргументов.

Это может быть вызвано с одним iterable аргументом вместо нескольких аргументов стратегии. В этом случае `one_of(x)` и `one_of(*x)` эквивалентны.

Примеры из этой стратегии, как правило, сокращаются до тех, которые исходят из стратегий ранее в списке, а затем сокращаются в соответствии с поведением стратегии, которая их создала. Для того, чтобы получить хорошее сокращающееся поведение, попробуйте поставить более простые стратегии в первую очередь. *Например:* `one_of(none(), text())` лучше, чем `one_of(text(), none())`.

Это особенно важно при использовании рекурсивных стратегий. *Например:* `x = st.deferred(lambda: st.none() | st.tuples(x, x))` будет хорошо сжиматься, `but x = st.deferred(lambda: st.tuples(x, x) | st.none())` будет сокращаться действительно очень плохо.

> **hypothesis.strategies.integers(min_value=None, max_value=None)**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#integers)]

Возвращает стратегию, которая генерирует целые числа (в Python 2 это могут быть ints или longs).

Если `min_value` не равно *None*, то все значения будут `>= min_value`. Если `max_value` не равно *None*, то все значения будут `<= max_value`

Примеры из этой стратегии будут стремиться к нулю, а отрицательные значения также будут сокращаться до положительных (т.е. `-n` может быть заменено на `+n`).

> **hypothesis.strategies.booleans()**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#booleans)]

Возвращает стратегию, которая генерирует экземпляры bool.

Примеры из этой стратегии будут сокращаться в сторону False (т. е. сжатие будет пытаться заменить True на False, где это возможно).

> **hypothesis.strategies.floats(min_value=None, max_value=None, allow_nan=None, allow_infinity=None)**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#floats)]

Возвращает стратегию, которая генерирует float.

 - Если `min_value` не равно *None*, все значения будут `>= min_value`.
 - Если `max_value` не равно *None*, все значения будут `<= max_value`.
 - Если `min_value` или `max_value` не равны *None* , при включении `allow_nan` возникнет ошибка.
 - Если оба значения `min_value` и `max_value` не равны *None*, при включении `allow_infinity` возникнет ошибка.

Где явно не исключаются границы, все варианты бесконечности, - *infinity* и *NaN* являются возможными значениями, генерируемыми этой стратегией.

Examples from this strategy have a complicated and hard to explain shrinking behaviour, but it tries to improve “human readability”. Finite numbers will be preferred to infinity and infinity will be preferred to NaN.

Примеры из этой стратегии сложны и трудны для объяснения сокращающегося поведения, но она пытается улучшить «удобочитаемость человеком». Конечные числа будут предпочтительнее infinity, и infinity будет предпочтительнее NaN.
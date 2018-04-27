# Что можно генерировать и как #
*Большинство объектов самых разных типов должно быть легко сгенерированы, и все должно быть возможно.*

Для поддержки этого принципа Hypothesis предоставляет стратегии для большинства встроенных типов с аргументами для ограничения или корректировки вывода, а также стратегий более высокого порядка, которые могут быть скомпонованы для создания более сложных типов.

Этот документ является руководством к тому, какие стратегии доступны для генерации данных и как их создавать. Стратегии имеют множество других важных внутренних функций, например, как упрощать, но данные, которые они могут генерировать, являются единственной публичной частью их API.

Функции для построения стратегий доступны в модуле hypothesis.strategies. Основные функции из него заключаются в следующем:

> **hypothesis.strategies.nothing()**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#nothing)]
Эта стратегия никогда не будет успешно использовать значение и всегда будет отклоняться при попытке привлечь.

Примеры из этой стратегии не сокращаются (потому что их нет).

> **hypothesis.strategies.just(value)**[[source](https://hypothesis.readthedocs.io/en/latest/_modules/hypothesis/strategies.html#just)]
Return a strategy which only generates value.

Note: value is not copied. Be wary of using mutable values.

If value is the result of a callable, you can use builds(callable) instead of just(callable()) to get a fresh value each time.

Examples from this strategy do not shrink (because there is only one).

Возвращает стратегию, которая генерирует только значение.

***Примечание:*** значение не копируется. Будьте осторожны при использовании изменяемых значений.

Если value является результатом callable, вы можете использовать `builds(callable)` вместо `just(callable())`, чтобы каждый раз получать новое значение.

Примеры из этой стратегии не сжимаются (потому что существует в единственном экземпляре).

hypothesis.strategies.none()[source]
Return a strategy which only generates None.

Examples from this strategy do not shrink (because there is only one).
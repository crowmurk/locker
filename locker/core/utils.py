import copy

from django.utils.text import slugify


def get_unique_slug(instance, slug_field, *args, **kwargs):
    """ Генерирует уникальный slug.

    Args:
        instance - экземпляр модели
        slug_field - строка с именем поля в котором хранится slug
        args - источник для создания slug:
            строки с  именами полей экземпляра или
            строки значений для создания slug

    Kwargs:
        unique=True - должен ли slug быть уникальным или
        unique_for= () - строка или список строк с именами полей
            экземпляра с учетом которых slug должен быть уникальным
        prohibit = () - строка или  список строк запрещенных значений slug

    Returns:
        строку с уникальным slug
    """
    def tuple_from_kwarg(name, **kwargs):
        """Создает tuple из значения именованного аргумента.
        Значение должно быть строкой или списком строк.
        """
        value = kwargs.get(name, None)
        if value is None:
            return tuple()
        if isinstance(value, str):
            return (value, )
        if any([isinstance(value, item) for item in (list, tuple, set)]):
            if all([isinstance(item, str) for item in value]):
                return tuple(set(value))

        raise ValueError(
            "'{}' argument must be str or iterable of str.".format(name)
        )

    # Получаем значения полей экземпляра из которых создается slug
    if args and all([isinstance(arg, str) for arg in args]):
        source = [getattr(instance, arg, arg) for arg in args]
    else:
        raise ValueError("Slug source must be str type.")

    # Составляем список запрещенных slug
    prohibit = ['create', 'update', 'delete']
    prohibit.extend(tuple_from_kwarg('prohibit', **kwargs))

    # Должен ли slug быть уникальным
    unique = kwargs.get('unique', True)
    unique_for = tuple_from_kwarg('unique_for', **kwargs)

    # Для уникальности будем создавать slug вида slug-1, slug-2, slug-n
    slugExtension = 1

    # Создаем slug
    slug = slugify(
        '-'.join([str(item) for item in source]),
        allow_unicode=True,
    )

    # Уникальность slug не требуется
    if not (unique or unique_for):
        if slug in prohibit:
            return "{}-{}".format(slug, slugExtension)
        return slug

    # Создаем уникальный slug
    if slug in prohibit:
        unique_slug = '{}-{}'.format(slug, slugExtension)
        slugExtension += 1
    else:
        unique_slug = slug

    # Формируем словарь для фильтра модели
    filter_dict = {slug_field: unique_slug}
    filter_dict.update(
        {field: getattr(instance, field) for field in unique_for}
    )

    # Пока slug не будет уникальным
    while instance.__class__.objects.filter(
        **filter_dict,
    ).exclude(id=instance.id).exists():
        # Генерируем новый slug
        unique_slug = '{}-{}'.format(slug, slugExtension)
        filter_dict.update({slug_field: unique_slug})
        slugExtension += 1

    return unique_slug


class Slug:
    default_prohibit = ['create', 'update', 'delete']

    def __init__(self, slug, *source, **kwargs):
        """ Генерирует slug.

        Args:
            slug   - строка с именем поля в котором хранится slug
            source - источник для создания slug:
                     строки с  именами полей экземпляра или
                     строки значений для создания slug

        Kwargs:
            unique=True - должен ли slug быть уникальным или
            unique_for  - iterable - строка или список строк с именами полей
                          экземпляра с учетом которых slug должен быть уникальным
            prohibit    - iterable - строка или  список строк запрещенных значений slug
        """

        # Имя поля slug
        self.slug = slug

        # Имена полей из которых создается slug
        self.source = source

        # Список запрещенных значений slug
        self.prohibit = kwargs.get('prohibit')

        # Должен ли slug быть уникальным
        self.unique = kwargs.get('unique', True)
        self.unique_for = kwargs.get('unique_for')

    def _get_iterable(self, value, *, _type=tuple):
        if value is None:
            return _type()
        if isinstance(value, str):
            return _type((value, ))
        if any((isinstance(value, item) for item in (list, tuple, set))):
            if all([isinstance(item, str) for item in value]):
                return _type(set(value))

        raise ValueError(
            "'{}' argument must be str or iterable of str.".format(value)
        )

    @property
    def slug(self):
        try:
            return self._slug
        except AttributeError:
            return ''

    @slug.setter
    def slug(self, value):
        if isinstance(value, str):
            self._slug = value
        else:
            raise ValueError('Slug property must be str type.')

    @property
    def unique(self):
        try:
            return self._unique
        except AttributeError:
            return True

    @unique.setter
    def unique(self, value):
        if isinstance(value, bool):
            self._unique = value
        else:
            raise ValueError('Unique property must be bool type.')

    @property
    def unique_for(self):
        try:
            return self._unique_for
        except AttributeError:
            return ()

    @unique_for.setter
    def unique_for(self, value):
        try:
            self._unique_for = self._get_iterable(value)
        except ValueError:
            raise ValueError('Unique_for property must be str type or iterable of str.')

    @property
    def source(self):
        try:
            return self._source
        except AttributeError:
            return ()

    @source.setter
    def source(self, value):
        try:
            self._source = self._get_iterable(value)
        except ValueError:
            raise ValueError('Source property must be str type or iterable of str.')

    @property
    def prohibit(self):
        try:
            return self._prohibit
        except AttributeError:
            return self.default_prohibit

    @prohibit.setter
    def prohibit(self, value):
        try:
            _prohibit = copy.copy(self.default_prohibit)
            _prohibit.extend(self._get_iterable(value))
            self._prohibit = list(set(_prohibit))
        except ValueError:
            raise ValueError('Prohibit property must be str or iterable of str.')

    def slugify(self, instance):
        """ Генерирует slug.

        Args:
            instance - экземпляр модели

        Returns:
            строку содержащюю slug
        """
        # Получаем значения полей экземпляра из которых создается slug
        source = [getattr(instance, item, item) for item in self.source]

        # Для уникальности будем создавать slug вида slug-1, slug-2, slug-n
        slugExtension = 1

        # Создаем slug
        slug = slugify(
            '-'.join([str(item) for item in source]),
            allow_unicode=True,
        )

        # Уникальность slug не требуется
        if not (self.unique or self.unique_for):
            if slug in self.prohibit:
                return "{}-{}".format(slug, slugExtension)
            return slug

        # Создаем уникальный slug
        if slug in self.prohibit:
            unique_slug = '{}-{}'.format(slug, slugExtension)
            slugExtension += 1
        else:
            unique_slug = slug

        # Формируем словарь для фильтра модели
        filter_dict = {self.slug: unique_slug}
        filter_dict.update(
            {field: getattr(instance, field) for field in self.unique_for}
        )

        # Пока slug не будет уникальным
        while instance.__class__.objects.filter(
            **filter_dict,
        ).exclude(id=instance.id).exists():
            # Генерируем новый slug
            unique_slug = '{}-{}'.format(slug, slugExtension)
            filter_dict.update({self.slug: unique_slug})
            slugExtension += 1

        return unique_slug

    def bulk_slugify(self, bulk):
        # Проверяем переданые аргументы
        if not bulk:
            return

        # Проверяем переданые аргументы
        if not all((isinstance(instance, type(bulk[0])) for instance in bulk)):
            raise ValueError("All instances must be same type")

        existed_slugs = bulk[0].__class__.objects.values_list('slug', flat=True)
        bulk_slugs = set([instance.slug for instance in bulk])

        for instance in bulk:
            # Получаем значения полей экземпляра из которых создается slug
            source = [getattr(instance, item, item) for item in self.source]

            # Для уникальности будем создавать slug вида slug-1, slug-2, slug-n
            slugExtension = 1

            # Создаем slug
            slug = slugify(
                '-'.join([str(item) for item in source]),
                allow_unicode=True,
            )

            # Уникальность slug не требуется
            if not self.unique:
                if slug in self.prohibit:
                    return "{}-{}".format(slug, slugExtension)
                return slug

            # Создаем уникальный slug
            if slug in self.prohibit:
                unique_slug = '{}-{}'.format(slug, slugExtension)
                slugExtension += 1
            else:
                unique_slug = slug

            # Пока slug не будет уникальным
            while unique_slug in existed_slugs or unique_slug in bulk_slugs:
                # Генерируем новый slug
                unique_slug = '{}-{}'.format(slug, slugExtension)
                slugExtension += 1

            instance.slug = unique_slug
            bulk_slugs.add(unique_slug)

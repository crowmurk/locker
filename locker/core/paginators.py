import string
import operator

from django.utils.translation import gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger


class AlphabetPaginator:
    """Pagination for string-based objects.
    """

    def __init__(self, object_list, per_page=25, *args, **kwargs):
        self.object_list = object_list
        self.count = len(object_list)
        self.pages = []

        # At least one page exists
        if not self.count:
            self.pages.append(AlphabetPage(self))

        # Chunk up the objects so we don't need to
        # iterate over the whole list for each letter
        chunks = {}

        on = kwargs.get('on', None)
        for obj in self.object_list:
            if on:
                obj_str = str(operator.attrgetter(on)(obj))
            else:
                obj_str = str(obj)

            letter = str.upper(obj_str[0])

            if letter not in chunks:
                chunks[letter] = []

            chunks[letter].append(obj)

        # The process for assigning objects to each page
        current_page = AlphabetPage(self)

        for letter in string.ascii_uppercase:
            if letter not in chunks:
                current_page.add([], letter)
                continue

            # The items in object_list starting with this letter
            sub_list = chunks[letter]

            new_page_count = len(sub_list) + len(current_page)
            # First, check to see if sub_list will fit or it needs to go onto
            # a new page. If assigning this list will cause the page to overflow
            # and an underflow is closer to per_page than an overflow
            # and the page isn't empty (which means len(sub_list) > per_page)...
            if new_page_count > per_page and \
                    abs(per_page - len(current_page)) < abs(per_page - new_page_count) and \
                    len(current_page) > 0:
                # Make a new page
                self.pages.append(current_page)
                current_page = AlphabetPage(self)

            current_page.add(sub_list, letter)

        # if we finished the for loop with a page that isn't empty, add it
        if len(current_page) > 0:
            self.pages.append(current_page)

    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)

    def validate_number(self, number):
        """Validate the given 1-based page number.
        """
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))

        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.num_pages:
            raise EmptyPage(_('That page contains no results'))

        return number

    def page(self, num):
        """Returns a Page object for the given 1-based page number.
        """
        try:
            number = self.validate_number(num)
        except PageNotAnInteger:
            if len(num) == 1 and num.upper() in string.ascii_uppercase:
                for page in self.pages:
                    if num.upper() in page.letters:
                        return page
            number = 1
        except EmptyPage:
            number = self.num_pages

        return self.pages[number - 1]

    @property
    def num_pages(self):
        """Returns the total number of pages.
        """
        return len(self.pages)

    @property
    def page_range(self):
        """ Return a 1-based range of pages for iterating
        through within a template for loop.
        """
        return range(1, self.num_pages + 1)

class AlphabetPage:
    def __init__(self, paginator):
        self.object_list = []
        self.letters = []
        self.paginator = paginator

    def __repr__(self):
        if self.start_letter == self.end_letter:
            return self.start_letter
        else:
            return '%c-%c' % (self.start_letter, self.end_letter)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                'Page indices must be integers or slices, not %s.'
                % type(index).__name__
            )
        # The object_list is converted to a list so that if it was
        # a QuerySet it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    @property
    def start_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else:
            return None

    @property
    def end_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else:
            return None

    @property
    def number(self):
        return self.paginator.pages.index(self) + 1

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)

    def add(self, new_list, letter=None):
        if len(new_list) > 0:
            self.object_list = self.object_list + new_list
        if letter:
            self.letters.append(letter)

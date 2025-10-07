class Author:
    def __init__(self, name):
        self._name = None
        self.name = name  # use the setter

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        """
        Allow setting only once. Subsequent attempts are ignored
        (no AttributeError), matching the tests' expectation.
        """
        if self._name is not None:
            return
        if isinstance(value, str) and len(value) > 0:
            self._name = value

    # ---- relationships ----
    def articles(self):
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        mags = [a.magazine for a in self.articles() if a.magazine is not None]
        seen, unique = set(), []
        for m in mags:
            if m not in seen:
                seen.add(m)
                unique.append(m)
        return unique

    # ---- aggregates / helpers ----
    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        mags = self.magazines()
        if not mags:
            return None
        cats = [m.category for m in mags if isinstance(m.category, str)]
        seen, unique = set(), []
        for c in cats:
            if c not in seen:
                seen.add(c)
                unique.append(c)
        return unique


class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        Magazine.all.append(self)

    # ---- name (mutable, 2..16) ----
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    # ---- category (mutable, len>0) ----
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    # ---- relationships ----
    def articles(self):
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        authors = [a.author for a in self.articles() if a.author is not None]
        seen, unique = set(), []
        for au in authors:
            if au not in seen:
                seen.add(au)
                unique.append(au)
        return unique

    # ---- aggregates ----
    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        counts = {}
        for a in self.articles():
            au = a.author
            if au:
                counts[au] = counts.get(au, 0) + 1
        result = [au for au, n in counts.items() if n > 2]
        return result if result else None

    # ---- bonus ----
    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        counts = {}
        for a in Article.all:
            m = a.magazine
            if m:
                counts[m] = counts.get(m, 0) + 1
        if not counts:
            return None
        return max(counts, key=counts.get)


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._title = None
        self._author = None
        self._magazine = None

        self.title = title
        self.author = author
        self.magazine = magazine

        Article.all.append(self)

    # ---- title (immutable, 5..50) ----
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, "_title") and self._title is not None:
            return
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value

    # ---- author (changeable, type Author) ----
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    # ---- magazine (changeable, type Magazine) ----
    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
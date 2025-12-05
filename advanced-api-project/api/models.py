from django.db import models

class Author(models.Model):
    """
    Represents a single author in the system.

    This model is intentionally simple for demonstration purposes:
    it only stores the author's name. However, it serves as the
    "parent" in a one-to-many relationship with books: one
    Author can be linked to many Book instances.
    """
    name = models.CharField(max_length=255, help_text="Full name of the author.")

    def __str__(self) -> str:
        # Human-readable string representation in admin / shell
        return self.name


class Book(models.Model):
    """
    Represents a single book in the system.

    Fields:
      - title: Human-readable title of the book.
      - publication_year: Calendar year in which the book was published.
      - author: ForeignKey to Author, defining a one-to-many relationship.
        Each Book is linked to exactly one Author, while an Author can
        have many related Book instances.

    The related_name='books' on the ForeignKey allows us to access all
    books for a given author using: author_instance.books.all().
    This is important for nested serializers in DRF.
    """
    title = models.CharField(
        max_length=255,
        help_text="Title of the book.",
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published (e.g. 1999).",
    )
    author = models.ForeignKey(
        Author,
        related_name='books',  # used for nested serializers
        on_delete=models.CASCADE,
        help_text="The author who wrote this book.",
    )

    def __str__(self) -> str:
        # Useful representation when printing/inspecting objects
        return f"{self.title} ({self.publication_year})"
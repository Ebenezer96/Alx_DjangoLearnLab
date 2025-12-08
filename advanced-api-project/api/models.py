from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, help_text="Full name of the author.")

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        help_text="Title of the book.",
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published (e.g. 1999).",
    )
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE,
        help_text="The author who wrote this book.",
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"

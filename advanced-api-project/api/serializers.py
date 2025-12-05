from datetime import date

from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    - Exposes all fields: id, title, publication_year, author.
    - Adds custom validation on publication_year to ensure
      it is not in the future, which would be invalid for a
      real, already-published book.

    This serializer can be used both standalone or as a nested
    serializer inside AuthorSerializer.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value: int) -> int:
        """
        Field-level validation for publication_year.

        Ensures we do not allow a publication year in the future.
        This is a simple data integrity rule that demonstrates
        how custom validation logic is implemented in DRF.

        Called automatically by DRF when validating this field.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (current year: {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested books.

    - Includes the 'name' field from Author.
    - Adds a nested representation of all related books using
      BookSerializer (via the 'books' related_name on the Book.author FK).

    This demonstrates how nested serializers can be used to
    return complex, hierarchical data structures. For example,
    serializing an Author instance will produce something like:

    {
        "id": 1,
        "name": "George Orwell",
        "books": [
            {
                "id": 10,
                "title": "1984",
                "publication_year": 1949,
                "author": 1
            },
            ...
        ]
    }

    Note:
    - books is read-only here by design; this keeps write logic
      simple and avoids needing to handle nested writes. If you
      wanted to create/update books together with an author, you
      would remove read_only=True and override create()/update().
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

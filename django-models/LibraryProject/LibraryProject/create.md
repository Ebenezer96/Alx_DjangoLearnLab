# Create Operation

### Command:
```python
from bookstore.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

book


# Retrieve Operation

### Command:
```python
from bookstore.models import Book

books = Book.objects.all()
books[0].title, books[0].author, books[0].publication_year


---

### **update.md**

```markdown
# Update Operation

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the update
updated_book = Book.objects.get(id=book.id)
print(updated_book.title)

# Expected Output:
# Nineteen Eighty-Four


---

### **delete.md**

```markdown
# Delete Operation

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
Book.objects.all()

# Expected Output:
# <QuerySet []>

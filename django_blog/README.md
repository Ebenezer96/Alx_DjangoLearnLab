📝 Comment System Documentation

The Django Blog application includes a fully integrated comment system that enables authenticated users to engage with blog posts through commenting, editing, and deleting their own contributions. This document summarizes how the feature works, the associated permissions, and the technical structure behind it.

📌 Overview

Each blog post supports a thread of user comments.
A comment contains:

The post it belongs to

The author

The text content

Timestamps for creation and last update

Comments are displayed on the post detail page.
Anonymous visitors may read comments but cannot interact with them.

✍️ Adding a Comment
Who can add comments?

Only authenticated users.

How to add a comment

Visit any blog post:

/post/<post_id>/


Scroll to the Add a Comment section.

Write a message and click Post Comment.

Behavior

The comment is validated using CommentForm.

author is set to the current user.

post is determined from the URL (post_id).

The user is redirected back to the post detail page.

✏️ Editing a Comment
Who can edit comments?

Only the original author.

Edit process

Go to the post where your comment appears.

Under your comment, click Edit.

Modify your text.

Save changes.

Rules

Only authors see the Edit link.

Unauthorized access to an edit URL results in a 403 or redirect.

updated_at timestamp is automatically refreshed.

🗑️ Deleting a Comment
Who can delete comments?

Only the original author.

Delete process

Click the Delete link under your comment.

Confirm deletion on the delete confirmation page.

You will return to the post detail page.

Notes

Deleted comments cannot be restored.

Only authors see the Delete link.

👁️ Comment Visibility Rules
User Type	View	Add	Edit	Delete
Anonymous Visitor	✔ Yes	❌ No	❌ No	❌ No
Authenticated User	✔ Yes	✔ Yes	Only their own	Only their own
Admin/Superuser	✔ Yes	✔ Yes	Via admin site	Via admin site

This maintains clean and safe interaction between users.

🧩 URL Structure
Purpose	URL Pattern
Create Comment	/post/<post_id>/comment/new/
Edit Comment	/comment/<comment_id>/update/
Delete Comment	/comment/<comment_id>/delete/

These routes are protected using Django mixins for authentication and authorization.

🏗️ Technical Components
Model

The Comment model includes:

post → ForeignKey to Post

author → ForeignKey to User

content → TextField

created_at → DateTimeField

updated_at → DateTimeField

Forms

CommentForm handles input validation and rendering for both creating and updating comments.

Views

Three class-based views manage comment interactions:

CommentCreateView

CommentUpdateView

CommentDeleteView

Built with:

LoginRequiredMixin
UserPassesTestMixin

Templates

comment_form.html (edit form)

comment_confirm_delete.html (delete confirmation page)

Comments displayed inside post_detail.html

🧪 Testing Checklist

Ensure the following behaviors work correctly:

✔ Authenticated users can post comments

✔ Anonymous users cannot post

✔ Only the author can edit or delete

✔ Attempting unauthorized edits/deletes is blocked

✔ After create/update/delete, redirect goes back to the post

✔ Comments appear only under the correct post

✔ XSS is escaped (HTML inside comments is sanitized)

🎉 Conclusion

The comment system adds meaningful interactivity to the blog by enabling discussion while enforcing strict user permissions. It is built with maintainability in mind using Django's generic class-based views, mixins, and modular templates.
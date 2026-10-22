from django.db import models
class Publisher(models.Model):
    """A company that publishes books"""
    name = models.CharField(max_length=100, help_text='The name of the publisher')
    website = models.URLField( help_text="The Publisher's website")
    email = models.EmailField( help_text="The Publisher's email address")
    def __str__(self):
        return self.name
class Contributor(models.Model):
    """A contributor to a book, e.g. author, editor, co-author."""
    first_names = models.CharField(max_length=50, help_text="The contributor's first name or names")
    last_names = models.CharField(max_length=50, help_text="The contributor's last name or names")
    email = models.EmailField( help_text="The contact email for the contributor")
    def initialled_name(self):
        names = self.first_names.split()
        initials = ''
        for name in names:
            initials += name[0]
        return self.last_names + ', ' + initials

    def __str__(self):
        return self.initialled_name()

class Book(models.Model):
    "A pulished book"
    title = models.CharField(max_length=70, help_text="The title of the book")
    publication_date = models.DateField(verbose_name= "Date the book was published")
    isbn= models.CharField( max_length=20, verbose_name="ISBN number of the book")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField(Contributor, through='BookContributor')
    def __str__(self):
        return "{} ({})".format(self.title, self.isbn)
class BookContributor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    class ContributionRoles(models.TextChoices):
        AUTHOR = 'Author', 'AUTHOR'
        CO_AUTHOR= 'CO_AUTHOR', 'Co-Author'
        EDITOR = 'Editor', 'EDITOR'
    role = models.CharField(verbose_name="The role this contributor had in the book",
                            choices=ContributionRoles.choices, max_length=20)

from django.contrib import auth
class Review(models.Model):
    content = models.TextField(help_text="The review content")
    rating= models.FloatField(help_text="The rating the reviewer has given")
    date_created= models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created")
    date_edited= models.DateTimeField(null=True, help_text="The date and time the review was last edited")
    creator=models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The book that the review is for")




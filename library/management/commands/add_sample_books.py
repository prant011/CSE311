from django.core.management.base import BaseCommand
from library.models import Author, Book


class Command(BaseCommand):
    help = 'Adds sample books and authors to the database'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample books and authors...')
        
        # Create authors
        authors_data = [
            {'name': 'J.K. Rowling', 'bio': 'British author, best known for the Harry Potter series'},
            {'name': 'George R.R. Martin', 'bio': 'American novelist and short story writer, creator of A Song of Ice and Fire'},
            {'name': 'Stephen King', 'bio': 'American author of horror, supernatural fiction, suspense, and fantasy novels'},
            {'name': 'Jane Austen', 'bio': 'English novelist known primarily for her six major novels'},
            {'name': 'Charles Dickens', 'bio': 'English writer and social critic, considered one of the greatest novelists'},
            {'name': 'Agatha Christie', 'bio': 'English writer known for her detective novels'},
            {'name': 'Ernest Hemingway', 'bio': 'American novelist, short-story writer, and journalist'},
            {'name': 'F. Scott Fitzgerald', 'bio': 'American novelist, essayist, and short story writer'},
            {'name': 'Mark Twain', 'bio': 'American writer, humorist, entrepreneur, publisher, and lecturer'},
            {'name': 'William Shakespeare', 'bio': 'English playwright, poet, and actor, widely regarded as the greatest writer'},
        ]
        
        authors = {}
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={'bio': author_data['bio']}
            )
            authors[author_data['name']] = author
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {author.name}'))
        
        # Create books
        books_data = [
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': '9780747532699',
                'publisher': 'Bloomsbury',
                'publication_year': 1997,
                'category': 'Fantasy',
                'description': 'The first book in the Harry Potter series, following the adventures of a young wizard.',
                'total_copies': 5,
                'available_copies': 5,
            },
            {
                'title': 'Harry Potter and the Chamber of Secrets',
                'author': 'J.K. Rowling',
                'isbn': '9780747538493',
                'publisher': 'Bloomsbury',
                'publication_year': 1998,
                'category': 'Fantasy',
                'description': 'The second book in the Harry Potter series.',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'A Game of Thrones',
                'author': 'George R.R. Martin',
                'isbn': '9780553103540',
                'publisher': 'Bantam Books',
                'publication_year': 1996,
                'category': 'Fantasy',
                'description': 'The first book in A Song of Ice and Fire series.',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'A Clash of Kings',
                'author': 'George R.R. Martin',
                'isbn': '9780553108033',
                'publisher': 'Bantam Books',
                'publication_year': 1998,
                'category': 'Fantasy',
                'description': 'The second book in A Song of Ice and Fire series.',
                'total_copies': 3,
                'available_copies': 2,
            },
            {
                'title': 'The Shining',
                'author': 'Stephen King',
                'isbn': '9780307743657',
                'publisher': 'Doubleday',
                'publication_year': 1977,
                'category': 'Horror',
                'description': 'A horror novel about a writer who becomes caretaker of a haunted hotel.',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'It',
                'author': 'Stephen King',
                'isbn': '9780670813025',
                'publisher': 'Viking Press',
                'publication_year': 1986,
                'category': 'Horror',
                'description': 'A horror novel about a group of children terrorized by an evil entity.',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'publisher': 'T. Egerton',
                'publication_year': 1813,
                'category': 'Romance',
                'description': 'A romantic novel of manners written by Jane Austen.',
                'total_copies': 6,
                'available_copies': 5,
            },
            {
                'title': 'Sense and Sensibility',
                'author': 'Jane Austen',
                'isbn': '9780141439662',
                'publisher': 'Thomas Egerton',
                'publication_year': 1811,
                'category': 'Romance',
                'description': 'A novel about two sisters with contrasting temperaments.',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'A Tale of Two Cities',
                'author': 'Charles Dickens',
                'isbn': '9780141439600',
                'publisher': 'Chapman & Hall',
                'publication_year': 1859,
                'category': 'Historical Fiction',
                'description': 'A historical novel set in London and Paris before and during the French Revolution.',
                'total_copies': 5,
                'available_copies': 4,
            },
            {
                'title': 'Great Expectations',
                'author': 'Charles Dickens',
                'isbn': '9780141439563',
                'publisher': 'Chapman & Hall',
                'publication_year': 1861,
                'category': 'Fiction',
                'description': 'A bildungsroman that depicts the personal growth and development of an orphan named Pip.',
                'total_copies': 4,
                'available_copies': 3,
            },
            {
                'title': 'Murder on the Orient Express',
                'author': 'Agatha Christie',
                'isbn': '9780062693662',
                'publisher': 'Collins Crime Club',
                'publication_year': 1934,
                'category': 'Mystery',
                'description': 'A detective novel featuring Hercule Poirot.',
                'total_copies': 5,
                'available_copies': 5,
            },
            {
                'title': 'The Murder of Roger Ackroyd',
                'author': 'Agatha Christie',
                'isbn': '9780062074028',
                'publisher': 'Collins Crime Club',
                'publication_year': 1926,
                'category': 'Mystery',
                'description': 'A detective novel featuring Hercule Poirot.',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'The Old Man and the Sea',
                'author': 'Ernest Hemingway',
                'isbn': '9780684801223',
                'publisher': 'Charles Scribner\'s Sons',
                'publication_year': 1952,
                'category': 'Fiction',
                'description': 'A short novel about an aging Cuban fisherman and his struggle with a giant marlin.',
                'total_copies': 6,
                'available_copies': 6,
            },
            {
                'title': 'For Whom the Bell Tolls',
                'author': 'Ernest Hemingway',
                'isbn': '9780684801469',
                'publisher': 'Charles Scribner\'s Sons',
                'publication_year': 1940,
                'category': 'Fiction',
                'description': 'A novel set during the Spanish Civil War.',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'publisher': 'Charles Scribner\'s Sons',
                'publication_year': 1925,
                'category': 'Fiction',
                'description': 'A novel about the American Dream set in the Jazz Age.',
                'total_copies': 5,
                'available_copies': 4,
            },
            {
                'title': 'Tender Is the Night',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780684801544',
                'publisher': 'Charles Scribner\'s Sons',
                'publication_year': 1934,
                'category': 'Fiction',
                'description': 'A novel about a young psychiatrist and his wife.',
                'total_copies': 3,
                'available_copies': 3,
            },
            {
                'title': 'The Adventures of Tom Sawyer',
                'author': 'Mark Twain',
                'isbn': '9780486400778',
                'publisher': 'American Publishing Company',
                'publication_year': 1876,
                'category': 'Fiction',
                'description': 'A novel about a young boy growing up along the Mississippi River.',
                'total_copies': 4,
                'available_copies': 4,
            },
            {
                'title': 'Adventures of Huckleberry Finn',
                'author': 'Mark Twain',
                'isbn': '9780486400779',
                'publisher': 'Chatto & Windus',
                'publication_year': 1884,
                'category': 'Fiction',
                'description': 'A novel about a boy and a runaway slave traveling down the Mississippi River.',
                'total_copies': 4,
                'available_copies': 3,
            },
            {
                'title': 'Hamlet',
                'author': 'William Shakespeare',
                'isbn': '9780486272788',
                'publisher': 'Various',
                'publication_year': 1603,
                'category': 'Drama',
                'description': 'A tragedy about the Prince of Denmark.',
                'total_copies': 6,
                'available_copies': 6,
            },
            {
                'title': 'Romeo and Juliet',
                'author': 'William Shakespeare',
                'isbn': '9780486275574',
                'publisher': 'Various',
                'publication_year': 1597,
                'category': 'Drama',
                'description': 'A tragedy about two young star-crossed lovers.',
                'total_copies': 5,
                'available_copies': 5,
            },
        ]
        
        created_count = 0
        for book_data in books_data:
            author_name = book_data.pop('author')
            author = authors[author_name]
            
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': author,
                    'publisher': book_data['publisher'],
                    'publication_year': book_data['publication_year'],
                    'category': book_data['category'],
                    'description': book_data['description'],
                    'total_copies': book_data['total_copies'],
                    'available_copies': book_data['available_copies'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {book.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully added {created_count} new books!'))
        self.stdout.write(f'Total books in database: {Book.objects.count()}')
        self.stdout.write(f'Total authors in database: {Author.objects.count()}')



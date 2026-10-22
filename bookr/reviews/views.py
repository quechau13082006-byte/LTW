from django.shortcuts import render, get_object_or_404,redirect
from .models import Book, Publisher, Contributor, Review
from django.contrib import messages
from django.utils import timezone
from .utils import average_rating
from .forms import PublisherForm, SearchForm, ReviewForm


def index(request):
    return render(request, "base.html")
def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,'book_rating': book_rating,'number_of_reviews':number_of_reviews})
    context = {'book_list': book_list}
    return render(request, 'reviews/book_list.html', context)
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.review_set.all()
    rating_list = [review.rating for review in reviews]
    if rating_list:
        book_rating = average_rating(rating_list)
    else:
        book_rating = None
    context = {'book': book, 'reviews': reviews, 'book_rating': book_rating}
    return render(request, 'reviews/book_detail.html', context)


def publisher_edit(request, pk=None):
    # 1. Xác định xem đây là Tạo mới hay Chỉnh sửa dựa vào tham số pk
    if pk is not None:
        # Nếu có pk (ví dụ: pk=1) -> Lấy đối tượng Publisher số 1 từ DB ra để sửa
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        # Nếu pk là None -> Đây là yêu cầu Tạo mới
        publisher = None
    # 2. Xử lý khi người dùng bấm nút Submit (gửi dữ liệu POST lên)
    if request.method == "POST":
        # Khởi tạo form với dữ liệu người dùng vừa gõ (request.POST)
        # và gắn vào đối tượng publisher (nếu là sửa thì ghi đè lên publisher cũ)
        form = PublisherForm(request.POST, instance=publisher)

        if form.is_valid():
            # Lưu đối tượng xuống Database
            updated_publisher = form.save()

            # Đăng ký thông báo thành công (Flash message)
            if publisher is None:
                messages.success(request, f'Publisher "{updated_publisher}" was created.')
            else:
                messages.success(request, f'Publisher "{updated_publisher}" was updated.')

            # Chuyển hướng (Redirect) về lại trang chỉnh sửa của chính Publisher này
            return redirect("publisher_edit", updated_publisher.pk)
    else:
        # 3. Xử lý khi người dùng mới chỉ mở trang web lên (method GET)
        form = PublisherForm(instance=publisher)
    # 4. Trả về giao diện template instance-form.html
    return render(request, "reviews/instance_form.html", {
        "form": form,
        "instance": publisher,
        "model_type": "Publisher"
    })
def book_search(request):
    search_text=""
    books= Book.objects.none()
    form = SearchForm(request.GET)
    if form.is_valid():
        search_text = form.cleaned_data.get("search") or ""
        search_in= form.cleaned_data.get ('search_in') or 'title'
        if search_text:
            if search_in=='title':
                books=Book.objects.filter(title__icontains=search_text)
            elif search_in=='contributor':
                contributors = Contributor.objects.filter(Q(first_names__icontains=search_text) | Q(last_names__icontains=search_text))

    context = { 'search_text': search_text, 'form':form, 'books': books}
    return render(request, 'reviews/search_results.html', context)


def review_edit(request, book_pk, review_pk=None):
    # [BƯỚC 1]: Luôn truy xuất cuốn sách trước dựa vào book_pk
    book = get_object_or_404(Book, pk=book_pk)

    # [BƯỚC 1]: Nếu có review_pk nghĩa là đang SỬA, nếu là None nghĩa là TẠO MỚI
    if review_pk is not None:
        # Đảm bảo bài review này phải thuộc đúng cuốn sách này (book_id=book.pk)
        review = get_object_or_404(Review, book_id=book.pk, pk=review_pk)
    else:
        review = None
    # [BƯỚC 2]: Xử lý khi người dùng gửi form lên (method POST)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            # DÒNG QUAN TRỌNG NHẤT: commit=False để chưa lưu vội vào Database
            updated_review = form.save(commit=False)

            # Gán thủ công cuốn sách cho bài Review
            updated_review.book = book

            # Nếu là sửa bài cũ (review khác None), cập nhật ngày giờ sửa đổi
            if review is not None:
                updated_review.date_edited = timezone.now()

            # Bây giờ mới chính thức lưu xuống Database
            updated_review.save()

            # [BƯỚC 3]: Đăng ký thông báo thành công và redirect về trang chi tiết sách
            messages.success(request, f'Review for "{book.title}" created.')
            return redirect("book_detail", book.pk)

    else:
        # [BƯỚC 4]: Xử lý khi người dùng mới mở trang (method GET)
        form = ReviewForm(instance=review)
    # [BƯỚC 5]: Xuất ra template instance-form.html với đầy đủ biến ngữ cảnh
    return render(request, "reviews/instance_form.html", {
        "form": form,
        "instance": review,
        "model_type": "Review",
        "related_instance": book,
        "related_model_type": "Book"
    })

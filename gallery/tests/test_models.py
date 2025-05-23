import pytest
from gallery.models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

@pytest.fixture
def category_factory(db):
    def create_category(name):
        return Category.objects.create(name=name)

    return create_category


@pytest.fixture
def image_file():
    return SimpleUploadedFile(
        name='test.jpg',
        content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00',
        content_type='image/jpeg'
    )


@pytest.fixture
def image_factory(db, image_file):
    def create_image(title, age_limit, categories=None):
        image = Image.objects.create(
            title=title,
            image=image_file,
            age_limit=age_limit
        )
        if categories:
            image.categories.add(*categories)
        return image

    return create_image

# Category
@pytest.mark.parametrize("name", ["Rock", "Bash", "Mozart"])
def test_category_creation(category_factory, name):
    category = category_factory(name)
    assert category.name == name
    assert Category.objects.filter(name=name).exists()

# Images
def test_image_creation(image_factory):
    image = image_factory("Test Image", 18)
    assert image.title == "Test Image"
    assert image.age_limit == 18
    assert image.created_date == date.today()


def test_image_with_categories(image_factory, category_factory):
    cat1 = category_factory("Rock")
    cat2 = category_factory("Bash")
    image = image_factory("With Categories", 16, [cat1, cat2])

    assert image.categories.count() == 2
    assert cat1 in image.categories.all()
    assert cat2 in image.categories.all()
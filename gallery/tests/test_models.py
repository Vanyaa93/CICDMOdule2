import pytest
from gallery.models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date


# -------- Фікстури --------

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


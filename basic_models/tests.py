from django.test import TestCase

from test_project.models import *


class BasicModelsTestCase(TestCase):


    def test_activequeryset_works(self):
        Category.objects.create(name='foo', is_active=True)
        Category.objects.create(name='bar', is_active=False)
        Category.objects.create(name='baz', is_active=True)

        self.assertEqual(Category.active_objects.all().count(), 2)

        # ensure that we can filter a queryset with .active()
        self.assertEqual(Category.objects.all().active().count(), 2)

        # ensure we can call the manager directly
        b_active = Category.objects.active().filter(name__istartswith='b')
        self.assertEqual(b_active.count(), 1)
        self.assertEqual(b_active[0].name, 'baz')


    def test_slugmodel(self):
        #ensure that a slug is created by default
        post = Post.objects.create(
            category=Category.objects.create(name='foobar'),
            name="Hello world",
            body="hey hey hey",
        )
        self.assertEqual(post.slug, "hello-world")

        #ensure natural_key is working
        self.assertEqual(post.natural_key(), ["hello-world"])
        self.assertEqual(Post.objects.get_by_natural_key("hello-world"), post)


    def test_onlyoneactive_model(self):
        cat = Category.objects.create(name='foobar')
        for foo in ["foo","bar","baz"]:
            Post.objects.create(
                category=cat,
                name=foo,
                body=foo,
            )

        hero = "<h1>hey everybody</h1>"
        home = Homepage.objects.create(
            hero=hero,
            is_active = True
        )
        home.posts = Post.objects.all()

        # home = Homepage.objects.active_one()

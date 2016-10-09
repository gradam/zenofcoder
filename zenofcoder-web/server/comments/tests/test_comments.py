# encoding: utf-8
import pytest
from articles.tests.test_articles import BaseTestClass
from articles.models import Article
from comments.models import Comment


CONTENT = """
This is sample comment content.
And here is next line.
"""


class TestComments(BaseTestClass):
    @pytest.fixture
    def comment(self, user, base_article: Article) -> Comment:
        return self.create_comment(user, base_article)

    @staticmethod
    def create_comment(user, base_article: Article, model_type='article', **kwargs) -> Comment:
        comment = Comment.objects.create_by_model_type(model_type=model_type, slug=base_article.slug,
                                                       content=CONTENT, user=user, **kwargs)
        return comment

    def test_str_representation(self, comment):
        assert str(comment) == CONTENT

    def test_comment_to_article(self, user, base_article: Article):
        comment = self.create_comment(user, base_article)
        assert [comment] == base_article.comments

    def test_comment_with_parent(self, user, base_article: Article):
        comment_parent = self.create_comment(user, base_article)
        comment_child = self.create_comment(user, base_article, parent=comment_parent)
        assert list(Comment.objects.filter(parent=comment_parent)) == [comment_child]
        assert comment_child.parent == comment_parent

    def test_top_level(self, user, base_article: Article):
        comment_parent_0 = self.create_comment(user, base_article)
        comment_parent_1 = self.create_comment(user, base_article)
        comment_parent_2 = self.create_comment(user, base_article, parent=comment_parent_1)
        comment_child_1 = self.create_comment(user, base_article, parent=comment_parent_2)
        comment_child_2 = self.create_comment(user, base_article, parent=comment_parent_2)

        assert list(Comment.objects.filter_top_lever()) == [comment_parent_1, comment_parent_0]

    def test_is_parent(self, user, base_article: Article):
        comment_parent = self.create_comment(user, base_article)
        comment_child = self.create_comment(user, base_article, parent=comment_parent)
        assert comment_parent.is_parent
        assert not comment_child.is_parent

    def test_create_for_nonexistent_model(self, user, base_article: Article):
        comment = self.create_comment(user, base_article, model_type='non_existing_one')
        assert comment is None

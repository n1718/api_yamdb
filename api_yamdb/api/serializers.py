from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('title',)

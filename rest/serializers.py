from rest_framework import serializers
from .models import Article, ArticleImage
# from cloudinary.serializers import CloudinaryJsFileField  

# class ArticleSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=50)
#     author = serializers.CharField(max_length=100)
#     email = serializers.EmailField()
#     date = serializers.DateTimeField()


#     def create(self, validated_data):
#         return Article(validated_data)


#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.author = validated_data.get('author', instance.author)
#         instance.email = validated_data.get('email', instance.email)
#         instance.date = validated_data.get('date', instance.date)

#         instance.save()
#         return instance
# class FileSerializer(serializers.Serializer):
    # file= serializers.FileField(max_length=None, allow_empty_file=False)
class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # fields = ['id', 'title', 'author', 'email', 'date']
        fields = '__all__'
        # image = CloudinaryFileField()
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser, MultiPartParser
from .models import Article, ArticleImage
from .serializers import ArticleSerializer, ArticleImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import cloudinary.uploader


# Create your views here.
@api_view([ 'POST'])
def upload(request):
    # if request.method == 'GET':
    #     articles = ArticleImage.objects.all()
    #     serializer = ArticleImageSerializer(articles, many=True)
    #     return Response(serializer.data)


    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.FILES)
        upload_data = cloudinary.uploader.upload(serializer)


        if upload_data.is_valid():
            upload_data.save()
            return Response(serializer.FILE, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class ArticleImageViewSet(viewsets.ModelViewSet):
#     serializer_class = ArticleImageSerializer
#     queryset = ArticleImage.objects.all()
    
#     upload_data = cloudinary.uploader.upload(request.FILES['file'])

class ArticleImageView(APIView):
    parser_classes = (MultiPartParser, JSONParser,)

    @staticmethod
    def post(request):
        file = request.data.get('picture')
        upload_data = cloudinary.uploader.upload(file)

        return Response({
            'status': 'success',
            'data':upload_data,
        }, status=201)

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


# class FileUploadViewSet(viewsets.Viewset):
#     def create(self, request):
#         serializer_class = FileSerializer(data=request.data)
#         if 'file' not in request.FILES or not serializer_class.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         else:
#             handle_uploaded_file(request.FILES['file'])
#             return Response(status=status.HTTP_201_CREATED)


#     def handle_uploaded_file(f):
#         with open(f.name, 'wb+') as destination:
#             for chunk in f.chunks():
#                 destination.write(chunk)

# Generic viewset
# class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
#     serializer_class= ArticleSerializer
#     queryset = Article.objects.all()
#     lookup_field = 'pk'


#using viewsets that will be registered using routers and provide actions instead of method handlers like get and post
# class ArticleViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Article.objects.all()
#         serializer = ArticleSerializer(queryset, many=True)
#         return Response(serializer.data)


#     def create(self, request):
#         serializer = ArticleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def retrieve(self, request, pk=None):
#         queryset = Article.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


#     def update(self, request, pk):
#         article = Article.objects.get(pk=pk)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def delete(self, request, pk):
#         article=Article.objects.get(pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# using generics and mixins
class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'
    
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        content = {

            'user': str(request.user), # `django.contrib.auth.user` instance
            'auth': str(request.auth), # None
        }

        return Response(content)


    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        return self.list(request)


    def post(self, request):
        return self.create(request)


    def put(self, request, pk=None):
        return self.update(request, pk)


    def delete(self, request, pk):
        return self.destroy(request, id)


    # def delete(self, request, id=None):
    #     return seld.des

# Using the APIView
class ArticleAPIView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    
    def get_object(self, pk):
        article = get_object_or_404(Article, pk=pk)
        return article
       
       
    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# decorator from clients with no CSRF Token
# @csrf_exempt
# def article_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return JsonResponse(serializer.data , safe=False)


#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


'''
using the api_view() decorator that returns response instead of HttpResponse or JsonResponse and provides request to the function_based view it wraps
'''
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# # provides individual details of retrieved object by id(primary key) 
# def article_detail(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(article, data=data, partial=True)
#         # serializer arguments include
#         # instance of the Article model we want to update
#         # data received from the request
#         # (optional)partial = True to indicate it may contain all fields of model
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)


#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status = 204)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)


    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
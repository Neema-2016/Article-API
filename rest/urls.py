from django.urls import path, include
from .views import article_list, article_detail, upload, ArticleAPIView, ArticleDetailView, GenericAPIView, ArticleViewSet, ArticleImageView
from rest_framework import routers
from rest_framework.routers import DefaultRouter
# from django.conf import settings
# from django.conf.urls.static import static

router = DefaultRouter()
# router.register(r'file', FileUploadViewSet, basename='file')
router.register(r'articles', ArticleViewSet, basename='article')
# router.register(r'images', ArticleImageViewSet, basename='image')
# urlpatterns = router.urls
# router.register(r'article', ArticleViewSet, basename='Article')
# this or the router.urls iincluded in the pth list within the url patterns urlpatterns = router.urls

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('upload-image', ArticleImageView.as_view()),
    path('upload-img', upload),
    path('viewset/<int:pk>/', include(router.urls)),
    # path('list/', article_list, name='list'),
    # path('detail/<int:pk>/', article_detail, name='detail'),
    path('list/', ArticleAPIView.as_view()),
    path('generic/<int:pk>/', GenericAPIView.as_view()),
    path('detail/<int:pk>/', ArticleDetailView.as_view()),
    path('upload/', include(router.urls))
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from .models import Post
from rest_framework.views import APIView
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import User

from rest_framework.generics import (
    ListAPIView,
)

from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

class PostView(APIView):
    
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'home.html'


    def get(self, request):
        """
        A method that returns a templated HTML representation of a given Posts.
        """
        try:
            posts = Post.objects.all()

            serializer = PostSerializer(posts, many = True)

            print(f"\nposts: {', '.join(map(str, [post.id for post in posts]))}", end='\n\n')

            return Response({
                'data': serializer.data,
                # 'object_list': posts,
                'message': 'posts fetched succesfully',
            }, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)
    

    def post(self, request):
        try:
            data = request.data
            serializer = PostSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()        

            return Response({
                'data': serializer.data,
                'message': 'post created succesfully',
            }, status = status.HTTP_201_CREATED)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
   


class PostDetailView(APIView):

    def get(self, request, pk):
        """
        A method that returns a templated HTML representation of a given a Post.
        """
        try:
            post = Post.objects.get(id = pk)

            serializer = PostSerializer(post)

            print(f'post likes from detail view: {post.likes}')
            print(f'post likes time: {post.likes.all()}')

            return Response({
                'data': serializer.data,
                'likes': post.likes.all(),
                'message': 'posts fetched succesfully',
            }, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)



class PostDeleteView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, pk):
        try:
            data = request.data 

            post = Post.objects.get(id = pk)
            serializer = PostSerializer(data = data)

            if not post:
                return Response({
                    'data': {},
                    'message': 'invalid post id'
                }, status = status.HTTP_400_BAD_REQUEST)

            print(f'post author id: {post.author.username}')
            print(f'author id: {data["username"]}')
            print(data['username'] != post.author.username)

            if data['username'] != post.author.username:
                return Response({
                    'data': {},
                    'message': 'you are not authorized to this'
                }, status = status.HTTP_400_BAD_REQUEST)

            post.delete()

            posts = Post.objects.all()
            serializer = PostSerializer(posts, many = True)

            return Response({
                'data': serializer.data,
                # 'object_list': posts,
                'message': 'post deleted succesfully',
                # 'template_name': 'home.html'
            }, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)


class PostLikesView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            data = request.data

            post = Post.objects.get(id = pk)
            post.likes.add(data['id'])

            post.save()

            return Response({
                'data': {},
                'message': 'post liked succesfully',
            }, status = status.HTTP_201_CREATED)


        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            data = request.data

            post = Post.objects.get(id = pk)
            post.likes.remove(data['id'])

            post.save()

            return Response({
                'data': {},
                'message': 'post unliked succesfully',
            }, status = status.HTTP_201_CREATED)


        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
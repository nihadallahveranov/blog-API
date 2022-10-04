from sys import api_version
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.models import User
from post.models import Post
from rest_framework.permissions import IsAdminUser

class RegisterView(APIView):

    def post(self, request):
        try: 
            data = request.data

            serializer = RegisterSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': {},
                'message': 'your account is created', 
            }, status = status.HTTP_201_CREATED)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST)

class UserView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authors.html'


    def get(self, request):
        """
        A method that returns a templated HTML representation of a given Users.
        """
        try:
            users = User.objects.all()

            print(f"\nusers: {', '.join(map(str, [user.id for user in users]))}", end='\n\n')

            serializer = UserSerializer(users, many = True)

            return Response({
                'data': serializer.data,
                'object_list': users,
                'message': 'users fetched succesfully',
            }, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'author_details.html'

    def get(self, request, pk):
        """
        A method that returns a templated HTML representation of a given a Post.
        """
        try:

            posts = [post for post in Post.objects.all() if post.author.id == pk]

            user = User.objects.get(id = pk)

            serializer = UserSerializer(user)

            return Response({
                'data': serializer.data,
                'posts': posts,
                'user': user,
                'message': 'posts fetched succesfully'
            }, status = status.HTTP_200_OK)

        except Exception as err:
            print(f'error: {err}')

            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)

class DeleteAccount(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = User.objects.get(id = pk)
        user.delete()

        return Response({"message": "user deleted succesfully"})

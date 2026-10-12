from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User,Profile,Post,Like,Favorite
from .serializers import UserSerializer,ProfileSerializer,PostSerializer,LikeSerializer,FavoriteSerializer
from django.db.models import Q,Count,Sum,Avg,Min,Max

@api_view(['GET','POST'])
def user_list(request):
    if request.method=='GET':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

@api_view(['GET','PUT','DELETE'])
def user_detail(request,pk):
    user = get_object_or_404(User,pk=pk)
    if request.method=='GET':
        serializer = UserSerializer(user)
        return Response(serializer.data,status=200)
    elif request.method=='PUT':
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    elif request.method=='DELETE':
        user.delete()
        return Response(status=204)

@api_view(['GET','POST'])
def profile_list(request):
    if request.method=='GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        user = get_object_or_404(User,pk=request.data.get('user'))
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=user)
            return Response(ProfileSerializer(profile).data,status=201)
        return Response(serializer.errors,status=400)

@api_view(['GET','PUT','DELETE'])
def profile_detail(request,pk):
    profile = get_object_or_404(Profile,pk=pk)
    if request.method=='GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data,status=200)
    elif request.method=='PUT':
        user_id = request.data.get('user',profile.user_id)
        user = get_object_or_404(User,pk=user_id)
        serializer = ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            profile = serializer.save(user=user)
            return Response(ProfileSerializer(profile).data,status=200)
        return Response(serializer.errors,status=400)
    elif request.method=='DELETE':
        profile.delete()
        return Response(status=204)

@api_view(['GET'])
def profile_city_statistics(request):
    statistics = Profile.objects.values('city').annotate(users_count=Count('id')).order_by('city')
    return Response(statistics,status=200)


@api_view(['GET','POST'])
def post_list(request):
    if request.method=='GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data,status=200)
    elif request.method=='POST':
        user = get_object_or_404(User,pk=request.data.get('user'))
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=user)
            return Response(PostSerializer(post).data,status=201)
        return Response(serializer.errors,status=400)

@api_view(['GET','PUT','DELETE'])
def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method=='GET':
        serializer = PostSerializer(post)
        return Response(serializer.data,status=200)
    elif request.method=='PUT':
        user_id = request.data.get('user',post.user_id)
        user = get_object_or_404(User,pk=user_id)
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=user)
            return Response(PostSerializer(post).data,status=200)
        return Response(serializer.errors,status=400)
    elif request.method=='DELETE':
        post.delete()
        return Response(status=204)
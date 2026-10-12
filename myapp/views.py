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
    if request.method == 'GET':
        liked_by = [
            {'id': like.user.id, 'username': like.user.username}
            for like in post.like_set.select_related('user').all()
        ]
        favorited_by = [
            {'id': favorite.user.id, 'username': favorite.user.username}
            for favorite in post.favorite_set.select_related('user').all()
        ]
        data = {
            'id': post.id,
            'title': post.title,
            'author': {
                'id': post.user.id,
                'username': post.user.username,
            },
            'views': post.views,
            'likes_count': len(liked_by),
            'favorites_count': len(favorited_by),
            'liked_by': liked_by,
            'favorited_by': favorited_by,
            'is_popular': len(liked_by) >= 10,
        }
        return Response(data, status=200)
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

@api_view(['GET'])
def user_statistics_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.filter(user=user).first()
    posts = Post.objects.filter(user=user)
    data = {
        'id': user.id,
        'username': user.username,
        'full_name': f'{user.first_name} {user.last_name}',
        'age': user.age,
        'profile': {
            'bio': profile.bio if profile else None,
            'city': profile.city if profile else None,
        },
        'stats': {
            'posts_count': posts.count(),
            'total_views': posts.aggregate(total=Sum('views'))['total'] or 0,
            'likes_received': Like.objects.filter(post__user=user).count(),
            'favorites_received': Favorite.objects.filter(post__user=user).count(),
        }
    }
    return Response(data, status=200)
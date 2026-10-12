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
            return Response(serializer.data,status=200)
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
            'content': post.content,
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
            'created_at': post.created_at,
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


@api_view(['GET'])
def user_statistics(request):
    statistics = User.objects.aggregate(total_users=Count('id'),average_age=Avg('age'),min_age=Min('age'),max_age=Max('age'),)
    return Response(statistics, status=200)


@api_view(['GET'])
def most_active_users(request):
    users = User.objects.annotate(posts_count=Count('post')).order_by('-posts_count')[:10]
    data = [
        {
        'id': user.id,
        'username': user.username,
        'full_name': f'{user.first_name} {user.last_name}',
        'posts_count': user.posts_count,}for user in users]
    return Response(data, status=200)

@api_view(['GET'])
def user_posts(request,pk):
    user = get_object_or_404(User,pk=pk)
    posts = Post.objects.filter(user=user)
    data = {
        'user': {
            'id': user.id,
            'username': user.username,
        },
        'posts_count': posts.count(),
        'results': [
            {
                'id': post.id,
                'title': post.title,
                'likes_count': post.like_set.count(),
                'views': post.views,
            }
            for post in posts
        ],
    }
    return Response(data, status=200)

@api_view(['GET'])
def popular_posts(request):
    posts = Post.objects.annotate(likes_count=Count('like')).filter(likes_count__gte=10).order_by('-likes_count')
    data = [
        {
            'id': post.id,
            'title': post.title,
            'likes_count': post.likes_count,
            'favorites_count': post.favorite_set.count(),
            'is_popular': post.likes_count >= 10,
        }
        for post in posts
    ]
    return Response(data, status=200)

@api_view(['GET'])
def search_posts(request):
    query = request.query_params.get('q', '')
    posts = Post.objects.filter(Q(title__icontains=query) |Q(content__icontains=query))
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def filter_posts(request):
    posts = Post.objects.all()
    min_views = request.query_params.get('min_views')
    max_views = request.query_params.get('max_views')
    user_id = request.query_params.get('user_id')
    if min_views is not None:
        posts = posts.filter(views__gte=min_views)
    if max_views is not None:
        posts = posts.filter(views__lte=max_views)
    if user_id is not None:
        posts = posts.filter(user_id=user_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def post_statistics(request):
    statistics = Post.objects.aggregate(
        total_posts=Count('id'),
        total_views=Sum('views'),
        average_views=Avg('views'),
        max_views=Max('views'),
        min_views=Min('views'),
        )
    statistics['total_likes'] = Like.objects.count()
    statistics['total_favorites'] = Favorite.objects.count()
    return Response(statistics, status=200)

@api_view(['GET'])
def author_statistics(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'error': 'user_id is required'},status=400)
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(user=user)
    data = {
        'user_id': user.id,
        'username': user.username,
        'posts_count': posts.count(),
        'total_views': posts.aggregate(
            total=Sum('views')
        )['total'] or 0,
        'average_views': posts.aggregate(
            average=Avg('views')
        )['average'] or 0,
        'likes_received': Like.objects.filter(
            post__user=user
        ).count(),
    }
    return Response(data, status=200)

@api_view(['GET', 'POST'])
def like_list(request):
    if request.method == 'GET':
        likes = Like.objects.select_related('user', 'post').all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)
    user = get_object_or_404(User, pk=request.data.get('user'))
    post = get_object_or_404(Post, pk=request.data.get('post'))
    if Like.objects.filter(user=user, post=post).exists():
        return Response({'error': 'You have already liked this post'},status=400)
    like = Like.objects.create(user=user, post=post)
    return Response(LikeSerializer(like).data, status=201)

@api_view(['DELETE'])
def like_delete(request, pk):
    like = get_object_or_404(Like, pk=pk)
    like.delete()
    return Response(status=204)

@api_view(['GET'])
def post_likes(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes = Like.objects.filter(post=post).select_related('user')
    data = {
        'post_id': post.id,
        'likes_count': likes.count(),
        'users': [
            {
                'id': like.user.id,
                'username': like.user.username,
            }
            for like in likes
        ],
    }
    return Response(data, status=200)
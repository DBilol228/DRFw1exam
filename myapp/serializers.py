from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','full_name','age','posts_count','likes_count','favorites_count']
        read_only_fields = ['id','full_name','posts_count','likes_count','favorites_count']
    def get_full_name(self,obj):
        return f'{obj.first_name} {obj.last_name}'
    def get_posts_count(self, obj):
        return obj.post_set.count()
    def get_likes_count(self, obj):
        return obj.like_set.count()
    def get_favorites_count(self, obj):
        return obj.favorite_set.count()

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['id','user','bio','city','birth_date','avatar','posts_count']
        read_only_fields = ['id','user','posts_count']
    def get_user(self,obj):
        info = {'id':obj.user.id,'username':obj.user.username,'full_name':f'{obj.user.first_name} {obj.user.last_name}'}
        return info
    def get_posts_count(self,obj):
        return obj.user.post_set.count()

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    is_popular = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','content','author','views','likes_count','favorites_count','is_popular','created_at']
        read_only_fields = ['id','author','likes_count','favorites_count','is_popular','created_at']
    def get_author(self,obj):
        author = {'id':obj.user.id,'username':obj.user.username,'full_name':f'{obj.user.first_name} {obj.user.last_name}'}
        return author
    def get_is_popular(self,obj):
        return obj.like_set.count() >= 10
    def get_likes_count(self,obj):
        return obj.like_set.count()
    def get_favorites_count(self,obj):
        return obj.favorite_set.count()

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['id','user','post','created_at']
        read_only_fields = ['id','user','post','created_at']
    def get_user(self,obj):
        user = {'id':obj.user.id,'username':obj.user.username}
        return user
    def get_post(self,obj):
        post = {'id':obj.post.id,'title':obj.post.title}
        return post

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    class Meta:
        model = Favorite
        fields = ['id','user','post','created_at']
        read_only_fields = ['id','user','post','created_at']
    def get_user(self, obj):
        user = {'id': obj.user.id,'username': obj.user.username}
        return user
    def get_post(self, obj):
        post = {'id': obj.post.id,'title': obj.post.title,'author':obj.post.user.username,'likes_count':obj.post.like_set.count()}
        return post
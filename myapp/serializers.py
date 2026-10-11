from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    favorites_count = serializers.IntegerField(read_only=True)
    is_popular = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','title','content','author','views','likes_count','favorites_count','is_popular','created_at',]
    def get_author(self,obj):
        author = {'id':obj.user.id,'username':obj.user.username,'full_name':f'{obj.user.first_name} {obj.user.last_name}'}
        return author
    def get_is_popular(self,obj):
        return obj.likes_count >= 10

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    class Meta:
        model = Like
        fields = ['id','user','post','created_at']
    def get_user(self,obj):
        user = {'id':obj.user.id,'username':obj.user.username}
        return user
    def get_post(self,obj):
        post = {'id':obj.post.id,'title':obj.post.title}
        return post

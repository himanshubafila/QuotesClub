from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50 , default=" ")
    subject = models.CharField(max_length=50, default=" ")
    message = models.CharField(max_length=500 , default=" ")



    def __str__(self):
        return self.name


class Post(models.Model):
    sno = models.AutoField(primary_key = True)
    image = models.ImageField(upload_to="read/img" , default = " ")
    caption = models.CharField(max_length=10000 , default = " ")
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    time = models.DateTimeField(default=now)


    def __str__(self):
        return self.caption[:15] + ".......... "


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , default=" ")
    bio = models.TextField(max_length=500 , default= " ")
    gender = models.CharField(max_length=10 , default=" ")
    phone = models.CharField(max_length=10 , default= " ")
    profile_picture = models.ImageField(upload_to='read/img' , default="read/img/df.jpg")
    privacy = models.BooleanField(default=False)




    def __str__(self):
        return self.user.username


class HashTag(models.Model):
    tag_name = models.CharField(max_length=20 , default=" ")
    tag_posts = models.ManyToManyField(Post , related_name= "posts" , blank=True)
    post_count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User , related_name="follower_user" , blank=True)
    followers_count = models.IntegerField(default=0)

    @classmethod

    def addPost(cls , tag , post):
        obj , create = cls.objects.get_or_create(tag_name = tag)
        obj.tag_posts.add(post)

    @classmethod

    def addFollowers(cls , tag , user):
        obj,create = cls.objects.get_or_create(tag_name = tag)
        obj.followers.add(user)

    @classmethod
    def rmvFollowers(cls, tag, user):
        obj, create = cls.objects.get_or_create(tag_name=tag)
        obj.followers.remove(user)

    def __str__(self):
        return self.tag_name


class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    comments = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE , null=True)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.comments[:10] + "............." + self.user.username


class Follower(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    follower = models.ManyToManyField(User , related_name= "followers_user" , blank=True)
    follow_count = models.IntegerField(default=0)

    @classmethod

    def follow(cls, user , follower_user):
        obj , create = cls.objects.get_or_create(user = user)
        obj.follower.add(follower_user)

    @classmethod
    def unfollow(cls, user , unfollower_user):
        obj , create = cls.objects.get_or_create(user = user)
        obj.follower.remove(unfollower_user)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    following = models.ManyToManyField(User, related_name="following_user" , blank=True)
    following_tag = models.ManyToManyField(HashTag , related_name="Hash_name" , blank=True)
    following_count = models.IntegerField(default=0)

    @classmethod
    def unfollowing(cls, user, unfollowing_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.following.remove(unfollowing_user)

    @classmethod
    def follow(cls, user, following_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.following.add(following_user)

    @classmethod
    def followingTag(cls , user , tag):
        obj , create = cls.objects.get_or_create(user = user)
        obj.following_tag.add(tag)

    @classmethod
    def unfollowingTag(cls , user , tag):
        obj , create = cls.objects.get_or_create(user = user)
        obj.following_tag.remove(tag)


    def __str__(self):
        return self.user.username


class Notifications(models.Model):
    sno = models.AutoField(primary_key = True)
    My_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='Me')
    NOTI_CHOICES = (
        ('F', 'Follow'),
        ('L', 'Like'),
        ('C' , 'Comment'),
        ('S' , 'Save'),
    )
    purpose = models.CharField(max_length=1, choices=NOTI_CHOICES)
    post = models.ForeignKey(Post , on_delete=models.CASCADE , blank=True , null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank=True)
    view = models.BooleanField(default=False)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return self.purpose+ ".... For....." + self.My_user.username


class MyNotifacions(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    notifications = models.ManyToManyField(Notifications , related_name='Notify' , blank=True)
    noti_count = models.IntegerField(default=0)

    @classmethod
    def AddNotification(cls , user, notify):
        obj , create = cls.objects.get_or_create(user = user)
        obj.notifications.add(notify)

    def __str__(self):
        return self.user.username


class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    liker = models.ManyToManyField(User , related_name= "like_user" , blank=True)
    like_count = models.IntegerField(default=0)

    @classmethod

    def like(cls, post , liker_user):
        obj , create = cls.objects.get_or_create(post = post)
        obj.liker.add(liker_user)

    @classmethod
    def unlike(cls, post , unliker_user):
        obj , create = cls.objects.get_or_create(post = post)
        obj.liker.remove(unliker_user)

    def __str__(self):
        return self.post.caption + "-------"


class MyLike(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likedPost = models.ManyToManyField(Post , related_name= "like_post" , blank=True)
    likedQuotes = models.ManyToManyField
    post_count = models.IntegerField(default=0)

    @classmethod

    def like(cls, user , like_post):
        obj , create = cls.objects.get_or_create(user = user)
        obj.likedPost.add(like_post)

    @classmethod
    def unlike(cls, user , unlike_post):
        obj , create = cls.objects.get_or_create(user = user)
        obj.likedPost.remove(unlike_post)

    def __str__(self):
        return self.user.username


class SavePost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    saver = models.ManyToManyField(User , related_name= "save_user" , blank=True)
    save_count = models.IntegerField(default=0)

    @classmethod

    def savepost(cls, post , saver_user):
        obj , create = cls.objects.get_or_create(post = post)
        obj.saver.add(saver_user)

    @classmethod
    def unsavepost(cls, post , unsaver_user):
        obj , create = cls.objects.get_or_create(post = post)
        obj.saver.remove(unsaver_user)

    def __str__(self):
        return self.post.caption


class MySave(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    savedPost = models.ManyToManyField(Post , related_name= "save_post" , blank=True)
    post_count = models.IntegerField(default=0)

    @classmethod

    def savepost(cls, user , save_post):
        obj , create = cls.objects.get_or_create(user = user)
        obj.savedPost.add(save_post)

    @classmethod
    def unsavepost(cls, user , unsave_post):
        obj , create = cls.objects.get_or_create(user = user)
        obj.savedPost.remove(unsave_post)

    def __str__(self):
        return self.user.username


class Blocking(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    blockedBy = models.ManyToManyField(User , related_name= "blocked_by" , blank=True )
    blocked_count = models.IntegerField(default=0)

    @classmethod
    def blocked(cls , user , blocked_by):
        obj , create = cls.objects.get_or_create(user = user)
        obj.blockedBy.add(blocked_by)

    @classmethod
    def unblocked(cls , user , unblocked_by):
        obj , create = cls.objects.get_or_create(user = user)
        obj.blockedBy.remove(unblocked_by)


class MyBlocking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blockedUser = models.ManyToManyField(User, related_name="blocked_user", blank=True)
    blocked_count = models.IntegerField(default=0)

    @classmethod
    def blocked(cls, user, blocked_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.blockedUser.add(blocked_user)

    @classmethod
    def unblocked(cls, user, unblocked_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.blockedUser.remove(unblocked_user)
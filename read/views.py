from django.shortcuts import render , redirect , HttpResponse
from .models import  Contact , Profile , User , Post ,Follower , Following , Like , MyLike ,SavePost , MySave , HashTag , Blocking , MyBlocking , Comment , Notifications ,MyNotifacions
from django.contrib import messages
from django.contrib.auth import logout
import wikiquotes , json ,random , csv


def index(request):
    return render(request , 'error.html' )



def search(request):
    try:
        s = request.GET.get('se')
        select = request.GET.get('select')
        try:
            mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
            pending = 0
            for i in mynoti.notifications.all():
                if i.view == False:
                    pending = pending + 1

            mynoti_list = [i for i in mynoti.notifications.all()]

        except:
            pending = 0
            mynoti_list = []

        if select == 'Quotes':
            f = open(r'C:\Users\Mr.Mg\Documents\Python\Projects\quotesbook1/Data\quotes.csv', encoding="utf8")
            csv_f = csv.reader(f)
            ans = []
            i = 0
            ran = 500
            for row in csv_f:
                if s.lower() in row[2]:
                    if len(row[0]) < 300:
                        ans.append([row[0] , row[1] , row[2] , len(row[0])])
                if i == ran:
                    if len(ans) <20:
                        ran = ran*10

                    else:
                        break
                i += 1
            return render(request, 'photo_search_quotes.html' , {'post' : ans , 's' : s , 'length' : len(ans) , 'pending' : pending , 'notification' : mynoti_list[::-1]})


        try:
            if select == 'User':
                s = s.lower()
                user = User.objects.filter(username=s)
                myFollowing = Following.objects.get_or_create(user = request.user)[0].following.all()
                l  = list(user)
                s = s.capitalize()
                l = l + list(User.objects.filter(last_name = s)) + list(User.objects.filter(first_name = s))


                if request.user in l:
                    l.remove(request.user)

                user = []
                for i in l:
                    followed = "Follow"
                    user_follower = [i for i in Follower.objects.get_or_create(user = i)[0].follower.all()]
                    user_following = [i for i in Following.objects.get_or_create(user = i)[0].following.all()]
                    user_follower_count = len(user_follower)
                    user_following_count = len(user_following)
                    if i in myFollowing:
                        followed = "Unfollow"

                    if user_follower_count > 10:
                        user_follower = user_follower[:9]

                    if user_following_count > 10:
                        user_following = user_following[:9]

                    user.append([i , followed , user_follower_count , user_follower , user_following_count, user_following])

        except:
            user = []

        return render(request, 'photo_search.html', {'users': user , 'length' : len(user) , 'search' : s , 'pending' : pending , 'notification' : mynoti_list[::-1]})


        if select == 'Movies':
            quotes = []
            for i in wikiquotes.search(s, "english"):
                for j in wikiquotes.get_quotes(i, "english"):
                    if len(j) > 50:
                        quotes.append([j, i])

            return render(request, 'search.html', {'q': quotes})


        if select == 'Hashtag':
            s = s.lower()
            if s[0] == "#":
                s = s[1:]
            hash_list = []
            myFollowing = Following.objects.get_or_create(user = request.user)[0].following_tag.all()
            tags = [i for i in HashTag.objects.all()]
            for i in tags:
                followed = "Follow"
                if s in str(i):
                    follower = [j for j in i.followers.all()]
                    follower_c = len(follower)

                    if follower_c > 10:
                        follower = follower[:9]

                    if i in myFollowing:
                        followed = "Unfollow"

                    hash_list.append([i , followed , follower_c , follower])

            return render(request , 'photo_search_tag.html' , {'users' : hash_list , 'length' : len(hash_list) , 'search' : s[1:] , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request , 'error.html')




def searchPage(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]
        return render(request , 'photo_search.html' , {'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def profile(request):
    try:
        follow = Follower.objects.get_or_create(user=request.user)
        following = Following.objects.get_or_create(user=request.user)
        following_list = following[0].following.all()
        following[0].following_count = len(following_list)
        f1_len = len(following_list)
        following[0].save()
        follow[0].follow_count = len(follow[0].follower.all())
        f_len = len(follow[0].follower.all())
        follow[0].save()
        u = User.objects.get(username= request.user)
        likes = MyLike.objects.get_or_create(user=request.user)
        saves = MySave.objects.get_or_create(user = request.user)
        saves[0].post_count = len(saves[0].savedPost.all())
        saved_Post = saves[0].post_count
        saves[0].save()
        likes[0].post_count = len(likes[0].likedPost.all())
        liked_post = likes[0].post_count
        likes[0].save()
        user = User.objects.exclude(username = request.user)
        p = []
        user_list = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        post = Post.objects.filter(user=request.user)
        for i in post:
            liked = False
            saved = False
            l = Like.objects.get_or_create(post = i)
            like_c = l[0].like_count
            s = SavePost.objects.get_or_create(post = i)
            save_c = s[0].save_count
            if i in likes[0].likedPost.all():
                liked = True

            if i in saves[0].savedPost.all():
                saved = True

            p.append([i, liked , like_c , saved , save_c ])


        count = 0
        lp = []
        for i in p:
            if count%2 == 0:
                lp.append([])
                cd = count//2
                lp[cd].append(i)
            else:
                cd = count//2
                lp[cd].append(i)

            count +=1

        for i in user:
            if i in following_list:
                pass
            else:
                user_list.append(i)

        return render(request, 'photo_profile_two.html', {'myuser': u, 'post': lp, 'l': len(p) , 'followers' : f_len, 'following' : f1_len , 'user_list' : user_list  , 'user_c' : len(user_list) , 'savedPost' : saved_Post , 'likedPost' : liked_post , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def quotes(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

    except:
        mynoti_list = []
        pending = 0
    return render(request , 'photo_quotes.html' , { 'pending' : pending , 'notification' : mynoti_list[::-1]})



def shayari(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

    except:
        mynoti_list = []
        pending = 0
    return render(request , 'photo_shayari.html' ,{ 'pending' : pending , 'notification' : mynoti_list[::-1]})



def shayarisearch(request):
    try:
        f = open(r'C:\Users\Mr.Mg\Documents\Python\Projects\quotesbook1\Data\Book.csv', encoding="utf8")
        s = request.GET.get('se')
        print(s.lower())
        csv_f = csv.reader(f)
        ans = []
        i = 0
        ran = 500

        for row in csv_f:
            print(row[0], s.lower())
            if s.lower() in row[0].lower():
                ans.append([row[1], row[0], row[2] , len(row[1])])
            if i == ran:
                if len(ans) < 20:
                    ran = ran * 10

                else:
                    break
            i += 1

        try:
            mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
            pending = 0
            for i in mynoti.notifications.all():
                if i.view == False:
                    pending = pending + 1

            mynoti_list = [i for i in mynoti.notifications.all()]

        except:
            mynoti_list = []
            pending = 0

        return render(request , 'photo_search_quotes.html' , {'post' : ans , 's': s , 'length' : len(ans) ,'pending' : pending , 'notification' : mynoti_list[::-1]})


    except:
        return render(request, 'error.html')



def searchProfile(request):
    try:
        searchuser = request.GET['sUser']
        u = User.objects.get(username=searchuser)
        pro = Profile.objects.get_or_create(user=u)
        likes = MyLike.objects.get(user=request.user)
        likePost = likes.likedPost.all()
        liked = False
        yes = False
        liked = False
        follower_len = 0
        p = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        user_list = []
        user = User.objects.exclude(username = request.user)
        following_list = Following.objects.get_or_create(user = request.user)[0].following.all()

        save = MySave.objects.get(user = request.user)
        savepost = save.savedPost.all()
        saved = False

        following = Following.objects.get_or_create(user = u)
        following_len = following[0].following_count

        follow = Follower.objects.get_or_create(user=u)
        if request.user in follow[0].follower.all():
            yes = True

            follower_len = follow[0].follow_count



        post = Post.objects.filter(user=u)
        for i in post:
            if i in likePost:
                liked = True

            like = Like.objects.get_or_create(post = i)
            like_c = like[0].like_count

            savep = SavePost.objects.get(post=i)
            save_c = savep.save_count

            if i in savepost:
                saved = True

            p.append([i, liked , like_c , saved , save_c ])

        count = 0
        lp = []
        for i in p:
            if count % 2 == 0:
                lp.append([])
                cd = count // 2
                lp[cd].append(i)
            else:
                cd = count // 2
                lp[cd].append(i)

            count += 1

        for i in user:
            if i in following_list:
                pass
            else:
                user_list.append(i)


        return render(request, 'photo_searchProfile_two.html', {'myuser': u, 'post': lp , 'post_l': len(p) , 'followers' : follower_len ,  'following' : following_len ,'yes' : yes , 'user_list' : user_list , 'user_c' : len(user_list) , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def singlePost(request):
    try:
        p = request.GET.get('post')
        post_asked = Post.objects.get(sno = p)
        comment_asked  = Comment.objects.filter(post = post_asked)
        like_asked = Like.objects.get_or_create(post = post_asked)[0].like_count
        save_asked = SavePost.objects.get_or_create(post = post_asked)[0].save_count
        post_asked_liked = False
        post_asked_saved = False

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        if post_asked in MyLike.objects.get_or_create(user = request.user)[0].likedPost.all():
            post_asked_liked = True

        if post_asked in MySave.objects.get_or_create(user = request.user)[0].savedPost.all():
            post_asked_saved = True

        user = post_asked.user

        post = Post.objects.filter(user = user)
        p = []
        for i in post:
            l = Like.objects.get_or_create(post = i)
            l_c = l[0].like_count
            p.append([i , l_c])

        count = 0
        lp = []
        for i in p:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1
        child_comment = []
        parent_comment = []
        for i in comment_asked:
            if i.parent == None:
                parent_comment.append(i)
            else:
                child_comment.append(i)

        len_comm = len(child_comment) + len(parent_comment)

        return render(request , 'photo_single_post.html' , {'post_asked':post_asked , 'like_asked' : like_asked  , 'save_asked' : save_asked, 'post_asked_liked' : post_asked_liked  , 'post_asked_saved' : post_asked_saved ,  'parent_comment' : parent_comment , 'child_comment' : child_comment ,'comment_asked' : len_comm , 'post' : lp , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        messages.error(request, 'Error : Post Not Found')
        return redirect('profile')



def singleHomePost(request):
    try:
        p = request.GET.get('post')
        post_asked = Post.objects.get(sno = p)
        comment_asked  = Comment.objects.filter(post = post_asked)
        save_asked = SavePost.objects.get_or_create(post = post_asked)[0].save_count
        like_asked = Like.objects.get_or_create(post = post_asked)[0].like_count
        following = Following.objects.get_or_create(user = request.user)[0]
        following_list = following.following.all()
        post_asked_saved = False

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        if post_asked in MySave.objects.get_or_create(user = request.user)[0].savedPost.all():
            post_asked_saved = True

        post_asked_liked = False
        if post_asked in MyLike.objects.get_or_create(user = request.user)[0].likedPost.all():
            post_asked_liked = True

        user = post_asked.user

        p = []

        for i in following_list :
            liked = False
            saved = False
            post = Post.objects.filter(user=i)
            for j in post:

                like = Like.objects.get_or_create(post = j)
                like_c = like[0].like_count
                liked_user = [i for i in like[0].liker.all()]
                random.shuffle(liked_user)
                save = SavePost.objects.get_or_create(post = j)
                save_c = save[0].save_count

                p.append([j , like_c , save_c , i ])

        count = 0
        lp = []
        for i in p:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1

        child_comment = []
        parent_comment = []

        for i in comment_asked:
            if i.parent == None:
                parent_comment.append(i)
            else:
                child_comment.append(i)




        len_comm = len(child_comment) + len(parent_comment)

        return render(request , 'photo_single_home_post.html' , {'post_asked':post_asked , 'save_asked' : save_asked ,'like_asked' : like_asked , 'post_asked_liked' : post_asked_liked , 'post_asked_saved' : post_asked_saved,  'parent_comment' : parent_comment , 'child_comment' : child_comment ,'comment_asked' : len_comm , 'post' : lp , 'pending' : pending , 'notification' : mynoti_list[::-1]})


    except:
        return render(request, 'error.html')



def singleExplorerPost(request):
    try:
        p = request.GET.get('post')
        post_asked = Post.objects.get(sno = p)
        comment_asked = Comment.objects.filter(post = post_asked)
        user = post_asked.user
        like_asked = Like.objects.get_or_create(post=post_asked)[0].like_count
        save_asked = SavePost.objects.get_or_create(post=post_asked)[0].save_count
        post_asked_liked = False
        post_asked_saved = False
        if post_asked in MyLike.objects.get_or_create(user=request.user)[0].likedPost.all():
            post_asked_liked = True

        if post_asked in MySave.objects.get_or_create(user=request.user)[0].savedPost.all():
            post_asked_saved = True
        user = User.objects.exclude(username=request.user)
        following = Following.objects.get_or_create(user=request.user)
        f = following[0].following.all()
        post = Post.objects.exclude(user=request.user)
        user_list = []
        l = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]


        for i in post:
            like = Like.objects.get_or_create(post=i)
            like_c = like[0].like_count

            save = SavePost.objects.get_or_create(post=i)
            save_c = save[0].save_count

            l.append([i, like_c , save_c])

        count = 0
        lp = []
        random.shuffle(l)
        for i in l[:8]:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1

        child_comment = []
        parent_comment = []
        for i in comment_asked:
            if i.parent == None:
                parent_comment.append(i)
            else:
                child_comment.append(i)

        len_comm = len(child_comment) + len(parent_comment)


        return render(request , 'photo_single_explore_post.html' , {'post_asked':post_asked , 'save_asked' : save_asked ,'like_asked' : like_asked , 'post_asked_liked' : post_asked_liked , 'post_asked_saved' : post_asked_saved, 'post' : lp , 'parent_comment' : parent_comment , 'child_comment' : child_comment ,'comment_asked' : len_comm , 'pending' : pending , 'notification' : mynoti_list[::-1]})


    except:
        return render(request, 'error.html')



def singleHashPost(request):
    try:
        p = request.GET.get('tag')
        h = request.GET.get('hash')
        post_asked = Post.objects.get(sno = p)
        comment_asked = Comment.objects.filter(post = post_asked)
        like_asked = Like.objects.get_or_create(post=post_asked)[0].like_count
        save_asked = SavePost.objects.get_or_create(post=post_asked)[0].save_count
        post_asked_liked = False
        post_asked_saved = False
        if post_asked in MyLike.objects.get_or_create(user=request.user)[0].likedPost.all():
            post_asked_liked = True

        if post_asked in MySave.objects.get_or_create(user=request.user)[0].savedPost.all():
            post_asked_saved = True

        following = Following.objects.get_or_create(user=request.user)
        post = HashTag.objects.get(tag_name = h).tag_posts.all()

        l = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]


        for i in post:
            like = Like.objects.get_or_create(post=i)
            like_c = like[0].like_count

            save = SavePost.objects.get_or_create(post=i)
            save_c = save[0].save_count

            l.append([i, like_c , save_c])

        count = 0
        lp = []
        random.shuffle(l)
        for i in l[:8]:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1

        child_comment = []
        parent_comment = []
        for i in comment_asked:
            if i.parent == None:
                parent_comment.append(i)
            else:
                child_comment.append(i)

        len_comm = len(child_comment) + len(parent_comment)


        return render(request , 'photo_single_hash_post.html' , {'post_asked':post_asked , 'save_asked' : save_asked ,'like_asked' : like_asked , 'post_asked_liked' : post_asked_liked , 'post_asked_saved' : post_asked_saved, 'post' : lp , 'length' : len(post), 'parent_comment' : parent_comment , 'child_comment' : child_comment ,'comment_asked' : len_comm , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')




def feed(request):
    try:
        following = Following.objects.get_or_create(user = request.user)
        likes = MyLike.objects.get_or_create(user = request.user)
        likePost = likes[0].likedPost.all()
        liked = False
        mysavedpost = MySave.objects.get_or_create(user = request.user)
        savepost = mysavedpost[0].savedPost.all()
        saved = False
        f = following[0].following.all()
        ft = following[0].following_tag.all()
        l = []
        user = User.objects.exclude(username = request.user)
        user_list = []

        mynoti = MyNotifacions.objects.get_or_create(user = request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]


        hash_post = []
        for i in ft:
            liked = False
            saved = False
            hash = HashTag.objects.get(tag_name=i)
            for j in hash.tag_posts.all():
                liked = False
                saved = False
                if j in likePost:
                    liked = True

                if j in savepost:
                    saved = True

                like = Like.objects.get_or_create(post=j)
                like_c = like[0].like_count
                liked_user = [i for i in like[0].liker.all()]
                random.shuffle(liked_user)
                if len(liked_user) >= 11:
                    liked_user = liked_user[:10]
                save = SavePost.objects.get_or_create(post=j)
                save_c = save[0].save_count

                l.append([j, liked, like_c, saved, save_c, j.user , liked_user])


        for i in f:
            liked = False
            saved = False
            post = Post.objects.filter(user=i)
            for j in post:
                liked = False
                saved = False
                if j in likePost:
                    liked = True

                if j in savepost:
                    saved = True

                like = Like.objects.get_or_create(post = j)
                like_c = like[0].like_count
                liked_user = [i for i in like[0].liker.all()]
                random.shuffle(liked_user)
                if len(liked_user) >= 11:
                    liked_user = liked_user[:10]
                save = SavePost.objects.get_or_create(post = j)
                save_c = save[0].save_count
                comment = len(Comment.objects.filter(post = j))
                l.append([j, liked , like_c , saved , save_c , i , liked_user , comment])


        for i in user:
            if i in f:
                pass
            else:
                user_list.append(i)

        random.shuffle(l)
        random.shuffle(user_list)

        return render(request , 'photo_home.html' , {'post' : l , 'length' : len(l), 'user_list' : user_list , 'user_c' : len(user_list) , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def notifications(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            noti = Notifications.objects.get(sno = i.sno)
            noti.view = True
            noti.save()

        mynoti_list = [i for i in mynoti.notifications.all()]

        return render(request , 'photo_notifications.html' , {'pending' : pending , 'notifications' : mynoti_list[::-1] , 'length' : len(mynoti_list)})

    except:
        return render(request, 'error.html')



def deleteNoti(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user = request.user)[0]
        mynoti.delete()

        return redirect('feed')

    except:
        return render(request, 'error.html')



def uploadPage(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]
        return render(request ,'photo_upload.html' , {'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def profileChangePage(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]
        return render(request ,'photo_profile_change.html' , {'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def uploadProfile(request):
    try:
        if request.method == "POST":
            image = request.FILES['uppic']
            user = request.user

            profile = Profile.objects.get(user = user)
            profile.profile_picture = image
            profile.save()
            return redirect('profile')

    except:
        return render(request, 'error.html')



def postComment(request):
    try:
        if request.method == 'POST' :
            comments = request.POST['comment']
            post = request.POST['post']
            parent = request.POST['sno']
            home = request.POST['home']
            post = Post.objects.get(sno = post)
            user = request.user
            myNoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
            noti = Notifications(My_user=post.user)
            noti.purpose = 'C'
            noti.user = request.user
            noti.post = post
            noti.save()
            myNoti.AddNotification(post.user, noti)



            if parent == "":
                comment = Comment(comments = comments , post = post , user = user)
                comment.save()


            else:
                ParentComment = Comment.objects.get(sno = parent)
                comment = Comment(comments = comments , post = post , user = user , parent = ParentComment)
                comment.save()

            if home == 'Home':
                s = "/read/viewHomePost?post=" + str(post.sno)

            elif home == 'Explore':
                s = '/read/viewExplorerPost?post=' + str(post.sno)

            else:
                s = "/read/viewPost?post=" + str(post.sno)

            return redirect(s)

    except:
        return render(request, 'error.html')



def deleteComment(request):
    try:
        sno = request.GET.get('sno')
        comment = Comment.objects.get(sno = sno)
        comment.delete()
        return HttpResponse(content_type="application/json")

    except:
        return render(request, 'error.html')



def deletePost(request):
    try:
        sno = request.GET.get('sno')
        post = Post.objects.get(sno = sno)
        post.delete()

        return redirect('profile')

    except:
        return render(request, 'error.html')



def explore(request):
    try:
        user = User.objects.exclude(username = request.user)
        following = Following.objects.get_or_create(user = request.user)
        f = following[0].following.all()
        post = Post.objects.exclude(user = request.user)
        user_list = []
        l = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]


        for i in post:
            like = Like.objects.get_or_create(post = i)
            like_c = like[0].like_count

            l.append([i,like_c])

        count = 0
        lp = []
        random.shuffle(l)
        for i in l:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1


        count = 0
        for i in user:
            if i in f:
                pass
            else:
                p = Post.objects.filter(user=i)
                if bool(p) == True:
                    user_list.append([i , p[0]])

        random.shuffle(user_list)


        #For shayari explore
        f = open(r'C:\Users\Mr.Mg\Documents\Python\Projects\quotesbook1\Data/Book.csv', encoding="utf8")
        csv_f = csv.reader(f)
        ans = []
        shayari_list = [i for i in csv_f]
        shayari_list = shayari_list[1:]
        random.shuffle(shayari_list)
        for row in shayari_list[:10]:
            if len(row[1])<300:
                ans.append([row[1], row[0], row[2]])


        count = 0
        ls = []
        for i in ans:
            if count % 3 == 0:
                ls.append([])
                cd = count // 3
                ls[cd].append(i)
            else:
                cd = count // 3
                ls[cd].append(i)

            count += 1


        #for quotes Explore
        f = open(r'C:\Users\Mr.Mg\Documents\Python\Pratice/quotes.csv', encoding="utf8")
        csv_f = csv.reader(f)
        ans = []
        quotes_list = []
        count = 0
        for i in csv_f:
            count = count +1
            if count == 100:
                break
            quotes_list.append(i)
        quotes_list = quotes_list[1:]
        random.shuffle(quotes_list)
        for row in quotes_list[:10]:
            if len(row[0]) <= 300:
                    ans.append([row[0], row[1], row[2]])

        count = 0
        lq = []
        for i in ans:
            if count % 3 == 0:
                lq.append([])
                cd = count // 3
                lq[cd].append(i)
            else:
                cd = count // 3
                lq[cd].append(i)

            count += 1


        return render(request , 'photo_explore.html' , { 'post' : lp[:3] , 'user_list' : user_list , 'shayari' : ls , 'quotes' : lq , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def upload(request):
    try:
        if request.method == "POST":
            image = request.FILES['uppic']
            caption = request.POST['cap']
            user = request.user

            post = Post(image = image , caption = caption , user = user)
            post.save()


            if len(caption) != 0:
                tag = []
                for i in caption.split(" "):
                    if i[0] == "#":
                        tag.append(i[1:])

                for i in tag:
                    hash = HashTag.objects.get_or_create(tag_name = i)
                    hash[0].addPost(i , post)

                    hash[0].post_count = len(hash[0].tag_posts.all())
                    hash[0].save()

            return redirect('profile')

        else:
            return render(request, 'error.html')

    except:
        return render(request, 'error.html')



def editProfile(request):
    try:
        if request.method == 'POST':
            user = request.POST['userName']
            location = request.POST['location']
            bio = request.POST['bio']

            mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
            pending = 0
            for i in mynoti.notifications.all():
                if i.view == False:
                    pending = pending + 1

            mynoti_list = [i for i in mynoti.notifications.all()]

            myuser = Profile.objects.get(user = request.user)
            myuser.bio = bio
            myuser.location = location
            myuser.save()
            myuser = User.objects.get(username = request.user)
            myuser.username = user
            #myuser.save()
            myuser = User.objects.get(username = user)

            return render(request , 'profile.html' , {'myuser' : myuser , 'pending' : pending , 'notification' : mynoti_list[::-1]})

        else:
            return render(request, 'error.html')

    except:
        return render(request, 'error.html')



def follow(request):
    try:
        f = request.GET.get('follower')
        if f[0] != '#':
            u = User.objects.get(username=f)

            follow = Follower.objects.filter(user = u , follower = request.user)
            followed = False
            myNoti = MyNotifacions.objects.get_or_create(user = request.user)[0]

            if bool(follow) == True:

                Follower.unfollow(u , request.user) #followers remover

                Following.unfollowing(request.user , u) #following remover




            else:
                followed = True
                Follower.follow(u , request.user) #follower adder

                Following.follow(request.user , u) #following adder
                noti = Notifications(My_user = u)
                noti.purpose = 'F'
                noti.user = request.user
                noti.save()
                myNoti.AddNotification(u, noti)

            #follower counting
            follow = Follower.objects.get(user=u)
            follow.follow_count = len(follow.follower.all())
            follow.save()

            #following counting
            following = Following.objects.get(user=request.user)
            following.following_count = len(following.following.all())
            following.save()


            resp = {
                    'follower' : followed ,
                    'followers': follow.follow_count
                }

        else:
            tag = HashTag.objects.get(tag_name = f)
            myfollowing = Following.objects.get_or_create(user = request.user)[0]
            followed = False

            if request.user in tag.followers.all():
                tag.rmvFollowers(tag , request.user)
                myfollowing.unfollowingTag(request.user , tag)


            else:
                tag.addFollowers(tag, request.user)
                myfollowing.followingTag(request.user , tag)
                followed = True

            tag.followers_count = len(tag.followers.all())
            tag.save()

            resp = {
                'follower': followed,
                'followers': tag.followers_count
            }


        response = json.dumps(resp)

        return HttpResponse(response , content_type="application/json")

    except:
        return render(request, 'error.html')



def like(request):
    try:
        f = request.GET.get('liker')
        post = Post.objects.get(sno = f)
        user = request.user

        like = Like.objects.filter(post = post , liker = request.user)
        myNoti = MyNotifacions.objects.get_or_create(user = request.user)[0]
        liked = False

        if bool(like) == True:
            Like.unlike(post, request.user)  # like remover
            MyLike.unlike(user, post)



        else:
            liked = True
            Like.like(post, request.user)  # like adder
            MyLike.like(user, post)

            noti = Notifications(My_user = post.user)
            noti.purpose = 'L'
            noti.user = request.user
            noti.post = post
            noti.save()
            myNoti.AddNotification(post.user, noti)


        # like counting
        like = Like.objects.get(post=post)
        like.like_count = len(like.liker.all())
        like.save()

        mylike = MyLike.objects.get(user=user)
        mylike.post_count = len(mylike.likedPost.all())
        mylike.save()

        resp = {
            'liker': liked,
            'like_c': like.like_count
        }

        response = json.dumps(resp)

        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def save(request):
    try:
        f = request.GET.get('saver')

        post = Post.objects.get(sno = f)
        user = request.user


        myNoti = MyNotifacions.objects.get_or_create(user = request.user)[0]
        save = SavePost.objects.filter(post = post , saver = request.user)


        saved = False

        if bool(save) == True:

            SavePost.unsavepost(post, request.user)  # like remover
            MySave.unsavepost(user, post)



        else:
            saved = True
            SavePost.savepost(post, request.user)  # like adder
            MySave.savepost(user, post)


            noti = Notifications(My_user = post.user)
            noti.purpose = 'S'
            noti.user = request.user
            noti.post = post
            noti.save()
            myNoti.AddNotification(post.user, noti)

        # like counting
        save = SavePost.objects.get(post=post)
        save.save_count = len(save.saver.all())
        save.save()

        mysave = MySave.objects.get(user=user)
        mysave.post_count = len(mysave.savedPost.all())
        mysave.save()

        resp = {
            'saver': saved,
            'save_c' : save.save_count
        }

        response = json.dumps(resp)

        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def postLiked(request):
    try:
        myLiked = MyLike.objects.get_or_create(user = request.user)
        post = myLiked[0].likedPost.all()
        mysavedpost = MySave.objects.get_or_create(user=request.user)
        savepost = mysavedpost[0].savedPost.all()
        saved = False
        l = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        for i in post:
            like = Like.objects.get(post = i)
            likecount = like.like_count

            if i in savepost:
                saved = True
            save = SavePost.objects.get_or_create(post=i)
            save_c = save[0].save_count
            l.append([i , likecount ,True , saved , save_c , i.user])

        count = 0
        lp = []
        for i in l:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1

        return render(request , 'photo_savedPost.html' , {"post" : lp , 'length' : len(post) , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def postSaved(request):
    try:
        myLiked = MyLike.objects.get_or_create(user = request.user)
        likepost = myLiked[0].likedPost.all()
        liked = False
        mysavedpost = MySave.objects.get_or_create(user=request.user)
        savepost = mysavedpost[0].savedPost.all()
        l = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        for i in savepost:
            like = Like.objects.get(post = i)
            likecount = like.like_count

            if i in likepost:
                liked = True

            save = SavePost.objects.get_or_create(post=i)
            save_c = save[0].save_count
            l.append([i ,likecount, liked , True , save_c , i.user ])

        count = 0
        lp = []
        for i in l:
            if count % 3 == 0:
                lp.append([])
                cd = count // 3
                lp[cd].append(i)
            else:
                cd = count // 3
                lp[cd].append(i)

            count += 1

        return render(request , 'photo_savedPost.html' , {"post" : lp , "length" : len(savepost) ,'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')


def follower(request):
    try:
        u = request.GET['sUser']
        u = User.objects.get(username = u)
        myfollower = Follower.objects.get_or_create(user = u)
        myfollower_list = myfollower[0].follower.all()
        myfollowing = Following.objects.get_or_create(user = u)
        myfollowing_list = myfollowing[0].following.all()

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        f= []
        for i in myfollower_list:
            followed = False
            user_follower = Follower.objects.get_or_create(user = i)
            followers_c = user_follower[0].follow_count
            user_follower_list = [ i for i in user_follower[0].follower.all()]
            random.shuffle(user_follower_list)
            if len(user_follower_list) >= 6:
                user_follower_list = user_follower_list[:5]

            user_following = Following.objects.get_or_create(user = i)
            following_c = user_following[0].following_count
            user_following_list = [i for i in user_following[0].following.all()]
            random.shuffle(user_following_list)
            if len(user_following_list) >= 6:
                user_following_list = user_following_list[:6]


            if i in myfollowing_list:
                followed = True

            f.append([i , followers_c , following_c , followed , user_follower_list , user_following_list])

        return render(request , 'photo_followers.html' , {"myfollower_list" : f , 'length' : len(f), 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')


def following(request):
    try:
        u = request.GET.get('sUser')
        u = User.objects.get(username=u)
        myfollowing = Following.objects.get_or_create(user = u)
        myfollowing_list = myfollowing[0].following.all()
        f = []

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        for i in myfollowing_list:
            user_follower = Follower.objects.get_or_create(user=i)
            followers_c = user_follower[0].follow_count
            user_follower_list = [i for i in user_follower[0].follower.all()]
            random.shuffle(user_follower_list)
            if len(user_follower_list) >= 6:
                user_follower_list = user_follower_list[:5]

            user_following = Following.objects.get_or_create(user=i)
            following_c = user_following[0].following_count
            user_following_list = [i for i in user_following[0].following.all()]
            random.shuffle(user_following_list)
            if len(user_following_list) >= 6:
                user_following_list = user_following_list[:6]



            f.append([i , followers_c , following_c , True , user_follower_list , user_following_list])

        return render(request , 'photo_followers.html' , {"myfollower_list" : f , 'length' : len(f), 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')


#contact
def contactPage(request):
    try:
        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]
        return render(request , 'photo_contact.html' , {'pending' : pending , 'notification' : mynoti_list[::-1]})
    except:
        return render(request, 'error.html')



def handlecontact(request):
    try:
        if request.method == 'POST':
            text = request.POST['message']
            name = request.POST['name']
            email = request.POST['emailId']
            subject = request.POST['subject']

            contact = Contact(name = name , email = email , subject = subject ,message = text)
            contact.save()

        messages.success(request, 'Your Feedback has been submitted')
        return redirect('profile')

    except:
        return render(request, 'error.html')



def handlesignout(request):
    try:
        logout(request)
        messages.success(request , "successfully signed out")
        return redirect('/')

    except:
        return render(request, 'error.html')



def check(request):
    try:
        user_name = request.POST['user_name']
        user = User.objects.filter(username = user_name)
        data = True
        if bool(user) == True:
            data = False

        resp = {
            'data': data,
        }

        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def checkEmail(request):
    try:
        email = request.POST['emailId']

        user = User.objects.filter(email=email)
        data = True
        rev = email[::-1]
        if bool(user) == True :
            data = False



        resp = {
            'data': data,
        }

        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def delete(request):
    try:
        p = request.GET.get('post_id')
        post = Post.objects.get(sno = p)
        post.delete()
        post = Post.objects.filter(user = request.user)

        resp = {
            'post_c': len(post)
        }

        response = json.dumps(resp)

        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def hashtagFollow(request):
    try:
        hashname = request.GET.get('hashname')
        following = False


        tag = HashTag.objects.get(tag_name = hashname)
        myfollowing = Following.objects.get_or_create(user = request.user)
        if request.user in tag.followers.all():
            following = True

        if following == True:
            tag.rmvFollowers(hashname , request.user)
            myfollowing[0].unfollowingTag(request.user , tag)

        else:
            tag.addFollowers(hashname , request.user)
            myfollowing[0].followingTag(request.user, tag)

        tag.followers_count = len(tag.followers.all())
        tag.save()

        resp = {
            'follower': following,
            'followers': tag.followers_count
        }

        response = json.dumps(resp)

        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def setttings(request):
    try:
        user = User.objects.get(username = request.user)
        user_details = [user.first_name , user.last_name , user.username , user.email]
        profile = Profile.objects.get(user = request.user)
        profile_details = [profile.bio , profile.phone  , profile.privacy ,profile.gender]

        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        return render(request , 'photo_settings.html' , {'user_details' : user_details , 'profile_details' : profile_details , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



def generalSettings(request):
    try:
        user = User.objects.get(username = request.user)
        profile = Profile.objects.get_or_create(user = request.user)



        if request.method == 'POST':
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            userName = request.POST['userName']
            email = request.POST['email']
            phone = request.POST['phone']
            bio = request.POST['bio']
            gender = request.POST['gender']
            #privacy = request.POST['privacy']

            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.username = userName
            user.save()

            profile[0].bio = bio
            profile[0].phone = phone
            #profile.privacy = privacy
            profile[0].gender = gender
            profile[0].save()


            return redirect('profile')

    except:
        return render(request, 'error.html')



def changePassword(request):
    try:
        user = User.objects.get(username = request.user)
        if request.method == "POST":
            currentPassword = request.POST['currentPassword']
            newPassword = request.POST['newPassword']
            confirmPassword = request.POST['confirmPassword']

            if user.password == currentPassword:
                if newPassword == confirmPassword:
                    user.password = newPassword
                    user.save()

            return redirect('profile')

    except:
        return render(request, 'error.html')



def blocking(request):
    try:
        s = request.GET.get('blocked')
        user = request.user
        block = Blocking.objects.filter(user = s , blocked_by = user)
        myBlocking = MyBlocking.objects.get_or_create(user = user)
        myfollowing = Following.objects.get_or_create(user = user)
        myfollowers = Follower.objects.get_or_create(user = user)

        blocked = False

        if bool(block) == True:
            block.unblocked(s , user)
            myBlocking.unblocked(s , user)

        else:
            blocked = True
            block.blocked(s , user)
            myBlocking.blocked(s , user)
            if s in myfollowing.following.all():
                myfollowing.unfollow(user , s)

            if user in myfollowers.follower.all():
                myfollowers.unfollow(user, s)

        block.blocked_count = len(block.bocked_by.all())
        block.save()

        myBlocking.blocked_count = len(myBlocking.blockedUser.all())
        myBlocking.save()


        resp = {
            'blocked': blocked,
        }

        response = json.dumps(resp)

        return HttpResponse(response, content_type="application/json")

    except:
        return render(request, 'error.html')



def searchHash(request):
    try:
        s = request.GET['tag']
        hash = HashTag.objects.get(tag_name = s)
        follower_len = hash.followers_count
        myfollowing_list = Following.objects.get_or_create(user = request.user)[0].following.all()
        post = hash.tag_posts.all()
        likePost = MyLike.objects.get_or_create(user = request.user)[0].likedPost.all()
        savePost = MySave.objects.get_or_create(user = request.user)[0].savedPost.all()
        user_list = []
        user = User.objects.exclude(username=request.user)


        mynoti = MyNotifacions.objects.get_or_create(user=request.user)[0]
        pending = 0
        for i in mynoti.notifications.all():
            if i.view == False:
                pending = pending + 1

        mynoti_list = [i for i in mynoti.notifications.all()]

        p = []
        for i in post:
            liked = False
            saved = False
            if i in likePost:
                liked = True

            like = Like.objects.get_or_create(post = i)
            like_c = like[0].like_count

            savep = SavePost.objects.get(post=i)
            save_c = savep.save_count

            if i in savePost:
                saved = True

            p.append([i, liked , like_c , saved , save_c ])

        count = 0
        lp = []
        for i in p:
            if count % 2 == 0:
                lp.append([])
                cd = count // 2
                lp[cd].append(i)
            else:
                cd = count // 2
                lp[cd].append(i)

            count += 1

        for i in user:
            if i in myfollowing_list:
                pass
            else:
                user_list.append(i)

            return render(request, 'photo_searchHash_two.html', {'myuser': hash, 'post': lp , 'post_l': len(p) , 'followers' : follower_len  , 'user_list' : user_list , 'user_c' : len(user_list) , 'pending' : pending , 'notification' : mynoti_list[::-1]})

    except:
        return render(request, 'error.html')



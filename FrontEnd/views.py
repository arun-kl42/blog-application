from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from FrontEnd.models import BlogUser, Blog
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def save_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                return redirect(register)
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                return redirect(login)
        else:
            return redirect(register)


def save_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            return redirect(login)


def logout(request):
    auth.logout(request)
    return redirect(home)


def blog(request):
    return render(request, 'blog.html')


def profile_actions(request):
    user = request.user
    profile_exists = BlogUser.objects.filter(user=user).exists()  # Check if a BlogUser profile exists
    return render(request, 'profile_actions.html', {'user': user, 'profile_exists': profile_exists})


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Check if the BlogUser profile exists for the user
    try:
        blog_user = BlogUser.objects.get(user=user)  # Correct way to fetch the BlogUser
        profile_exists = True
    except BlogUser.DoesNotExist:
        blog_user = None  # Handle case where BlogUser doesn't exist
        profile_exists = False

    return render(request, 'profile.html', {'user': user, 'blog_user': blog_user, 'profile_exists': profile_exists})


def profilecard(request, user_id):
    # Fetch the user using the user_id
    user = get_object_or_404(User, id=user_id)

    # Attempt to retrieve the BlogUser profile associated with the user
    try:
        blog_user = BlogUser.objects.get(user=user)  # Use user ForeignKey
    except BlogUser.DoesNotExist:
        blog_user = None  # Handle the case where the BlogUser doesn't exist

    return render(request, 'profilecard.html', {'user': user, 'blog_user': blog_user})


def save_blog_user(request):
    if request.method == "POST":
        user = request.user  # Get the logged-in user
        bio = request.POST.get('bio')
        image = request.FILES.get('profile')

        # Create or update the BlogUser instance
        blog_user, created = BlogUser.objects.update_or_create(
            user=user,
            defaults={'bio': bio, 'profile_image': image}
        )

        return redirect('profilecard', user_id=user.id)


def blog_list(request):
    blogs = Blog.objects.all()  # Retrieve all blog posts
    return render(request, 'blog_list.html', {'blogs': blogs})


def blogform(request):
    return render(request, 'blogform.html')


@login_required
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        image = request.FILES.get('image')  # Handle file upload

        if title and description:  # Basic validation
            obj = Blog(
                user=request.user.bloguser,  # Assuming BlogUser is linked to the User model
                title=title,
                description=description,
                tags=tags,
                image=image,
            )
            obj.save()
            return redirect('list')  # Ensure this name matches what you defined
    return render(request, 'blogform.html')


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Fetch the blog by ID
    return render(request, 'blog_detail.html', {'blog': blog})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == "POST":
        blog.delete()  # Delete the blog post
        return redirect('list')  # Redirect to the blog list after deletion

    return render(request, 'confirm_delete.html', {'blog': blog})  # Render a confirmation template if needed

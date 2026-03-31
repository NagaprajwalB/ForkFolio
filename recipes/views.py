from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .models import Recipe, Category, Rating
from .forms import RegisterForm, RecipeForm, IngredientFormSet, StepFormSet, RatingForm


def home(request):
    featured = Recipe.objects.all()[:6]
    categories = Category.objects.all()
    top_rated = sorted(Recipe.objects.all(), key=lambda r: r.average_rating(), reverse=True)[:4]
    return render(request, 'recipes/home.html', {
        'featured': featured,
        'categories': categories,
        'top_rated': top_rated,
    })


def recipe_list(request):
    recipes = Recipe.objects.all()
    categories = Category.objects.all()

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    max_time = request.GET.get('max_time', '')

    if q:
        recipes = recipes.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(ingredients__name__icontains=q)
        ).distinct()

    if category:
        recipes = recipes.filter(category__slug=category)

    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)

    if max_time:
        try:
            mt = int(max_time)
            recipes = [r for r in recipes if r.total_time() <= mt]
        except ValueError:
            pass

    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'categories': categories,
        'q': q,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'max_time': max_time,
    })


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ratings = recipe.ratings.all().order_by('-created_at')
    user_rating = None
    rating_form = RatingForm()

    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(recipe=recipe, user=request.user)
            rating_form = RatingForm(instance=user_rating)
        except Rating.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated:
        if user_rating:
            form = RatingForm(request.POST, instance=user_rating)
        else:
            form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            messages.success(request, 'Rating submitted!')
            return redirect('recipe_detail', slug=slug)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'ratings': ratings,
        'user_rating': user_rating,
        'rating_form': rating_form,
    })


@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        step_formset = StepFormSet(request.POST, prefix='steps')

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            base_slug = slugify(recipe.title)
            slug = base_slug
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            recipe.slug = slug
            recipe.save()

            ingredients = ingredient_formset.save(commit=False)
            for i, ing in enumerate(ingredients):
                ing.recipe = recipe
                ing.order = i
                ing.save()

            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps):
                step.recipe = recipe
                step.order = i + 1
                step.save()

            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        step_formset = StepFormSet(prefix='steps')

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'action': 'Create',
    })


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(request.POST, instance=recipe, prefix='steps')

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            form.save()
            ingredient_formset.save()
            steps = step_formset.save(commit=False)
            for i, step in enumerate(steps):
                step.recipe = recipe
                step.order = i + 1
                step.save()
            for obj in step_formset.deleted_objects:
                obj.delete()
            messages.success(request, 'Recipe updated!')
            return redirect('recipe_detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe, prefix='ingredients')
        step_formset = StepFormSet(instance=recipe, prefix='steps')

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
        'action': 'Edit',
    })


@login_required
def recipe_delete(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted.')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


def profile(request, username):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'recipes/profile.html', {'profile_user': user, 'recipes': recipes})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'recipes/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'recipes/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

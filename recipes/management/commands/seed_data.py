from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Category, Recipe, Ingredient, Step


class Command(BaseCommand):
    help = 'Seed the database with sample categories and recipes'

    def handle(self, *args, **kwargs):
        # Create categories
        cats = [
            ('Breakfast', 'breakfast', '🥞'),
            ('Italian', 'italian', '🍝'),
            ('Indian', 'indian', '🍛'),
            ('Desserts', 'desserts', '🍰'),
            ('Salads', 'salads', '🥗'),
            ('Soups', 'soups', '🍜'),
            ('Baking', 'baking', '🍞'),
            ('Vegan', 'vegan', '🌱'),
        ]
        for name, slug, icon in cats:
            Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
        self.stdout.write(self.style.SUCCESS('✅ Categories created'))

        # Create demo user
        user, created = User.objects.get_or_create(username='chef_demo', defaults={
            'email': 'demo@forkfolio.com'
        })
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Demo user created: chef_demo / demo1234'))

        # Sample recipes
        recipes_data = [
            {
                'title': 'Classic Spaghetti Carbonara',
                'slug': 'classic-spaghetti-carbonara',
                'category': 'italian',
                'description': 'A rich and creamy Roman pasta dish made with eggs, cheese, pancetta, and pepper. Simple ingredients, extraordinary result.',
                'prep_time': 10, 'cook_time': 20, 'servings': 4, 'difficulty': 'medium',
                'ingredients': [
                    ('Spaghetti', '400', 'g'),
                    ('Pancetta or bacon', '150', 'g'),
                    ('Eggs', '4', ''),
                    ('Pecorino Romano', '100', 'g'),
                    ('Black pepper', '1', 'tsp'),
                    ('Salt', '1', 'tsp'),
                ],
                'steps': [
                    'Bring a large pot of salted water to boil and cook spaghetti until al dente.',
                    'Fry pancetta in a pan over medium heat until crispy. Remove from heat.',
                    'Whisk eggs with grated Pecorino Romano and a generous amount of black pepper.',
                    'Reserve 1 cup of pasta water before draining. Add hot pasta to the pancetta pan.',
                    'Remove pan from heat. Quickly stir in egg mixture, adding pasta water to create a silky sauce.',
                    'Serve immediately with extra cheese and black pepper.',
                ],
            },
            {
                'title': 'Butter Chicken (Murgh Makhani)',
                'slug': 'butter-chicken-murgh-makhani',
                'category': 'indian',
                'description': 'Tender chicken in a velvety tomato-cream sauce, fragrant with aromatic spices. The ultimate Indian comfort food.',
                'prep_time': 20, 'cook_time': 40, 'servings': 6, 'difficulty': 'medium',
                'ingredients': [
                    ('Chicken thighs', '700', 'g'),
                    ('Yogurt', '100', 'ml'),
                    ('Garam masala', '2', 'tsp'),
                    ('Butter', '3', 'tbsp'),
                    ('Tomato puree', '400', 'ml'),
                    ('Heavy cream', '150', 'ml'),
                    ('Garlic cloves', '4', ''),
                    ('Ginger', '1', 'inch'),
                    ('Kashmiri chili powder', '1', 'tsp'),
                ],
                'steps': [
                    'Marinate chicken in yogurt, garam masala, and salt for at least 1 hour.',
                    'Grill or pan-fry marinated chicken until charred. Set aside.',
                    'Melt butter in a pan. Add minced garlic and ginger, sauté for 2 minutes.',
                    'Add tomato puree, chili powder, and simmer for 15 minutes.',
                    'Blend sauce until smooth. Return to heat and add grilled chicken.',
                    'Stir in cream and simmer for 10 more minutes. Garnish with cream and coriander.',
                ],
            },
            {
                'title': 'Fluffy Banana Pancakes',
                'slug': 'fluffy-banana-pancakes',
                'category': 'breakfast',
                'description': 'Light, golden pancakes with natural banana sweetness. Ready in 20 minutes — the perfect weekend breakfast.',
                'prep_time': 5, 'cook_time': 15, 'servings': 2, 'difficulty': 'easy',
                'ingredients': [
                    ('Ripe bananas', '2', ''),
                    ('Eggs', '2', ''),
                    ('All-purpose flour', '120', 'g'),
                    ('Milk', '150', 'ml'),
                    ('Baking powder', '1', 'tsp'),
                    ('Vanilla extract', '1', 'tsp'),
                    ('Butter for frying', '1', 'tbsp'),
                ],
                'steps': [
                    'Mash bananas thoroughly in a bowl.',
                    'Whisk in eggs, milk, and vanilla until smooth.',
                    'Fold in flour and baking powder. Do not overmix — lumps are fine.',
                    'Heat a non-stick pan over medium heat with a little butter.',
                    'Pour small ladles of batter. Cook until bubbles form, then flip.',
                    'Serve with maple syrup, fresh fruit, or a dusting of powdered sugar.',
                ],
            },
            {
                'title': 'Chocolate Lava Cake',
                'slug': 'chocolate-lava-cake',
                'category': 'desserts',
                'description': 'Warm, gooey chocolate cakes with a molten center that flows when you cut in. Impressive yet surprisingly easy.',
                'prep_time': 15, 'cook_time': 12, 'servings': 4, 'difficulty': 'hard',
                'ingredients': [
                    ('Dark chocolate', '200', 'g'),
                    ('Butter', '100', 'g'),
                    ('Eggs', '4', ''),
                    ('Sugar', '80', 'g'),
                    ('All-purpose flour', '40', 'g'),
                    ('Cocoa powder', '1', 'tbsp'),
                    ('Pinch of salt', '1', 'pinch'),
                ],
                'steps': [
                    'Preheat oven to 220°C (425°F). Grease 4 ramekins and dust with cocoa.',
                    'Melt chocolate and butter together over a bain-marie. Let cool slightly.',
                    'Whisk eggs and sugar until pale and thick, about 3 minutes.',
                    'Fold chocolate mixture into eggs. Sift in flour and fold gently.',
                    'Divide batter into ramekins. Refrigerate for at least 30 minutes.',
                    'Bake for exactly 12 minutes. The edges should be set but center still jiggly.',
                    'Run a knife around edge, invert onto plate, and serve immediately.',
                ],
            },
        ]

        italian = Category.objects.get(slug='italian')
        indian = Category.objects.get(slug='indian')
        breakfast = Category.objects.get(slug='breakfast')
        desserts = Category.objects.get(slug='desserts')
        cat_map = {'italian': italian, 'indian': indian, 'breakfast': breakfast, 'desserts': desserts}

        for data in recipes_data:
            if Recipe.objects.filter(slug=data['slug']).exists():
                continue
            recipe = Recipe.objects.create(
                title=data['title'],
                slug=data['slug'],
                author=user,
                category=cat_map.get(data['category']),
                description=data['description'],
                prep_time=data['prep_time'],
                cook_time=data['cook_time'],
                servings=data['servings'],
                difficulty=data['difficulty'],
            )
            for i, (name, qty, unit) in enumerate(data['ingredients']):
                Ingredient.objects.create(recipe=recipe, name=name, quantity=qty, unit=unit, order=i)
            for i, instruction in enumerate(data['steps']):
                Step.objects.create(recipe=recipe, order=i + 1, instruction=instruction)
            self.stdout.write(self.style.SUCCESS(f'✅ Created recipe: {recipe.title}'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Seed complete! Run the server and enjoy ForkFolio.'))

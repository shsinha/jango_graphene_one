# cookbook/ingredients/schema.py
import graphene

from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    
    category = graphene.Field(CategoryType,
                                id=graphene.Int(),
                                name=graphene.String())
    
    all_categories = graphene.List(CategoryType)
    
    ingredient = graphene.Field(IngredientType,
                                  id=graphene.Int(),
                                  name=graphene.String())
          
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()
    
    def resolve_category(self, info, **kwargs):
        category_id = kwargs.get('id')
        name = kwargs.get('name')

        if category_id is not None:
            return Category.objects.get(pk=category_id)

        if name is not None:
            return Category.objects.get(name=name)

        return None
    
    def resolve_ingredient(self, info, **kwargs):
        ingredient_id = kwargs.get('id')
        name = kwargs.get('name')

        if ingredient_id is not None:
            return Ingredient.objects.get(pk=ingredient_id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None
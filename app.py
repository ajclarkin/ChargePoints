from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from util import filters
from datetime import date


username = "ajc"

app = Flask(__name__)
app.config['SECRET_KEY'] = b'&!rYjFO0sRe*4l8iYZh3IDYnguAn#!Gvo0gR'
app.jinja_env.filters['nl2br'] = filters.nl2br

# This is where the database stuff is
from models import *


def NormaliseQuantities(iList):
    newList = []



def RegenerateShoppingList(mealplanId):
    ShoppingList.query.delete()
    query = '''
        insert into shopping_list (mealplanId, ingredtxt, quantity, purchased, category)
        select
        :mpId
        , ingredients.ingredient
        , sum(meal_plan_recipes.quantity * recipe_ingredients.quantity / recipes.serves) as multiplied
        , 0
        , ingredients.category
        from meal_plan_recipes
        inner join recipe_ingredients on meal_plan_recipes.recipeId = recipe_ingredients.recipeId
        inner join ingredients on ingredients.id = recipe_ingredients.ingredientId
        inner join recipes on recipes.id = meal_plan_recipes.recipeId
        where meal_plan_recipes.mealplanId = :mpId
        group by ingredients.id
        '''

    db.session.execute(query, {'mpId': mealplanId})
    db.session.commit()

    

@app.route("/")
def Index():
    return render_template("index.html")


@app.route("/editrecipe", methods=['GET', 'POST'])
def EditRecipe():
    if request.method == 'POST':
        print("post")
        if request.form['submit'] == "method":
            entry = Recipes.query.filter_by(id=request.form['recipeId']).first()
            entry.serves = request.form['serves']
            entry.method = request.form['method']
            db.session.commit()
        

        else:
            print("else")
            if request.form['submit'] == "ingredient":
                entry = RecipeIngredients(recipeId=request.form['recipeId'], ingredientId=request.form['ingredientId'], quantity=request.form['quantity'])
                db.session.add(entry)
                db.session.commit()

            recipe = Recipes.query.filter_by(id=request.form['recipeId']).first()
            iList = RecipeIngredients.query.with_entities(RecipeIngredients.quantity, Ingredients.ingredient, Ingredients.category).filter_by(recipeId=request.form['recipeId']).join(Ingredients, RecipeIngredients.ingredientId == Ingredients.id).all()
            ingredients = Ingredients.query.all()
            return render_template("editRecipes.html", recipe=recipe, ingredients=ingredients, iList=iList)
        
    entries = Recipes.query.all()
    return render_template("buildMealList.html", entries=entries)






@app.route("/meals", methods=['GET', 'POST'])
def BuildMealList():
    if request.method == 'POST':
        if request.form['recipeId'] == "new":
            entry = Recipes(recipe=request.form['newrecipe'])
            db.session.add(entry)
            db.session.commit()
        else:
            return redirect(url_for('EditRecipe'), code=307)    # code 307 needed to redirect POST

    entries = Recipes.query.all()
    return render_template("buildMealList.html", entries=entries)



# This works and is finished
@app.route("/list/i")
def ListIngredients():
        iList = Ingredients.query.all()
        return render_template("listIngredients.html", iList=iList)

# @app.route("/list")
# @app.route("/list/r")
# def ListRecipes():
#         entries = Recipes.query.all()
#         return render_template("listRecipes.html", entries=entries)


# This works and is finished
@app.route("/ingredients", methods=['GET', 'POST'])
def AddIngredient():
    if request.method == 'POST':
        if request.form['category'] == "new":
            entry = Ingredients(ingredient=request.form['ingredient'], category=request.form['newcategory'], calories=request.form['calories'])
        else:
            entry = Ingredients(ingredient=request.form['ingredient'], category=request.form['category'], calories=request.form['calories'])
        
        db.session.add(entry)
        db.session.commit()
        
    ingredients = Ingredients.query.all()
    categories = Ingredients.query.with_entities(Ingredients.category).distinct()
    return render_template("ingredients.html", categories=categories, iList=ingredients)


# @app.route("/recipes")
# def ListRecipes():
#     # need a list of recipes which will link through to ViewRecipe()
#     entries = Recipes.query.all()
#     return render_template("listRecipes.html", entries=entries)


@app.route("/recipes", methods=['GET', 'POST'])
def ViewRecipe():
    # Might eventually want to change the url pattern here
    # Pattern should prevent enumerating recipes to view them, eg username, recipe title

    recipeId = request.form['recipeId']
    recipe = Recipes.query.filter_by(id=recipeId).first()
    if recipe:
        iList = RecipeIngredients.query.with_entities(RecipeIngredients.quantity, Ingredients.ingredient, Ingredients.category, Ingredients.calories).filter_by(recipeId=recipeId).join(Ingredients, RecipeIngredients.ingredientId == Ingredients.id).all()
        calories = 0
        for i in iList:
            calories += i.quantity * i.calories
        return render_template("viewRecipe.html", recipe=recipe, iList=iList, calories=calories)
    else:
        return redirect(url_for('Index'))



@app.route("/mealplan/create", methods=['GET', 'POST'])
def CreateMealPlan():
    if request.method == 'POST':
        entry = MealPlan(username=username, startDate=request.form['startDate'], defaultNo=request.form['defaultNo'])
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('EditMealPlan'), code=307)
    else:
        prevPlans = MealPlan.query.with_entities(MealPlan.id, MealPlan.startDate).filter_by(username=username).order_by(MealPlan.startDate.desc()).all()
        getDefault = MealPlan.query.with_entities(MealPlan.defaultNo).filter_by(username=username).order_by(MealPlan.id.desc()).first()
        return render_template("createMealPlan.html", defaultNo=getDefault, plans=prevPlans)



@app.route("/mealplan/edit", methods=['GET', 'POST'])
def EditMealPlan():
    if request.method == 'POST':
        if request.form['submit'] == 'newplan':
            defaultNo = request.form['defaultNo']
            mealplanId, startDate = MealPlan.query.with_entities(MealPlan.id, func.strftime('%d-%m-%Y', MealPlan.startDate)).filter_by(username=username, startDate=request.form['startDate']).first()
 
        elif request.form['submit'] == "addmeal":
            if MealPlan.query.with_entities(MealPlan.username).filter_by(id=request.form['mealplanId']).first().username == username:
                entry = MealPlanRecipes(mealplanId=request.form['mealplanId'], recipeId=request.form['recipeId'], quantity=request.form['quantity'], mealDate=request.form['mealDate'])
                db.session.add(entry)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    flash('That meal is already on the plan - if you want to change it delete the original first')

                mealplanId = request.form['mealplanId']
                defaultNo, startDate = MealPlan.query.with_entities(MealPlan.defaultNo, func.strftime('%d-%m-%Y', MealPlan.startDate)).filter_by(id=mealplanId).first()
            else:
                render_template("nopermission.html")

        else:
            # arrive here by picking a mealplan to edit
            mealplanId = request.form['submit']
            defaultNo, startDate = MealPlan.query.with_entities(MealPlan.defaultNo, func.strftime('%d-%m-%Y', MealPlan.startDate)).filter_by(id=mealplanId).first()


        recipes = Recipes.query.all()
        planMeals = MealPlanRecipes.query.with_entities(MealPlanRecipes.quantity, Recipes.recipe, MealPlanRecipes.id, func.strftime('%d-%m-%Y', MealPlanRecipes.mealDate)).filter_by(mealplanId=mealplanId).join(Recipes, MealPlanRecipes.recipeId==Recipes.id).all()
        return render_template("editMealPlan.html", recipes=recipes, planMeals=planMeals, defaultNo=defaultNo, startDate=startDate, mealplanId=mealplanId)

    else:
        return redirect(url_for('CreateMealPlan'))



@app.route("/mealplan", methods=['GET', 'POST'])
def ViewMealPlan():
    today = str(date.today())
    mealplanId = MealPlan.query.with_entities(MealPlan.id).filter(MealPlan.username==username, MealPlan.startDate<=today).order_by(MealPlan.startDate.desc()).first().id
    planMeals = MealPlanRecipes.query.with_entities(MealPlanRecipes.quantity, Recipes.recipe, MealPlanRecipes.recipeId, MealPlanRecipes.id, func.strftime('%d-%m-%Y', MealPlanRecipes.mealDate)).filter_by(mealplanId=mealplanId).join(Recipes, MealPlanRecipes.recipeId==Recipes.id).all()
    return render_template("viewMealPlan.html", planMeals=planMeals, mealplanId=mealplanId)



@app.route("/mealplan/delete", methods=['POST'])
def DeleteMealPlan():
    print(request.form['mealplanId'], request.form['mprId'])
    MealPlanRecipes.query.filter_by(id=request.form['mprId']).delete()
    db.session.commit()
    return



@app.route("/shoppinglist")
def DisplayShoppingList():
    mealplanId=1;

    # Every time we display the shopping list we regenerate it in the database in case of changes
    # This might be an issue if things are ticked off though

    RegenerateShoppingList(mealplanId)
    
    result = ShoppingList.query.join(MealPlan, ShoppingList.mealplanId==MealPlan.id).all()
    return render_template("listShoppingList.html", result=result)
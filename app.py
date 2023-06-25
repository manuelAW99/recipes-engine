from analysis import FoodGraph
import networkx as nx
from typing import List
import streamlit as st
from json import load, dump

st.set_page_config("Recipes Engine", page_icon="👨‍🍳", layout="wide")

with open("data/init.md") as fp:
    st.write(fp.read())

graph = FoodGraph(graphs_path='data/graphs/')

def save_substitutions(ingredient: str, substitutions: List[str]) -> None:
    subs = load(open("data/substitutions.json", 'r'))
    print(subs)
    if ingredient not in subs:
        subs[ingredient] = {}
    for ing in substitutions:
        if ing in subs[ingredient]:
            subs[ingredient][ing] += 1
        else:
            subs[ingredient][ing] = 1
    
    dump(subs, open("data/substitutions.json", "w"))
    st.balloons()

def get_recipes(graph: FoodGraph) -> List[str]:
    "See the ingredients by recipes"
    
    rel_graph = graph.recipe_ingredient_relationship_graph
    recipes = {node["label"]:node for node in rel_graph.nodes.values() if node["type"] == "recipe_name"}
    all_ingredients = [node["label"] for node in rel_graph.nodes.values() if node["type"] == "ingredient_name"]
    left, right = st.columns(2)
    with left:
        select_recipe = recipes[st.selectbox(f"Select recipe ({len(recipes)})", options=[recipe.capitalize() for recipe in recipes]).lower()]
        ingredients = [ing for ing in rel_graph.neighbors(select_recipe['label'])]
        st.write(f"### Ingredients for {select_recipe['label'].capitalize()}")
        for ingredient in ingredients:
            st.write(f"- {ingredient.capitalize()}")
    with right:
        select_ingredient = st.selectbox(f"Select an ingredient of this recipe ({len(ingredients)})", options=ingredients)
        result_ingredients = graph.replace_ingredient(select_ingredient)
        changes = st.multiselect(label="I can substitute this ingredient by ...", options=all_ingredients, key=ingredient)
        if changes:
            st.button("Send info", on_click=save_substitutions, kwargs=dict(ingredient=select_ingredient, substitutions=changes))
        if not result_ingredients:
            st.warning(f"No ingredients found to replace {select_ingredient}", icon="⚠️")
        else:
            st.write(f"#### You can substitute the {select_ingredient} for the following ingredients")
            for ingredient in result_ingredients:
                st.write(f"- {ingredient.capitalize()}")

def get_ingredients(graph: FoodGraph) -> List[str]:
    "Select recipes with a set of ingredients"
    
    rel_graph = graph.recipe_ingredient_relationship_graph
    ingredients = {node["label"]:node for node in rel_graph.nodes.values() if node["type"] == "ingredient_name"}
    select_ingredients = st.multiselect(f"Select a set of ingredients ({len(ingredients)})", options=ingredients)
    result_recipes = graph.recipes_with(select_ingredients)
    if not result_recipes:
        st.info(f"Please, select an ingredient", icon="ℹ️")
    else: 
        left, right = st.columns(2)
        with left:
            st.write("### Recipes")
            for recipe in result_recipes:
                st.write(f"- {recipe[0].capitalize()} *(with {recipe[1]} coincidences)*")
        with right:
            st.write("#### See the ingredients of a recipe")
            recipe = st.selectbox("Select a recipe", options=[rec[0].capitalize() for rec in result_recipes]).lower()
            for ing in rel_graph.neighbors(recipe):
                st.write(f"- {ing.capitalize()}")
            
def replace_an_ingredient(graph: FoodGraph) -> None:
    "Give a list of ingredients that can replace the one defined"
    
    rel_graph = graph.recipe_ingredient_relationship_graph
    ingredients = {node["label"]:node for node in rel_graph.nodes.values() if node["type"] == "ingredient_name"}
    select_ingredient = st.selectbox(f"Select an ingredient ({len(ingredients)})", options=ingredients)
    result_ingredients = graph.replace_ingredient(select_ingredient)
    if not result_ingredients:
        st.warning(f"No ingredients found to replace {select_ingredient}", icon="⚠️")
    else:
        st.write(f"### You can substitute the {select_ingredient} for the following ingredients")
        for ingredient in result_ingredients:
            st.write(f"- {ingredient.capitalize()}")


actions = {func.__doc__ : func for func in [get_recipes, get_ingredients, replace_an_ingredient]}
actions[st.selectbox("Select a functionaly", options=actions.keys())](graph=graph)





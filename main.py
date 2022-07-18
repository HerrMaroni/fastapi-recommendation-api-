import tensorflow as tf
import pandas as pd
from utils import compatible_colors
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

MODEL_PATH = './models/'
app = FastAPI()

origins = [
    "https://localhost:7260",
    "http://localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.saved_model.load(MODEL_PATH)
ASOS_DB = pd.read_csv('../../data/ASOS/asos_products_colors_categ_upd_wo_other.csv').astype({"id": int, "title": str,
      'image_url':str, 'type':str, 'brand':str, 'colour':str, 'gender':str, 'color_base':str, 'gen_category':str })

BASIC_OUTFIT = {'tops', 'bottom', 'shoes'}
ALLOWED_PRODUCTS = {'bottom', 'tops', 'outerwear', 'one-piece'}

class SelectedProduct(BaseModel):
    product_id: int
    color_palette: str = None
    top_k: int = None
    recommend_bags: bool = False
    recommend_jewelry: bool = False
    recommend_accessories: bool = False
    recommend_outerwear: bool = False
    recommend_underwear: bool = False
    recommend_headwear: bool = False

class OutfitRecommendation(BaseModel):
    outfit: list

class SimilarItemRecommendation(BaseModel):
    similar_items: list


def get_outfit_combination(product_cat: str, req: SelectedProduct):
    if product_cat not in ALLOWED_PRODUCTS:
        raise ValueError('{} is not allowed. Please choose another category.'.format(product_cat))

    garments_to_find = set()
    if req.recommend_bags is True:
        garments_to_find.add('bags')
    if req.recommend_jewelry is True:
        garments_to_find.add('jewelry')
    if req.recommend_accessories is True:
        garments_to_find.add('accessories')
    if req.recommend_outerwear is True:
        garments_to_find.add('outerwear')
    if req.recommend_headwear is True:
        garments_to_find.add('headwear')

    if product_cat == 'one-piece':
        garments_to_find.add('shoes')
        return garments_to_find
    if product_cat == 'underwear':
        print('underwear')
        # TODO: do what?
    # Basic outfit
    for x in BASIC_OUTFIT:
        if product_cat == x:
            continue
        garments_to_find.add(x)
    return garments_to_find



@app.post("/recommendOutfit", response_model=OutfitRecommendation)
def recommend_outfit(req: SelectedProduct):
    """
    Recommendation of clothing items that form an outfit.
    :return:
    """

    # TODO: add argument checks

    # 1. Get product category
    product = ASOS_DB.loc[ASOS_DB['id'] == req.product_id]
    prod_cat = product['gen_category'].values[0]

    # 2. Determine which parts of the outfit need to be found
    garments_to_find = get_outfit_combination(prod_cat, req)
    print(garments_to_find)

    # 3. Get matching colors
    product_color = product['color_base'].values[0]
    compat_colors = compatible_colors(req.color_palette, product_color)

    # 4. Get similar item recommendations
    final_outfit = [req.product_id]
    sim_item_ids, _ = model.call_item_item(tf.constant(req.product_id, dtype=tf.int32))

    # 5. Filter similar items based on category and color
    for item in sim_item_ids:
        item_id = tf.keras.backend.get_value(item)
        # get item color and category
        pr = ASOS_DB.loc[ASOS_DB['id'] == item_id]
        if pr.empty:
            print('Id {} not found in the data base'.format(item_id))
            continue
        recom_color = pr['color_base'].values[0]
        recom_cat = pr['gen_category'].values[0]

        # if color and category are compatible, add to outfit
        if recom_cat in garments_to_find and recom_color in compat_colors:
            garments_to_find.remove(recom_cat)
            final_outfit.append(int(item_id))

    ''' just for checking
    for i in final_outfit:
        p = ASOS_DB.loc[ASOS_DB['id'] == i]
        col = p['color_base'].values[0]
        cat = p['gen_category'].values[0]
        print(p, col, cat)
    print(final_outfit)'''

    return {"outfit": final_outfit}


@app.post("/recommendSimilarArticles", response_model=SimilarItemRecommendation)
def recommend_similar_articles(req: SelectedProduct):
    """
        Recommendation of items that are similar to each of the selected items.
        Does not do any outfit compatibility analysis.
    :return:
    """
    if req.top_k == 0:
        raise ValueError('Top_k should be >0')
    sim_item_ids, _ = model.call_item_item(tf.constant(req.product_id, dtype=tf.int32))
    top_k = [int(tf.keras.backend.get_value(item)) for item in sim_item_ids[0:req.top_k]] #[0:req.top_k]
    return {"similar_items": top_k}


@app.get("/")
def root():
    return {"message": "Please send a request to /recommendSimilarArticles or /recommendOutfit"}

"""
if __name__ == '__main__':
    product_cat = 'top'
    prod = SelectedProduct(product_id = 123, color_palette= 'Monochromatic', recommend_bags=True, recommend_headwear=True)
"""
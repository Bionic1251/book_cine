from flask import Flask
from flask import request
import json
import simplejson
import pandas as pd
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# init

# loading data
limited_tg_books = pd.read_csv("limited_tg_books.csv")
limited_tg_movies = pd.read_csv("limited_tg_movies.csv")
movies = pd.read_csv("movies.csv")
books = pd.read_csv("books.csv")

allowed_tags = pd.read_csv("allowed_tags.csv")
allowed_tags = set(allowed_tags[allowed_tags.include == 1].tag)

# limiting tag genome
#limited_tg_books = tg_books[tg_books.tag.isin(tg_movies.tag.unique())]
#limited_tg_movies = tg_movies[tg_movies.tag.isin(tg_books.tag.unique())]

# calculating vector length
def get_item_length_df(tg_df):
    len_df = tg_df.copy()
    len_df["length"] = len_df.score * len_df.score
    len_df = len_df.groupby("item_id")["length"].sum().reset_index()
    len_df["length"] = len_df["length"]**(1/2)
    return len_df

movie_len_df = get_item_length_df(limited_tg_movies)
book_len_df = get_item_length_df(limited_tg_books)

# initialized

def domain_rating_to_vectors(tg, domain_ratings, positive_rating_num, negative_rating_num):
    df = pd.DataFrame()
    for rating in domain_ratings:
        weight = rating[1]  # this is the weight of each rating
        if weight > 0:
            weight = weight / positive_rating_num
        else:
            weight = weight / negative_rating_num
        item = tg[tg.item_id == rating[0]].copy()
        item.score = item.score * weight  # we multiply item vector by the weight based on the rating
        df = pd.concat([df, item])  # we add the item vector to the dataframe
    return df

def get_rating_number(positive, ratings):
    return (get_domain_rating_number(positive, ratings["movies"]) +
            get_domain_rating_number(positive, ratings["books"]))

def get_domain_rating_number(positive, ratings):
    rating_num = 0
    for rating in ratings:
        if rating[1] > 0 and positive:
            rating_num += 1
        if rating[1] < 0 and not positive:
            rating_num += 1
    return rating_num

def get_user_profile(ratings):
    positive_rating_num = get_rating_number(True, ratings)
    negative_rating_num = get_rating_number(False, ratings)
    profile = domain_rating_to_vectors(limited_tg_movies, ratings["movies"], positive_rating_num, negative_rating_num)
    profile = pd.concat([profile, domain_rating_to_vectors(limited_tg_books, ratings["books"], positive_rating_num, negative_rating_num)])
    profile = profile.groupby("tag").score.sum().reset_index()
    return profile

def get_dot_product(profile, tg_df):
    tg_domain_profile = pd.merge(tg_df, profile, on="tag", how="inner")
    tg_domain_profile["dot_product"] = tg_domain_profile.score_x * tg_domain_profile.score_y
    dot_product_df = tg_domain_profile.groupby("item_id").dot_product.sum().reset_index()
    return dot_product_df

def get_sim_df(dot_product_df, len_df):
    sim_df = pd.merge(dot_product_df, len_df)
    sim_df["sim"] = sim_df["dot_product"] / sim_df["length"]
    return sim_df

def rank_candidate_items(profile, limited_tg, len_df):
    dot_product = get_dot_product(profile, limited_tg)
    sim_df = get_sim_df(dot_product, len_df)
    return sim_df

def extract_ids(ratings):
    ids = []
    for obj in ratings:
        ids.append(obj[0])
    return ids

def get_ratings(request_data):
    params = str(request_data)
    if params == "b''":
        params = 'b\'{"movies":[[2011,1]], "books":[]}\''
    return json.loads(params[2:-1])

def get_item_id(request_data):
    params = str(request_data)
    if params == "b''":
        params = 'b\'{"movies":[[2011,1]], "books":[]}\''
    return int(json.loads(params[2:-1]))

def get_recommendation(ratings, domain):
    profile = get_user_profile(ratings)

    limited_tg = None
    len_df = None
    items = None
    if domain == 'movies':
        len_df = movie_len_df
        limited_tg = limited_tg_movies
        items = movies
    else:
        len_df = book_len_df
        limited_tg = limited_tg_books
        items = books

    recs = rank_candidate_items(profile, limited_tg, len_df)
    rated_domain_items = extract_ids(ratings[domain])
    recs = recs[~recs.item_id.isin(rated_domain_items)]  # removing rated movies or books

    #item itself
    item_id = recs.sort_values(by="sim", ascending=False).head(1).to_dict(orient="tight")["data"][0][0]
    item_dict = items[items.item_id == item_id].to_dict()

    #item top topics
    item_top_topics = limited_tg[(limited_tg.item_id == item_id) & (limited_tg.tag.isin(allowed_tags))].sort_values(["score", "tag"], ascending=[False, False]).head(5).to_dict()

    # profile top topics
    profile_top_topics = profile[profile.tag.isin(allowed_tags)].sort_values(["score", "tag"], ascending=[False, False]).head(5).to_dict()

    data = {"item": item_dict, "item_topics": item_top_topics, "profile_topics": profile_top_topics}
    output = simplejson.dumps(data, ignore_nan=True)
    return output

def get_item(item_id, items, limited_tg):
    #finding the item
    item_dict = items[items.item_id == item_id].to_dict()

    #item top topics
    item_top_topics = limited_tg[(limited_tg.item_id == item_id)  & (limited_tg.tag.isin(allowed_tags))].sort_values(["score", "tag"], ascending=[False, False]).head(5).to_dict()

    data = {"item": item_dict, "item_topics": item_top_topics}
    output = simplejson.dumps(data, ignore_nan=True)
    return output


@app.route("/movie_recs", methods=['POST', 'GET'])
def get_movie_recs():
    ratings = get_ratings(request.data)
    print(ratings)

    movie_json = get_recommendation(ratings, "movies")
    return jsonify(movie_json)

@app.route("/book_recs", methods=['POST', 'GET'])
def get_book_recs():
    ratings = get_ratings(request.data)
    print(ratings)

    book_json = get_recommendation(ratings, "books")
    return jsonify(book_json)

@app.route("/movie", methods=['POST', 'GET'])
def get_movie():
    item_id = get_item_id(request.data)
    print(item_id)
    return jsonify(get_item(item_id, movies, limited_tg_movies))

@app.route("/book", methods=['POST', 'GET'])
def get_book():
    item_id = get_item_id(request.data)
    print(item_id)
    return jsonify(get_item(item_id, books, limited_tg_books))

@app.route("/", methods=['POST', 'GET'])
def hello():
    return "Hello, this is BookCine"

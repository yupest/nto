# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:19:17 2023

@author: yupes
"""
from flask import Flask, make_response, request, abort, Response, jsonify
# import json
import pandas as pd
from numpy import nan as np_nan
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def get_df(name):
    
    name = 'films' if name == 'movies' else name
    
    df = pd.read_csv(f'data/{name}.csv').fillna(np_nan).replace([np_nan], [None])
    df['code_2'] = df['code']
    df = df.set_index('code_2')
    
    return df

@app.route('/api/v1.0/movies', methods=['GET'])
@app.route('/api/v1.0/movies/', methods=['GET'])
@app.route('/api/v1.0/movies/<int:code>', methods=['GET'])
def get_movie(code=0):

    for k in request.args.keys():
        if not k in ['genre', 'country', 'offset']:
            abort(Response('Найден направильно заданный параметр', 404))

    df = get_df('movies')

    genre = request.args.get("genre")
    country = request.args.get("country")
    offset = request.args.get("offset")

    # num = None
    records = df.copy()

    # if offset and offset!='':
    #     try:
    #         num = ((int(offset) - 1) // 30 + 1) * 30
    #         records = records[num:num+30]
    #         result = {'offset':num,
    #                   'count_records':records.shape[0],
    #                   'count_movies':records['code'].unique().shape[0],
    #                   'records':records.to_dict(orient = 'records')}

    #         resp = make_response(json.dumps(result,ensure_ascii=False))
    #         resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    #         return resp
    #     except:
    #         pass

    if genre and genre!='':
        genre = genre.split(',')
        records = records.loc[records['Жанр'].isin([g.strip() for g in genre if g.strip()!=''])]

    if country and country!='':
        country = country.split(',')
        records = records.loc[records['Страна'].isin([c.strip() for c in country if c.strip()!=''])]

    if offset and offset!='':
        # num = ((int(offset) - 1) // 30 + 1) * 30
        # records = records[num:num+30]
        if not country and not genre:
            try:
                n = int(offset)
                if n < 0:
                    n = abs(n)
                num = ((n - 1) // 30 + 1) * 30
                records = records[num:num+30]
                result = {'offset':num,
                          'count_records':records.shape[0],
                          'count_movies':records['code'].unique().shape[0],
                          'records':records.to_dict(orient = 'records')}

                # resp = make_response(json.dumps(result,ensure_ascii=False).replace('NaN', 'null'))
                resp = make_response(jsonify(result))
                resp.headers['Content-Type'] = 'application/json; charset=utf-8'
                return resp
            except:
                pass
        else:
            abort(Response('При использовании offset не должны быть указаны другие параметры', 404))

    if records.shape[0] != df.shape[0]:
        result = {'genre':genre,
                  'country':country,
                #   'offset':num,
                  'count_records':records.shape[0],
                  'count_movies':records['code'].unique().shape[0],
                  'records':records.to_dict(orient = 'records')}

        # resp = make_response(json.dumps(result,ensure_ascii=False).replace('NaN', 'null'))
        resp = make_response(jsonify(result))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    else:
        if code == 0:
            code = random.choice(list(records.code.unique()))
            # resp = make_response(df.sample().to_json(orient = 'records', force_ascii=False))
            # # resp = make_response(jsonify(df.sample().to_json(orient = 'records')))
            # resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            # return resp
        if code in df.index:
            # resp = make_response(df.loc[code].to_json(orient = 'records', force_ascii=False))
            result = {'code':int(code),
                      'count_records':df.loc[code].shape[0],
                      'records':df.loc[code].to_dict(orient = 'records')}
            resp = make_response(jsonify(result) )
            resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            return resp
        else:
            abort(Response('Фильм не найден', 404))


@app.route('/api/v1.0/movies/genres', methods=['GET'])
@app.route('/api/v1.0/movies/genres/', methods=['GET'])
def get_moovies_genres():
    df = get_df('movies')

    resp = make_response(jsonify({'count_records':df['Жанр'].unique().shape[0],
				     'records':df['Жанр'].unique().tolist()}))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/api/v1.0/movies/countries', methods=['GET'])
@app.route('/api/v1.0/movies/countries/', methods=['GET'])
def get_moovies_countries():
    df = get_df('movies')

    resp = make_response(jsonify({'count_records':df['Страна'].unique().shape[0],
				     'records':df['Страна'].unique().tolist()}))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/api/v1.0/books', methods=['GET'])
@app.route('/api/v1.0/books/', methods=['GET'])
@app.route('/api/v1.0/books/<int:code>', methods=['GET'])
def get_books(code=0):

    for k in request.args.keys():
        if not k in ['genre', 'author', 'age']:
            abort(Response('Найден направильно заданный параметр', 404))

    df = get_df('books')
    records = df.copy()

    genre = request.args.get("genre")
    age = request.args.get("age")
    author = request.args.get('author')
    
    if genre and genre!='' and set(genre.split(',')).issubset(set(records['Жанр'])):
        genre = genre.split(',')
        records = records.loc[records['Жанр'].isin([g.strip() for g in genre if g.strip()!=''])]

    if age and age!='' and set(age.split(',')).issubset(set(records['Возраст'].astype(str))):
        age = age.split(',')
        records = records.loc[records['Возраст'].isin([int(c.strip()) for c in age if c.strip()!=''])]
        
    if author and author!='' and set(author.split(',')).issubset(set(records['Автор'])):
        author = author.split(',')
        records = records.loc[records['Автор'].isin([c.strip() for c in author if c.strip()!=''])]
        
    if records.shape[0] != df.shape[0]:
        
        
        result = {'genre':genre,
                   'age':age if not age else [int(a) for a in age],
                   'author': author,
                  'count_records':records.shape[0],
                  'count_books':records['code'].unique().shape[0],
                  'records':records.to_dict(orient = 'records')}

        # resp = make_response(json.dumps(result,ensure_ascii=False).replace('NaN', 'null'))
        resp = make_response(jsonify(result))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

    elif not genre and not age and not author:
        if code == 0:
            code = random.choice(list(records.code.unique()))
            # resp = make_response(jsonify(df.sample().to_json(orient = 'records')))
            
        if code and code in records.index:
            result = {'code':int(code),
                      'count_records':records.loc[code].shape[0],
                      'records':records.loc[code].to_dict(orient = 'records')}
            resp = make_response(jsonify(result) )
            resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            return resp
    else:
        abort(Response('Книга(и) не найдена(ы)', 404))

@app.route('/api/v1.0/books/get', methods=['GET'])
@app.route('/api/v1.0/books/get/', methods=['GET'])
def get_books_offset():
    df = get_df('books')
    end = request.args.get("end")
    for k in request.args.keys():
        if k != 'end':
            abort(Response('Найден направильно заданный параметр', 404))
            
    offsets = ['526c77e039deee1fee00d08589b1763d',
     'c4793b4ed228be975c758a70bc9a17ad',
     'e00ba4d4dec89a2afcdc958a26f1fff0',
     '185b6f08a18fdb8be4f83511bcd93817',
     'd4a9e96b32e0e26c063609746ae3348f',
     '49cf1e080942bd8195b885cb01dc5199',
     'b7a023922e8721e483aee8a676385080',
     '130174bfca84255ab8e0171edab792b9',
     'e56ada52f4e38d2b8f37179bc91f2c2d',
     '5f2b466332307acf3b13a389ee257bad',
     'dc909df63ff64ffd36c1cce455d1a29e',
     'cb70b20312e81b59b2cf829f84a28474',
     None]
    if not end:
        result = {'end':offsets[0],
                  'count_records':df[:20].shape[0],
                  'count_books':df[:20]['code'].unique().shape[0],
                  'records':df[:20].to_dict(orient = 'records')}

        # resp = make_response(json.dumps(result,ensure_ascii=False).replace('NaN', 'null'))
        resp = make_response(jsonify(result))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp
    elif end and end in offsets:
        offset = (offsets.index(end)+1)*20
        
        records = df[offset:offset+20]
        
        result = {'end':offsets[offsets.index(end)+1],
                  'count_records':records.shape[0],
                  'count_books':records['code'].unique().shape[0],
                  'records':records.to_dict(orient = 'records')}

        # resp = make_response(json.dumps(result,ensure_ascii=False).replace('NaN', 'null'))
        resp = make_response(jsonify(result))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp
        
    else:
        abort(Response('Книга(и) не найдена(ы)', 404))
        
@app.route('/api/v1.0/books/genres', methods=['GET'])
@app.route('/api/v1.0/books/genres/', methods=['GET'])
def get_books_genres():
    df = get_df('books')

    resp = make_response(jsonify({'count_records':df['Жанр'].unique().shape[0],
				     'records':df['Жанр'].unique().tolist()}))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/api/v1.0/books/ages', methods=['GET'])
@app.route('/api/v1.0/books/ages/', methods=['GET'])
def get_books_ages():
    df = get_df('books')

    resp = make_response(jsonify({'count_records':df['Возраст'].unique().shape[0],
				     'records':df['Возраст'].unique().tolist()}))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@app.route('/api/v1.0/books/authors', methods=['GET'])
@app.route('/api/v1.0/books/authors/', methods=['GET'])
def get_books_authors():
    df = get_df('books')

    resp = make_response(jsonify({'count_records':df['Автор'].unique().shape[0],
				     'records':df['Автор'].unique().tolist()}))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp

if __name__ == '__main__':
    app.run(debug=True)
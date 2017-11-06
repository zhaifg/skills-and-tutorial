#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-06 17:07:00
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me
# @Version : $Id$

# 对文章进行投票, 条件
# 1. 如果一篇文章或得了至少200支持票(up vote), 那么网站就认为这篇文章有趣
# 2. 加入这个网站每天发布1000篇, 而七种的50篇符合网站对有趣的要求,  那么网站要做的就是把这50篇放到文章列表前
#    100位一天
# 计算评分时于支持票数量相乘的常量是 432

# 构建文章投票网站除了需要计算文章评分外, 还需要使用redis 结构存储网站上的各种信息. 对于
# 网站里的每篇文章, 程序都使用一个散列来存储文章的标题, 指向文章的网址, 发布文章的用户, 文章的发布时间, 文件得到
# 的投票数量等


# 使用两个有序集合来有序的存储文章
# 1. 文章ID , 分值为 发布时间, score: zset article: 1100x  13232323
# 2. 文章ID, 分值为文章的评分 score: zset  article:1000x 123432323

# 为防止用户多次投票, 则记录每篇文章已投票的用户名单 voted:articleID user:userID 使用SET
# 一周后 删除

import time
import redis

ONE_WEEK_IN_SECONDS = 60 * 60 * 24 * 7
VOTE_SCORE = 432

ARTICLES_PER_PAGES = 25


def article_vote(conn, user, article):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return

    article_id = article.partition(':')[-1]
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('socre:', article, VOTE_SCORE)
        conn.hincrby(article, 'votes', 1)


# 发布一篇新文章
def post_article(conn, user, title, link):
    article_id = str(conn.incr('article:'))

    voted = 'voted:' + article_id
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    not = time.time()
    article = 'article:' + article_id
    conn.hmset(
        article, {
            'title': title,
            'link': link,
            'poster': user,
            'time': now,
            'votes': 1,
        }
    )
    conn.zadd('score:', article, now + VOTE_SCORE)
    conn.zadd('time:', article, now)
    return article_id


def get_articles(conn, page, order='score:'):
    start = (page - 1) * ARTICLES_PER_PAGES
    end = start + ARTICLES_PER_PAGES - 1

    ids = conns.zrevrange(order, start, end)
    articles = []

    for id in ids:
        article_data = conn.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)
    return articles

# 群组


def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn, group, page, order='score:'):
    key = order + group
    if not conn.exist(key):
        conn.zinterstore(key,
                         ['group:' + group, order],
                         aggregate='max'
                         )
        conn.expire(key, 60)
    return get_articles(conn, page, key)

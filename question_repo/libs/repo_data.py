"""
@file:repo_data.py
@author:李霞丹
@date：2019/08/14
"""
from apps.repo.models import Answers, User, Questions
from django.db.models import Count


def recent_user():
    """最近刷题的同学"""
    # 按用户统计刷题的数量（新近刷的在后面）
    result = Answers.objects.values_list('user').annotate(Count('id'))
    # 从后取最新的10个用户
    user_id_list = [item[0] for item in result][-10:]
    userlist = User.objects.filter(id__in=user_id_list)
    return userlist


def user_answer_data(user):
    # 答题数量及总量
    # count=> 计数
    answer_num = Answers.objects.filter(user=user).count()
    question_all = Questions.objects.all().__len__()
    # 用户总量
    user_sum = User.objects.all().__len__()
    # 答题情况
    # 每个用户答题数量:按用户统计答题数量
    rank = Answers.objects.values('user').annotate(Count('id'))
    # <QuerySet [{'user': 1, 'id__count': 1}, {'user': 2, 'id__count': 1}, {'user': 3, 'id__count': 2}]>
    # print(rank) 按答题量排序
    rank = sorted(rank, key=(lambda item: item["id__count"]), reverse=True)

    # 统计每个人的排名(为提升效率，可写入memcache)
    rank_dict = {}
    # 当前排名
    cur_rank = 0
    # 刷题数量
    cur_count = 0
    for index, item in enumerate(rank, start=1):
        # 如果上一名的刷题数据与自己不一样，则更新排名（否则跟上一名同名次）
        if cur_count != item["id__count"]:
            cur_rank = index
        cur_count = item["id__count"]
        rank_dict[item["user"]] = dict(item, **{"rank": cur_rank})
    # print(rank_dict)
    kwgs = {
        "answer_num": answer_num,
        "question_all": question_all,
        "user_sum": user_sum,
        "rank": rank_dict[user.id] if answer_num else {"rank": 0, },
    }
    return kwgs
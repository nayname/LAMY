import collections
import itertools
import json
import os
import random
import shutil
import sys
import time
import urllib
from copy import copy
from pathlib import Path
from urlextract import URLExtract

import psycopg2

from app.validator import Validator
from config.config import courses
from lib.parse_code import parse_json, compile_request
from lib.query import proceed_query, send_request
from helper import get_submitted, overall_analysis_from_dataset, create_dataset, iterate_over_db, \
    report, get_overall, get_name, get_dataset_report

lessons = []

make_groups = (...)

rules_from_errors = ...


def get_all_lesson(works, type, sample):
    examples = {}

    ...
    return examples


def get_works(dir, errors_qouta, normals_qouta, criterias):
    new_data = {"normal": [], "errors": []}

    ...


    return new_data


def create_groups(id, conn, version):
    ...

    for k in groups.keys():
        conf_trained[id][k]["classes"]["pos"] = {}
        conf_trained[id][k]["classes"]["neg"] = {}

        for j in groups[k]:
            ...

            if 'pos' in groups[k][j]['type']:
                conf_trained[id][k]["classes"]["pos"][groups[k][j]["description"]] = j + ":bool"
            else:
                conf_trained[id][k]["classes"]["neg"][groups[k][j]["description"]] = j + ":bool"

    f_ = open('config/config_all.json', "w")
    f_.write(json.dumps(conf_trained))

    return True


def make_placeholder(lecture, conn):
    descr = ""

    f = open('config/config_all.json')
    conf_trained = json.load(f)

    if lecture not in conf_trained.keys():
        ...

    with open('config/config_all.json', 'w') as f:
        json.dump(conf_trained, f)
    f.close()


def set_new(id, conn, version, with_tutor=True):
    dir = "../works/" + id

    works = get_works(dir, 25, 100, [])

    with open(dir + '/works.json', 'w') as f:
        json.dump(works, f)

    f = open('config/config_all.json')
    conf_trained = json.load(f)

    cur = conn.cursor()

    t = []
    num = 1
    ...

    normals = get_all_lesson(works, "normal", 100)
    errors = get_all_lesson(works, "errors", 50)

    ...

    for i in errors.keys():
        ...


def get_classifying_queries(id, conn, version):
    ...

def run_over_flow(l, limit, version):
    query =  ...

    static_check(query, version, lectures, out_of_scope_course)
    get_submitted(l)


def set_type(param, lecture, conn):
    ...


def exists_type(lecture):
    ...

    if ...:
        return True
    else:
        return False


def exists_comments(lecture):
    ...

    if ...:
        return True
    else:
        return False


def get_data_type(lecture, conn):
    if not exists_type (lecture):
        ...


def get_lectures(conn, thread, stage):
    cur = conn.cursor()
    res = []

    if stage == 'first':
        ...
    else:
        ...

    print(cur.query, cur.rowcount)
    for i in cur.fetchall():
            res.append(i[0])
    return res

def fill_configs(conn, l, chosen):
    cur = conn.cursor()
    f = open('config/config_all.json')
    conf_trained = json.load(f)

    ids = []

    for c in conf_trained.keys():
        insert_query = ...


f = open('report.json')
rprt = json.load(f)

f = open('variants.json')
variants = json.load(f)

def score(param):
    if param['not_passed']['count_unmatched'] > ((param['not_passed']['count']/10) * 3):
        param['score'] = -2
    elif param['perfect']['count_matched'] < ((param['perfect']['count']/10) * 3):
        param['score'] = -1
    else:
        param['score'] = param['perfect']['count_matched'] + (5 * param['not_passed']['count_matched'])
    return param


def store_variants(report, l, version, conn):
    classes = []
    output = {}
    f = open('config/config_all.json')
    conf_trained = json.load(f)

    cur = conn.cursor()

    ...

    for L in range(len(classes) + 1):
        for subset in itertools.combinations(classes, L):
            res = score(get_dataset_report(conn, l, version, list(subset)))

            if res['score'] not in output.keys():
                output[res['score']] = []
            output[res['score']].append(
                {"rows": res["rows"], "perfect": res["perfect"], "passed": res["passed"],
                 "not_passed": res["not_passed"], "subset":subset, str(res['not_passed']['count_unmatched'])+", "+str(res['perfect']['count_matched'])+", "+str(len(subset)):"label"})
            insert_query = ...


def choose_variant(variants, l, conn):
    max = 0
    chosen = None

    for k in variants[l].keys():
        if int(k) > 0 and int(k) > int(max):
            chosen = variants[l][k][0]['subset']
            max = k

    if chosen is not None:
        ...

    return chosen


def base_report(rprt, conn):
    cur = conn.cursor()

    for r in rprt.keys():
        insert_query = ...



def get_version(l, conn, flag=None):
    ...

    return version


def update_chosen(variants):
    for l in variants.keys():
        version = get_version(l, conn)

        max = 0
        chosen = None

        for k in variants[l].keys():
            if int(k) > 0 and int(k) > int(max):
                chosen = variants[l][k][0]['subset']
                max = k

        for k in variants[l].keys():
            for i in variants[l][k]:
                res = i
                if chosen == res['subset']:
                    insert_query = (...)



def first_part(thread):
    lectures = get_lectures(conn, thread, 'first')

    for lecture in lectures:
        get_data_type(lecture, conn)
        make_placeholder(lecture, conn)

        version = get_version(lecture, conn, "update")

        if not exists_comments(lecture):
                ...

                set_new(lecture, conn, version)

                get_classifying_queries(lecture, conn, version)

        try:
            ...

            create_groups(lecture, conn, version)

            create_dataset(lecture, 20, version, conn)

            get_submitted(lecture, True)
            overall_analysis_from_dataset(lecture, version)
            print("variants:", lecture)

            store_variants(variants, lecture, version, conn)
            chosen = choose_variant(variants, lecture, conn)
            fill_configs(conn, lecture, chosen)
            ...
        except Exception as e:
            ...

    ...



def second_part(thread):
    lectures = get_lectures(conn, thread, 'second')

    for l in lectures:
        version = get_version(l, conn)
        run_over_flow(l, 50, version)

    courses = set()

    for l in lectures:
        version = get_version(l, conn)
        res = report(l, version, conn)
        if res[1] not in rprt.keys():
            rprt[res[1]] = {}
        rprt[res[1]].update(res[0])
        courses.add(res[1])

    get_overall(rprt, courses, conn)
    base_report(rprt, conn)

    with open('report.json', 'w') as f:
        json.dump(rprt, f)


if 'first' in sys.argv[1]:
    first_part(sys.argv[2])
elif 'second' in sys.argv[1]:
    second_part(sys.argv[2])



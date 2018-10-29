#!/usr/bin/env python

import os
import time
import threading
import traceback
import pprint
import dateutil.parser
import shutil

from datetime import datetime
from dateutil import tz
from tkinter import *

from yattag import Doc

import init
import api_calls as api


def iso8601_to_local_time(time):
    #timezones
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    return str(dateutil.parser.parse(time).replace(tzinfo=from_zone).astimezone(to_zone))[:-6]

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def find_replies(arr,rep,dis):
    without_replies = without_keys(rep,'replies')
    without_replies['discussion_title'] = dis['title']
    without_replies['discussion_url'] = dis['url']
    arr.append(without_replies)
    if 'replies' in rep:
        for more_rep in rep['replies']:
                find_replies(arr,more_rep,dis)

def find_replies_group(arr,rep,dis,group):
    without_replies = without_keys(rep,'replies')
    without_replies['discussion_title'] = dis['title']
    without_replies['discussion_url'] = dis['url']
    without_replies['group_title'] = group['title']
    without_replies['group_url'] = group['url']
    arr.append(without_replies)
    if 'replies' in rep:
        for more_rep in rep['replies']:
                find_replies_group(arr,more_rep,dis,group)


def scrape_discussions():
    discussions = api.get_all_discussions()

    print('The number of discussion we have: ' + str(len(discussions)))


    master_list = []

    #find all participants in all discussions
    for discussion in discussions:
        participants = []
        print("Discussion title: " + discussion['title'])

        #check if its group discussion or not
        group_category_id = discussion.get('group_category_id', None)
        if group_category_id is not None:
            group_topic_children = discussion['group_topic_children']
            for group_topic_child in group_topic_children:
                topic_info_group = api.get_full_topic_group_discussion(group_topic_child['group_id'], group_topic_child['id'])
                grab_participants = topic_info_group.get('participants',None)
                if grab_participants is not None:
                    participants = topic_info_group['participants']
                    for participant in participants:
                        new_participant = {}
                        new_participant['id'] = participant['id']
                        new_participant['name'] = participant['display_name']
                        new_participant['entries'] = []
                        if new_participant not in master_list:
                            master_list.append(new_participant)
                    
                else:
                    continue
        else:
            topic_info = api.get_full_topic(discussion['id'])
            participants = topic_info['participants']
            for participant in participants:
                new_participant = {}
                new_participant['id'] = participant['id']
                new_participant['name'] = participant['display_name']
                new_participant['entries'] = []
                if new_participant not in master_list:
                    master_list.append(new_participant)
    

    #find all discussions
    for discussion in discussions:
        flattened_replies = []

        #grabs all the entries from group discussion
        group_category_id = discussion.get('group_category_id', None)
        if group_category_id is not None:
            group_topic_children = discussion['group_topic_children']
            for group_topic_child in group_topic_children:
                flattened_replies_group = []
                topic_info = api.get_full_topic_group_discussion(group_topic_child['group_id'], group_topic_child['id'])
                group_info = api.get_group_discussion(group_topic_child['group_id'], group_topic_child['id'])
                grab_view = topic_info.get('view',None)
                if grab_view is not None:
                    for elem in topic_info['view']:
                        find_replies_group(flattened_replies_group,elem,discussion,group_info)

                    #remove deleted entries                
                    for entry in flattened_replies_group:
                        entry_delete = entry.get('deleted', None)
                        if entry_delete is not None:
                           flattened_replies_group.remove(entry)

                    #tying entries to masterlist's names
                    for entry in flattened_replies_group:
                        for entry2 in master_list:
                            entry_user_id = entry.get('user_id', None)
                            if entry_user_id is not None and entry['user_id'] == entry2['id']:
                                entry2['entries'].append(entry)


        else:
            #grabs all the entries from graded discussion
            topic_info = api.get_full_topic(discussion['id'])


            for elem in topic_info['view']:
                find_replies(flattened_replies,elem,discussion)

            #remove deleted entries                
            for entry in flattened_replies:
                entry_delete = entry.get('deleted', None)
                if entry_delete is not None:
                   flattened_replies.remove(entry)

            #tying entries to masterlist's names
            for entry in flattened_replies:
                for entry2 in master_list:
                    entry_user_id = entry.get('user_id', None)
                    if entry_user_id is not None and entry['user_id'] == entry2['id']:
                        entry2['entries'].append(entry)


    current_directory = os.getcwd()
    pprint.pprint(current_directory)
    final_directory = os.path.join(current_directory, init.course_name)
    pprint.pprint(final_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


    for person in master_list:
        person_name = person['name']
        person_id = person['id']
        person_entries = person['entries']
        person_url = '{}/courses/{}/users/{}'.format(init.base_url,init.course_id,person_id)

        doc, tag, text = Doc().tagtext()
        with tag('html', lang="en"):
            with tag('head'):
                with tag('body'):
                    with tag('h1'):
                        text(person_name)
                    with tag('p'):
                        with tag('strong'):
                            text("Total Number of Entries: ")
                        text(str(len(person_entries)))
                    with tag('p'):
                        with tag('strong'):
                            text("User Profile: ")
                        with tag('a', href=person_url):
                            text(person_url)
                    for entry in person_entries:
                        discussion_title = entry["discussion_title"]
                        discussion_link = entry["discussion_url"]
                        posted_at = iso8601_to_local_time(entry["created_at"])
                        updated_at = entry['updated_at']
                        entry_message = entry["message"]
                        attachments = entry.get('attachments',None)
                        group_title = entry.get('group_title',None)
                        group_url = entry.get('group_url',None)
                        with tag('div'):
                            doc.attr(style = "border:2px solid black; padding: 5px 5px")
                            with tag('p'):
                                with tag('strong'):
                                    text("From Discussion: ")
                                text(discussion_title)
                            with tag('p'):
                                with tag('strong'):
                                    text("Discussion Link: ")
                                with tag('a', href=discussion_link):
                                    text(discussion_link)
                            if group_title is not None:
                                with tag('p'):
                                    with tag('strong'):
                                        text("From Group: ")
                                    text(group_title)
                            if group_url is not None:
                                with tag('p'):
                                    with tag('strong'):
                                        text("Group Link: ")
                                    with tag('a', href=group_url):
                                        text(group_url)
                            with tag('p'):
                                with tag('strong'):
                                    text("Posted at: ")
                                text(posted_at)
                            with tag('p'):
                                with tag('strong'):
                                    text("Attachments: ")
                                if attachments is not None:
                                    for attachment in attachments:
                                        with tag('a', href=attachment['url']):
                                            text(attachment['display_name'])
                                else:
                                    text('None')
                            with tag('p'):
                                with tag('strong'):
                                    text("Entry Message: ")
                                if entry_message:
                                    with tag('div'):
                                        doc.attr(style = "border:1px solid black; padding: 5px 5px")
                                        doc.asis(entry_message)
                                else:
                                    text("None")

                        doc.stag('br')

        with open('{} ({}).html'.format(person_name,person_id), 'wb') as file:
            file.write(doc.getvalue().encode("utf-8"))

        shutil.move(current_directory + '//{} ({}).html'.format(person_name,person_id), final_directory + '//{} ({}).html'.format(person_name,person_id))





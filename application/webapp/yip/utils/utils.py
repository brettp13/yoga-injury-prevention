"""
General utilities for the YIP project
"""


import os
import json

from conditions.models import Condition
from conditions.serializers import ConditionSerializer
from user_profiles.models import SearchEntry, UserProfile
from yogaposes.models import BeneficialPoses, YogaPose
from yogaposes.serializers import YogaPoseSerializer


def create_email_wrapper(func):
    """
    The create_email function should only run in prod.
    """
    def function_wrapper(recipient, subject, body, email_type):
        if os.environ.get('ENV', None):
            func(recipient, subject, body, email_type)
        else:
            print("\nApplication is running in local environment.", flush=True)
            print("Faking it. create_email function not actually called.\n", flush=True)

    return function_wrapper


def add_to_mail_list_wrapper(func):
    """
    The add_to_mail_list function should only run in prod.
    """
    def function_wrapper(email, fname, lname, list_name):
        if os.environ.get('ENV', None):
            func(email, fname, lname, list_name)
        else:
            print("\nApplication is running in local environment.", flush=True)
            print("\nFaking it. add_to_mail_list function not actually called.\n", flush=True)

    return function_wrapper


def increment_searches(user, yogapose=None, conditions=None, search_type=None):
    """
    Increment the number of queries for the given user by 1,
    and create a search entry object.
    """
    user_profile = UserProfile.objects.get(user=user)
    user_profile.number_of_queries += 1
    user_profile.save()

    if yogapose:
        search_criteria = yogapose.sanskrit_name
        search_type = 'by pose'
    elif conditions:
        search_criteria = ''
        for condition_id in conditions:
            condition = Condition.objects.get(id=condition_id)
            search_criteria += '%s ' % condition.name
    else:
        print('No pose or condition passed in!', flush=True)

    search_entry = SearchEntry.objects.create(
            profile=user_profile, search_criteria=search_criteria, search_type=search_type)


def increment_logins(user):
    """
    Increment the number_of_logins by 1
    """
    user_profile = UserProfile.objects.get(user=user)
    user_profile.number_of_logins += 1
    user_profile.save()


def get_conditions_searched(condition_ids):
    """
    Takes a list of condition ids, and returns a list of condition
    objects
    """
    conditions = []

    for id in condition_ids:
        condition = Condition.objects.get(id=id)
        conditions.append(condition)

    return conditions


def get_contraindicated_poses(condition_ids):
    """
    Takes a list of condition ids. Returns a list of poses that are
    contraindicated for one or more of the given conditions, and a 
    list of condition objects corresponding to ids passed in.
    """
    contraindicated_poses = []

    conditions = get_conditions_searched(condition_ids)

    for condition in conditions:
        poses_contraindicated = YogaPose.objects.filter(
            contraindicated_conditions__name__in=[condition]).distinct()

        for pose in poses_contraindicated:
            contraindicated_poses.append(pose)

    return list(dict.fromkeys(contraindicated_poses))


def remove_contraindicated_poses(poses, contraindicated_poses):
    """
    Takes two lists, one list consisting of all the poses that are
    contraindicated, and one containing poses that are either
    beneficial, or safe.

    Returns a single list consisting of the set of poses that exist
    in the benefifical/safe list, but not in the contraindicated list.
    """
    return set([x for x in poses if x not in contraindicated_poses])


def get_beneficial_poses(condition_ids):
    """
    Return a list of poses that are beneficial for the given conditions
    """
    beneficial_poses = []

    # Assemble conditions searched
    conditions = get_conditions_searched(condition_ids)
    condition_serializer = ConditionSerializer(conditions, many=True)

    # Assemble contraindicated poses
    contraindicated_poses = get_contraindicated_poses(condition_ids)

    # Assemble beneficial poses
    for condition in conditions:
        beneficial_poses_mapper = BeneficialPoses.objects.filter(
            condition=condition)

        if len(beneficial_poses_mapper) > 0:
            poses = beneficial_poses_mapper[0].poses.all()
        else:
            # need to set this empty so we don't fail when none exist
            poses = []
        
        for pose in poses:
            beneficial_poses.append(pose)

        # Make sure no beneficial poses are contraindicated for any searched conditions
        beneficial_poses = list(remove_contraindicated_poses(
            poses=beneficial_poses, contraindicated_poses=contraindicated_poses))

    pose_serializer = YogaPoseSerializer(beneficial_poses, many=True)
    condition_serializer = ConditionSerializer(conditions, many=True)
    
    return pose_serializer.data, condition_serializer.data


def get_indicated_poses(condition_ids):
    """
    Return a dictionary of yogaposes beneficial to the conditions searched
    and the condition(s) they are beneficial for.

    Return a list of serialized conditions that were searched.
    """
    pose_and_conditions_benefitted = []
    returned_searched_conditions = []

    # assemble contraindicated poses
    all_the_contraindicated_poses = get_contraindicated_poses(condition_ids)

    # assemble conditions searched
    conditions_searched = get_conditions_searched(condition_ids)

    # assemble beneficial poses
    for condition in conditions_searched:
        poses_beneficial = []
        beneficial_poses_mapper = BeneficialPoses.objects.filter(
            condition=condition)

        if len(beneficial_poses_mapper) > 0:
            beneficial_poses = beneficial_poses_mapper[0].poses.all()
        else:
            beneficial_poses = []

        for pose in beneficial_poses:
            poses_beneficial.append(pose)

        # Make sure none of the beneficial poses exist in the list of
        # contraindicated poses
        poses_beneficial = remove_contraindicated_poses(
            poses=poses_beneficial, contraindicated_poses=all_the_contraindicated_poses)

        # combine each pose with the condition(s) it benefits
        for pose in poses_beneficial:
            serializer = YogaPoseSerializer(pose)
            conditions_benefitted = []
            pose_to_condition_mapper = BeneficialPoses.objects.filter(
                poses=pose)

            for relation in pose_to_condition_mapper:
                condition_benefitted = relation.condition
                conditions_benefitted.append(condition_benefitted)

                # Remove all conditions from conditions_benefitted that
                # were not referenced in the search
                for c in conditions_benefitted:
                    if c not in conditions_searched:
                        conditions_benefitted.remove(c)

                c_serializer = ConditionSerializer(
                        conditions_benefitted, many=True)

                print('After json_dumps : %s' % json.dumps(c_serializer.data), flush=True)

            # serialize and return pose with the conditions it benefits
            pose_and_conditions_benefitted.append(
                    {'yoga_pose': serializer.data,
                     'conditions_benefitted': json.dumps(c_serializer.data)})

    # Assemble conditions searched in json form
    for condition in conditions_searched:
        serializer = ConditionSerializer(condition)
        returned_searched_conditions.append(serializer.data)

    return pose_and_conditions_benefitted, returned_searched_conditions


def get_safe_poses(condition_ids):
    """
    Return a list of yogaposes that are safe for the given conditions.
    """
    # assemble conditions searched
    conditions = get_conditions_searched(condition_ids)
    
    condition_serializer = ConditionSerializer(conditions, many=True)

    # assemble contraindicated poses
    contraindicated_poses = get_contraindicated_poses(condition_ids)

    # remove contraindicated poses to return a list of safe poses
    all_poses = YogaPose.objects.all()
    safe_poses = remove_contraindicated_poses(
        poses=all_poses, contraindicated_poses=contraindicated_poses)

    return safe_poses, condition_serializer.data

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import generics

from .serializers import *
from .models import *

import ipfsApi


class MembersListView(APIView):
    """
    Provides a get method handler.
    """

    def get(self, requset):
        queryset = Member.objects.all()
        serializer = MemberSerializer(queryset, many=True)
        return Response(serializer.data)


class MemberView(APIView):
    """
    Provides a get method handler.
    """

    def get(self, request, MemberID):
        queryset = Member.objects.get(MemberID=MemberID)
        serializer = MemberSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, MemberID=None):
        if MemberID is None:
            data = json.loads(request.body)
            serializer = MemberSerializer(data=data['member_data'])
            if serializer.is_valid():
                member_saved = serializer.save()
                return Response({"success": "Member {} created successfully".format(data['member_data']['MemberID'])})
            return Response({"failed": "Member {} NOT created!!!".format(data['member_data']["MemberID"])})
        else:
            pass

        return Response({"done": True})


class AddEpisode(APIView):
    def post(self, request):
        data = json.loads(request.body)['episode_data']
        data['HistoryHash'] = None

        if Member.objects.filter(pk=data['member']).exists():
            if Episode.objects.filter(pk=data['Episode_ID']).exists():
                return Response({"failed": "Episode {} already exists!!!".format(data["Episode_ID"])})
            else:
                serializer = EpisodeSerializer(data=data)
                if serializer.is_valid():
                    episode_saved = serializer.save()
                    return Response({"success": "Episode {} created successfully".format(data['Episode_ID'])})
                return Response({"failed": "Episode {} NOT created!!!".format(data["Episode_ID"])})


def add_encounter_util(encounter_data, Klass, KlassSerializer, tag=''):
    ret = {}

    if Episode.objects.filter(pk=encounter_data['episode']).exists():
        if Klass.objects.filter(pk=encounter_data['Encounter_ID']).exists():
            ret['{}_encounters'.format(tag)] = {
                "failed": "{} Encounter {} already exists!!!".format(tag, encounter_data["Encounter_ID"])}
            return ret, False
        else:
            serializer = KlassSerializer(data=encounter_data)
            if serializer.is_valid():
                episode_saved = serializer.save()
                ret['{}_encounters'.format(tag)] = {
                    "success": "{} Encounter {} created successfully".format(tag, encounter_data['Encounter_ID'])}
            else:
                ret['{}_encounters'.format(tag)] = {
                    "failed": "{} Encounter {} NOT created!!!".format(tag, encounter_data["Encounter_ID"])}
                return ret, False

    return ret, True


class AddEncounter(APIView):
    def post(self, request):
        data = json.loads(request.body)['encounter_data']

        medical_encounters_data = data.pop('medical_encounters', None)
        emergency_encounters_data = data.pop('emergency_encounters', None)
        lab_encounters_data = data.pop('lab_encounters', None)
        pharmacy_encounters_data = data.pop('pharmacy_encounters', None)

        response_data_log = {}

        try:
            if medical_encounters_data is not None:
                response_data_log['medical_enc'], flag = add_encounter_util(medical_encounters_data, Medical,
                                                                            MedicalSerializer, 'Medical')
                if not flag:
                    raise Exception
            if emergency_encounters_data is not None:
                response_data_log['medical_enc'], flag = add_encounter_util(emergency_encounters_data, Emergency,
                                                                            EmergencySerializer, 'Emergency')
                if not flag:
                    raise Exception
            if lab_encounters_data is not None:
                response_data_log['medical_enc'], flag = add_encounter_util(lab_encounters_data, Lab, LabSerializer,
                                                                            'Lab')
                if not flag:
                    raise Exception
            if pharmacy_encounters_data is not None:
                response_data_log['medical_enc'], flag = add_encounter_util(pharmacy_encounters_data, Pharmacy,
                                                                            PharmacySerializer, 'Pharmacy')
                if not flag:
                    raise Exception
        except Exception as e:
            response_data_log['ERROR'] = 'Some data invalid'

        return Response({"response": response_data_log})


def episode_to_ipfs(episode_id):
    if Episode.objects.filter(pk=episode_id).exists():
        episode_obj = Episode.objects.get(pk=episode_id)
        member_obj = Member.objects.get(pk=episode_obj.member)

        try:
            client = ipfsApi.Client('127.0.0.1', 5001)
        except Exception as e:
            print(e)
            return False

        try:
            episode_obj.HistoryHash = member_obj.LastHash
            episode_obj.Active = False

            episode_json = EpisodeSerializer(episode_obj).data

            # some code to push json data into ipfs and get a hash
            episode_hash = client.add_json(episode_json)
            member_obj.LastHash = episode_hash
            episode_obj.delete()
        except Exception as e:
            print(e)
            # rollback
            episode_obj.HistoryHash = None
            episode_obj.Active = True
            return False

    return True


class DeactivateEpisode(APIView):
    def post(self, request):
        episode_id = json.loads(request.body)['episode_id']

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from rest_framework import generics

from .serializers import *
from .models import *

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
    def get(self, requset, MemberID):
        queryset = Member.objects.get(MemberID=MemberID)
        serializer = MemberSerializer(queryset)
        return Response(serializer.data)

    def post(self, requset, MemberID=None):
        if MemberID is None:
            data = json.loads(requset.body)
            # print('\n\n\n*******************')
            # print(data)
            # print('\n\n\n*******************')
            serializer = MemberSerializer(data=data['member_data'])
            if serializer.is_valid():
                member_saved = serializer.save()
                return Response({"success": "Member {} created successfully".format(data['member_data']['MemberID'])})
            return Response({"failed": "Member {} NOT created!!!".format(data['member_data']["MemberID"])})
        else:
            pass

        return Response({"done": True})

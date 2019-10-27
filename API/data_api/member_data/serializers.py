from rest_framework import serializers
from .models import *


class MedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical
        fields = '__all__'


class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = '__all__'


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'


class EpisodeSerializer(serializers.ModelSerializer):
    medical_encounters = MedicalSerializer(many=True)
    emergency_encounters = EmergencySerializer(many=True)
    lab_encounters = LabSerializer(many=True)
    pharmacy_encounters = PharmacySerializer(many=True)

    class Meta:
        model = Episode
        fields = (
            'member',
            'Episode_ID',
            'HistoryHash',
            'Active',
            'Disposition',
            'SOAP_Note',
            'CC',
            'medical_encounters',
            'emergency_encounters',
            'lab_encounters',
            'pharmacy_encounters'
        )

    def create(self, validated_data):
        medical_encounters_data = validated_data.pop('medical_encounters', None)
        emergency_encounters_data = validated_data.pop('emergency_encounters', None)
        lab_encounters_data = validated_data.pop('lab_encounters', None)
        pharmacy_encounters_data = validated_data.pop('pharmacy_encounters', None)

        episode = Episode.objects.create(**validated_data)

        if medical_encounters_data is not None:
            for medical_encounter in medical_encounters_data:
                Medical.objects.create(episode=episode, **medical_encounter)
        if emergency_encounters_data is not None:
            for emergency_encounter in emergency_encounters_data:
                Emergency.objects.create(episode=episode, **emergency_encounter)
        if lab_encounters_data is not None:
            for lab_encounter in lab_encounters_data:
                Lab.objects.create(episode=episode, **lab_encounter)
        if pharmacy_encounters_data is not None:
            for pharmacy_encounter in pharmacy_encounters_data:
                Pharmacy.objects.create(episode=episode, **pharmacy_encounter)

        return episode


class MemberSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Member
        fields = (
            'MemberID',
            'LastHash',
            'Patient_DOB',
            'Patient_Gender',
            'episodes'
        )

    def create(self, validated_data):
        episodes_data = validated_data.pop('episodes', None)

        member = Member.objects.create(**validated_data)

        if episodes_data is not None:
            for episode in episodes_data:
                Episode.objects.create(member=member, **episode)

        return member

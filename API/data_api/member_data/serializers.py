from rest_framework import serializers
from .models import *


class MedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical
        fields = (
            # base class
            'Encounter_ID',
            'Clinic_ID',
            'Encounter_DateTime',
            'Encounter_Description',
            'Provider_ID_x',
            'Provider_NPI',
            'Provider_Name',
            'lat',
            'lon',

            # derived class
            'CC',
            'Specialty_x',
        )


class EmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency
        fields = (
            # base class
            'Encounter_ID',
            'Clinic_ID',
            'Encounter_DateTime',
            'Encounter_Description',
            'Provider_ID_x',
            'Provider_NPI',
            'Provider_Name',
            'lat',
            'lon',

            # derived class
            'CC',
            'Specialty_x'
        )


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = (
            # base class
            'Encounter_ID',
            'Clinic_ID',
            'Encounter_DateTime',
            'Encounter_Description',
            'Provider_ID_x',
            'Provider_NPI',
            'Provider_Name',
            'lat',
            'lon',

            # derived class
            'Test_ID',
            'Order_ID_x',
            'Test_Name',
            'Units_x',
            'Result_Name',
            'Result_Status',
            'Date_Collected',
            'Date_Resulted',
            'Numeric_Result',
        )


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = (
            # base class
            'Encounter_ID',
            'Clinic_ID',
            'Encounter_DateTime',
            'Encounter_Description',
            'Provider_ID_x',
            'Provider_NPI',
            'Provider_Name',
            'lat',
            'lon',

            # derived class
            'Pharmacy_Name',
            'Prescription',
            'Drug_Name',
            'Units_y',
            'Days_Of_Supply',
            'Dispense_Date',
            'Dispense_Qty',
            'Dose'
        )


class EpisodeSerializer(serializers.ModelSerializer):
    medical_encounters = MedicalSerializer(many=True)
    emergency_encounters = EmergencySerializer(many=True)
    lab_encounters = LabSerializer(many=True)
    pharmacy_encounters = PharmacySerializer(many=True)

    class Meta:
        model = Episode
        fields = (
            'Episode_ID',
            'Disposition',
            'SOAP_Note',
            'medical_encounters',
            'emergency_encounters',
            'lab_encounters',
            'pharmacy_encounters'
        )

    @staticmethod
    def create(self, validated_data, member=None):
        medical_encounters_data = validated_data.pop('medical_encounters')
        emergency_encounters_data = validated_data.pop('emergency_encounters')
        lab_encounters_data = validated_data.pop('lab_encounters')
        pharmacy_encounters_data = validated_data.pop('pharmacy_encounters')

        if member is None:
            episode = Episode.objects.create(**validated_data)
        else:
            episode = Episode.objects.create(member=member, **validated_data)

        for medical_encounter in medical_encounters_data:
            Medical.objects.create(episode=episode, **medical_encounter)
        for emergency_encounter in emergency_encounters_data:
            Emergency.objects.create(episode=episode, **emergency_encounter)
        for lab_encounter in lab_encounters_data:
            Lab.objects.create(episode=episode, **lab_encounter)
        for pharmacy_encounter in pharmacy_encounters_data:
            Pharmacy.objects.create(episode=episode, **pharmacy_encounter)

        return episode


class MemberSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = Member
        fields = (
            'MemberID',
            'Patient_DOB',
            'Patient_Gender',
            'episodes'
        )

    def create(self, validated_data):
        episodes_data = validated_data.pop('episodes')

        member = Member.objects.create(**validated_data)

        for episode in episodes_data:
            _episode = EpisodeSerializer.create(self, validated_data=episode, member=member)

        return member

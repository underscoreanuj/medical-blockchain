from django.db import models


class Member(models.Model):
    # Gender choices constants
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    MemberID = models.CharField(primary_key=True, unique=True, max_length=100)
    Patient_DOB = models.DateField()
    Patient_Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    LastHash = models.TextField(null=True, blank=True, editable=False)

    def __str__(self):
        return '''
        Member: {}
        '''.format(str(self.MemberID))


class Episode(models.Model):
    # disposition choices constants
    RWTL = 'ReleasedWithoutLimitations'
    RWL = 'ReleasedWithLimitations'
    SAH = 'SickAtHome'
    ADMT = 'Admitted'

    DISPOSITION_CHOICES = [
        (RWTL, 'Released without limitations'),
        (RWL, 'Released with limitations'),
        (SAH, 'Sick at Home'),
        (ADMT, 'Admitted')
    ]

    Episode_ID = models.CharField(primary_key=True, unique=True, max_length=100)
    Active = models.BooleanField(default=True, editable=False)
    Disposition = models.CharField(max_length=100, choices=DISPOSITION_CHOICES, default=SAH)
    SOAP_Note = models.TextField()
    CC = models.CharField(max_length=100)
    HistoryHash = models.TextField(null=True, blank=True, editable=False)
    member = models.ForeignKey(Member, related_name='episodes', on_delete=models.CASCADE)

    def __str__(self):
        return '''
        Episode: {} -- Member: {}
        '''.format(str(self.Episode_ID), str(self.member.MemberID))


class EncounterBase(models.Model):
    Encounter_ID = models.CharField(primary_key=True, unique=True, max_length=100)
    Clinic_ID = models.CharField(max_length=100)
    Encounter_DateTime = models.DateTimeField()
    Encounter_Description = models.TextField()
    Provider_ID_x = models.BigIntegerField()
    Provider_NPI = models.BigIntegerField()
    Provider_Name = models.CharField(max_length=100)

    # to store location
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    lon = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)


class Medical(EncounterBase):
    Specialty_x = models.CharField(max_length=100)
    episode = models.ForeignKey(Episode, related_name='medical_encounters', on_delete=models.CASCADE)

    def __str__(self):
        return '''
        Encounter: {} -- Episode: {} -- Member: {}
        '''.format(str(self.Encounter_ID), str(self.episode.Episode_ID), str(self.episode.member.MemberID))


class Emergency(EncounterBase):
    Specialty_x = models.CharField(max_length=100)
    episode = models.ForeignKey(Episode, related_name='emergency_encounters', on_delete=models.CASCADE)

    def __str__(self):
        return '''
        Encounter: {} -- Episode: {} -- Member: {}
        '''.format(str(self.Encounter_ID), str(self.episode.Episode_ID), str(self.episode.member.MemberID))


class Lab(EncounterBase):
    Test_ID = models.CharField(max_length=100)
    Order_ID_x = models.CharField(max_length=100)
    Test_Name = models.CharField(max_length=100)
    Units_x = models.CharField(max_length=100)
    Result_Name = models.CharField(max_length=100)
    Result_Status = models.CharField(max_length=100)
    Date_Collected = models.DateTimeField()
    Date_Resulted = models.DateTimeField()
    Numeric_Result = models.BigIntegerField()
    episode = models.ForeignKey(Episode, related_name='lab_encounters', on_delete=models.CASCADE)

    def __str__(self):
        return '''
        Encounter: {} -- Episode: {} -- Member: {}
        '''.format(str(self.Encounter_ID), str(self.episode.Episode_ID), str(self.episode.member.MemberID))


class Pharmacy(EncounterBase):
    Pharmacy_Name = models.CharField(max_length=100)
    Prescription = models.CharField(max_length=100)
    Drug_Name = models.CharField(max_length=100)
    Units_y = models.CharField(max_length=100)
    Days_Of_Supply = models.BigIntegerField()
    Dispense_Date = models.DateTimeField()
    Dispense_Qty = models.BigIntegerField()
    Dose = models.BigIntegerField()
    episode = models.ForeignKey(Episode, related_name='pharmacy_encounters', on_delete=models.CASCADE)

    def __str__(self):
        return '''
        Encounter: {} -- Episode: {} -- Member: {}
        '''.format(str(self.Encounter_ID), str(self.episode.Episode_ID), str(self.episode.member.MemberID))

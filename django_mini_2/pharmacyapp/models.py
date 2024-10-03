# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has on_delete set to the desired behavior
#   * Remove managed = False lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    pword = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Pharmacy(models.Model):
    pname = models.CharField(max_length=100, blank=True, null=True)
    p_id = models.AutoField(primary_key=True)
    paddr = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pharmacy'


class Board(models.Model):
    pname = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, db_column='pname')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    uptime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'board'
        unique_together = (('pname', 'user'),)


class Score(models.Model):
    p = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    q1_score = models.IntegerField(blank=True, null=True)
    q2_score = models.IntegerField(blank=True, null=True)
    q3_score = models.IntegerField(blank=True, null=True)
    q4_score = models.IntegerField(blank=True, null=True)
    q5_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score'
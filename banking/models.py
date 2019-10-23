from __future__ import unicode_literals

from urllib import request
from django.db import models
from core.models import AuthUser


import logging
log = logging.getLogger("core.corelogger")


def user_bank_dir(instance, filename):
    # https://stackoverflow.com/a/34239992/4915733
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    dir_path = u'user_media/files/user_{0}/banking/{1}'.format(
        instance.author.id, request.quote(filename).encode('utf-8'))
    return dir_path
    # TODO: Add model to save banking data


class BankAccounts(models.Model):
    """ User, card, account holder """
    account_number = models.CharField(max_length=255, unique=True)
    holder_user = models.ForeignKey(AuthUser, null=True, related_name='account_holder',
                                    on_delete=models.CASCADE)
    holder_name = models.TextField(max_length=255)
    bank_name = models.TextField(max_length=255)

    class Meta:
        managed = True
        db_table = 'bank_accounts'

    def __str__(self):
        return '{0} - {1}:{2}'.format(self.holder_user, self.bank_name, self.account_number)


class AccountTypes(models.Model):
    """ Account type and descriptions: credit, debt etc """
    account_number = models.ForeignKey(BankAccounts, on_delete=models.CASCADE, blank=True)
    account_custom_type = models.TextField(null=True, blank=True)
    account_custom_comment = models.TextField(null=True, blank=True)
    user_alias = models.TextField(max_length=255, null=True, blank=True)
    active = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'bank_account_types'

    def __str__(self):
        return '{0} - {1}'.format(self.account_number, self.account_custom_type)


class OperationGroups(models.Model):
    """ User custom operations: cinemas, groceries, etd"""
    operation_group_name = models.TextField(max_length=255)
    operation_description = models.TextField(null=True, blank=True)
    operation_max_limit = models.IntegerField()
    operation_min_limit = models.IntegerField()
    operation_limit = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'bank_operation_groups'

    def __str__(self):
        return '{0} - {1}'.format(self.operation_group_name, self.operation_limit)


class CardOperations(models.Model):
    """ Card account operations """
    account_number = models.CharField(max_length=255)
    operation_type = models.TextField(null=True, blank=True)
    operation_date = models.DateTimeField()  # Convert from sheet
    operation_bank_date = models.DateTimeField()  # Convert from sheet
    operation_description = models.TextField(null=True, blank=True)
    operation_sum = models.IntegerField()
    operation_currency = models.TextField(max_length=255, null=True, blank=True)
    operation_sum_by_account_currency = models.IntegerField()
    account_currency = models.TextField(max_length=255, null=True, blank=True)
    company_code = models.TextField(max_length=255, null=True, blank=True)

    # Other relations:
    related_account_number = models.ForeignKey(
        BankAccounts, related_name='related_account_number',
        on_delete=models.CASCADE, blank=True, null=True)
    operation_group = models.ForeignKey(  # Can be more than one:
        OperationGroups, related_name='operation_group',
        on_delete=models.CASCADE, blank=True, null=True)
    operation_bank = models.ForeignKey(  # Can be only one:
        BankAccounts, related_name='operation_bank',
        on_delete=models.CASCADE, blank=True, null=True)
    operation_account_type = models.ForeignKey(  # Can be only one:
        AccountTypes, related_name='operation_account_type',
        on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bank_card_operations'

    def __str__(self):
        return '{0} - {1}/{2}/{3}/{4}'.format(
            self.account_number, self.operation_type,
            self.operation_group, self.operation_bank, self.operation_account_type)
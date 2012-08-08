#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime

from django import forms
from django.utils.translation import ugettext as _
from django.core import validators

from django_db_utils.forms import SpreadSheetField
from db_utils.validators.name import (
        NamesValidator, SurnameValidator, ALPHABET_LT)
from db_utils.validators.phone_number import PhoneNumberValidator
from pysheets.sheet import Sheet

from nmadb_students import models as students_models
from nmadb_contacts import models as contacts_models
from nmadb_academics import models


IMPORT_ACADEMICS_REQUIRED_COLUMNS = {
    u'first_name': _(u'First name'),
    u'last_name': _(u'Last name'),
    u'gender': _(u'Gender'),
    u'birth_date': _(u'Birth date'),
    u'school_class': _(u'Class'),
    u'school_year': _(u'School year'),
    u'school': _(u'School'),
    u'social_disadvantage_mark': _(u'Socially supported'),
    u'section': _(u'Section'),
    u'entered': _(u'Entered'),
    u'email': _(u'Email address'),
    u'main_address': _(u'Home address'),
    u'town': _(u'Town'),
    }


IMPORT_ACADEMICS_OPTIONAL_COLUMNS = {
    u'school_id':_(u'School ID'),
    u'phone': _(u'Phone'),
    u'municipality_code': _(u'Municipality code'),
    }


name_validator = NamesValidator(
        ALPHABET_LT,
        validation_exception_type=forms.ValidationError,
        )

surname_validator = SurnameValidator(
        ALPHABET_LT,
        validation_exception_type=forms.ValidationError,
        )

phone_number_validator = PhoneNumberValidator(
        u'370',
        validation_exception_type=forms.ValidationError,
        )

def academic_import_validate_row(sheet, row):
    """ Checks if row is valid.
    """
    new_row = {}
    for column, caption in IMPORT_ACADEMICS_REQUIRED_COLUMNS.items():
        try:
            new_row[column] = row[caption]
        except KeyError as e:
            raise forms.ValidationError(
                    _(u'Missing column: \u201c{0}\u201d.').format(
                        e.message))
    for column, caption in IMPORT_ACADEMICS_OPTIONAL_COLUMNS.items():
        try:
            new_row[column] = row[caption]
        except KeyError as e:
            pass

    try:
        new_row[u'first_name'] = name_validator(
                new_row[u'first_name'])
        new_row[u'last_name'] = name_validator(
                new_row[u'last_name'])
        for db_key, verbose_name in (
                students_models.Student.GENDER_CHOICES):
            if new_row[u'gender'] == verbose_name:
                new_row[u'gender'] = db_key
                break
        else:
            raise forms.ValidationError(
                    _(u'Unknown gender: \u201c{0}\u201d.').
                    format(new_row[u'gender']))
        try:
            new_row[u'school'] = students_models.School.objects.get(
                    title=new_row[u'school'])
        except students_models.School.DoesNotExist as e:
            raise forms.ValidationError(
                    _(u'School not found: \u201c{0}\u201d.').format(
                        new_row[u'school']))
        if 'school_id' in new_row:
            try:
                new_row['school_id'] = int(new_row['school_id'])
            except ValueError:
                raise forms.ValidationError(
                        _(u'School ID have to be a number. '
                        u'\u201c{0.title}\u201d ID is {1}. ').format(
                            new_row[u'school'], new_row['school_id']))
            if new_row[u'school'].id != new_row['school_id']:
                raise forms.ValidationError(
                        _(u'School ID does not match. '
                        u'\u201c{0.title}\u201d in DB is {0.id}. '
                        u'In file is {1}').format(
                            new_row[u'school'], new_row['school_id']))
        validators.validate_email(new_row[u'email'])
        try:
            new_row[u'section'] = models.Section.objects.get(
                    title__iexact=new_row[u'section'])
        except models.Section.DoesNotExist as e:
            raise forms.ValidationError(
                    _(u'Section not found: \u201c{0}\u201d.').format(
                        new_row[u'section']))
        for number_field in (u'school_class', u'school_year'):
            try:
                new_row[number_field] = int(new_row[number_field])
            except ValueError as e:
                raise forms.ValidationError(
                        _(u'Failed to convert to number: '
                        u'\u201c{0}\u201d.').format(
                            new_row[number_field]))
        if not (6 <= new_row[u'school_class'] and
                new_row[u'school_class'] <= 12):
            raise forms.ValidationError(
                    _(u'School class have to be between 6 and 12. '
                    u'Now it is {0}.').format(new_row[u'school_class']))
        if not (2005 <= new_row[u'school_year'] and
                new_row[u'school_year'] <= 2020):
            raise forms.ValidationError(
                    _(u'School year have to be between 2005 and 2020. '
                    u'Now it is {0}.').format(new_row[u'school_year']))
        if not (new_row.get(u'main_address') or u'').strip():
            raise forms.ValidationError(
                    _(u'Home address must be not empty.'))
        if not (new_row.get(u'town') or u'').strip():
            raise forms.ValidationError(
                    _(u'Town must be not empty.'))
        if new_row.get(u'phone'):
            new_row[u'phone'] = unicode(
                    phone_number_validator(new_row[u'phone']))
        else:
            new_row[u'phone'] = None
        try:
            new_row[u'birth_date'] = datetime.datetime.strptime(
                    new_row[u'birth_date'], u'%Y-%m-%d').date()
        except ValueError:
            raise forms.ValidationError(
                    _(u'Invalid date: \u201c{0}\u201d.').format(
                        new_row[u'birth_date']))
        try:
            new_row[u'entered'] = datetime.datetime.strptime(
                    new_row[u'entered'], u'%Y-%m-%d').date()
        except ValueError:
            raise forms.ValidationError(
                    _(u'Invalid date: \u201c{0}\u201d.').format(
                        new_row[u'entered']))
        if new_row[u'social_disadvantage_mark'] == _(u'Yes'):
            new_row[u'social_disadvantage_mark'] = True
        elif new_row[u'social_disadvantage_mark'] == _(u'No'):
            new_row[u'social_disadvantage_mark'] = False
        else:
            raise forms.ValidationError(
                    _(u'Socially supported have to be '
                    u'either \u201cYes\u201d or \u201cNo\u201d. '
                    u'Now it is \u201c{0}\u201d.').format(
                        new_row[u'social_disadvantage_mark']))
        try:
            if new_row.get(u'municipality_code'):
                new_row[u'municipality_code'] = (
                        contacts_models.Municipality.objects.get(
                            code=new_row[u'municipality_code']))
            else:
                new_row[u'municipality_code'] = (
                        new_row[u'school'].municipality)
        except contacts_models.Municipality.DoesNotExist:
            raise forms.ValidationError(
                    _(u'Failed to determine municipality.'))

    except forms.ValidationError as e:
        raise forms.ValidationError(
                _(u'{0} Error occurred in {1} line. '
                u'Sheet name is {2}.').format(
                    e.messages[0], len(sheet) + 2, sheet.name))
    return new_row


def academic_import_validate_sheet(spreadsheet, name, sheet):
    """ Creates sheet with correct columns.
    """
    sheet = Sheet(
            captions=(
                list(IMPORT_ACADEMICS_REQUIRED_COLUMNS.keys()) +
                list(IMPORT_ACADEMICS_OPTIONAL_COLUMNS.keys())))
    sheet.add_validator(academic_import_validate_row, 'insert')
    return sheet, name


class ImportAcademicsForm(forms.Form):
    """ Form for importing new academics.
    """

    spreadsheet = SpreadSheetField(
            sheet_name=_(u'Academics'),
            spreadsheet_constructor_args={
                'validators': {
                    'spreadsheet': [
                        (academic_import_validate_sheet, 'add_sheet'),
                        ],
                    },
                },
            label=_(u'Spreadsheet document'),
            required=True,
            help_text=_(
                u'Please select spreadsheet file. '
                u'Required columns are: {0}.').format(
                    u','.join(
                        _(u'\u201c{0}\u201d').format(caption)
                        for caption in
                        IMPORT_ACADEMICS_REQUIRED_COLUMNS.values()))
            )

    check_duplicates = forms.BooleanField(initial=True)

    def clean(self):
        """ Checks for duplicates.
        """
        cleaned_data = super(ImportAcademicsForm, self).clean()
        if cleaned_data.get(u'check_duplicates', False):
            found = []
            for sheet in cleaned_data.get('spreadsheet', ()):
                for row in sheet:
                    if contacts_models.Human.objects.filter(
                            first_name=row[u'first_name'],
                            last_name=row[u'last_name']).exists():
                        found.append((u'{0[first_name]} {0[last_name]}'
                            ).format(row))
                    if contacts_models.Human.objects.filter(
                            last_name=row[u'first_name'],
                            first_name=row[u'last_name']).exists():
                        found.append((u'{0[last_name]} {0[first_name]}'
                            ).format(row))
            if found:
                raise forms.ValidationError(
                        _(u'{0} already exists in database.').format(
                            u', '.join(found)))
        return cleaned_data

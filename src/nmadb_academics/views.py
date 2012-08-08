from django.contrib import admin
from django.db import transaction
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django import shortcuts
from django.contrib import messages
from annoying.decorators import render_to

from nmadb_academics import forms, models
from nmadb_students import models as students
from nmadb_contacts import models as contacts


@admin.site.admin_view
@render_to('admin/file-form.html')
@transaction.commit_on_success
def import_academics(request):
    """ Imports academics to NMADB.
    """
    if request.method == 'POST':
        form = forms.ImportAcademicsForm(request.POST, request.FILES)
        if form.is_valid():
            counter = 0
            for sheet in form.cleaned_data['spreadsheet']:
                for row in sheet:
                    student = students.Student()
                    student.first_name = row[u'first_name']
                    student.last_name = row[u'last_name']
                    student.gender = row[u'gender']
                    student.birth_date = row[u'birth_date']
                    student.school_class = row[u'school_class']
                    student.school_year = row[u'school_year']
                    student.save()
                    student.change_school(row[u'school'], row[u'entered'])
                    if row[u'social_disadvantage_mark']:
                        mark = students.SocialDisadvantageMark()
                        mark.student = student
                        mark.start = row[u'entered']
                        mark.end = None
                        mark.save()
                    academic = models.Academic()
                    academic.student = student
                    academic.section = row[u'section']
                    academic.entered = row[u'entered']
                    academic.left = None
                    academic.leaving_reason = None
                    academic.comment = None
                    academic.save()
                    email = contacts.Email()
                    email.human = student
                    email.address = row[u'email']
                    email.save()
                    address = contacts.Address()
                    address.human = student
                    address.town = row[u'town']
                    address.address = row[u'main_address']
                    address.municipality = row[u'municipality_code']
                    address.save()
                    student.main_address = address
                    student.save()
                    if row[u'phone']:
                        phone = contacts.Phone()
                        phone.number = row[u'phone']
                        print phone.number, student
                        phone.human = student
                        phone.save()
                    counter += 1
            msg = _(u'{0} academics successfully imported.').format(counter)
            messages.success(request, msg)
            return shortcuts.redirect(
                    'admin:nmadb_students_student_changelist')
    else:
        form = forms.ImportAcademicsForm()
    return {
            'admin_index_url': urlresolvers.reverse('admin:index'),
            'app_url': urlresolvers.reverse(
                'admin:app_list',
                kwargs={'app_label': 'nmadb_academics'}),
            'app_label': _(u'NMADB Academics'),
            'form': form,
            }


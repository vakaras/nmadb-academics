import datetime

from django.contrib import admin
from django.db import models as django_models
from django.utils.translation import ugettext as _

from nmadb_academics import models
from nmadb_students import models as students_models
from nmadb_students import admin as students_admin
from nmadb_utils import admin as utils
from nmadb_utils import actions
from django_db_utils import utils as db_utils


class SectionAdmin(utils.ModelAdmin):
    """ Administration for section.
    """

    list_display = [
            'id',
            'title',
            'abbreviation',
            'established',
            'abolished',
            ]


class AcademicInline(admin.StackedInline):
    """ Inline for academic information.
    """

    model = models.Academic
    extra = 0


class AchievementInline(admin.StackedInline):
    """ Inline for achievement information.
    """

    model = models.Achievement
    extra = 0


class AcademicAdmin(utils.ModelAdmin):
    """ Administration for academic.
    """

    list_display = (
            'id',
            'student',
            'section',
            'entered',
            'left',
            'leaving_reason',
            )

    list_filter = (
            'leaving_reason',
            'section',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            'entered',
            'left',
            'section__title',
            )

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'First name'), ('student', 'first_name',)),
            (_(u'Last name'), ('student', 'last_name',)),
            (_(u'School'), ('student', 'current_school', 'title')),
            (_(u'Class'), ('student', 'current_school_class')),
            (_(u'Section'), ('section', 'title')),
            (_(u'Entered'), ('entered',)),
            (_(u'Left'), ('left',)),
            (_(u'Leaving reason'), ('get_leaving_reason_display',)),
            )


class AcademicWorkbookProxy(models.Academic):
    """ Proxy for workbook admin.
    """

    class Meta:
        verbose_name = _(u'academic worbook')
        verbose_name_plural = _(u'academics workbook')
        proxy = True

class SchoolClassFilter(admin.SimpleListFilter):
    """ Allows to filter by current student class.
    """

    title = _(u'current class')
    parameter_name = 'class'

    def lookups(self, request, model_admin):
        """ Returns the list from 6 to 13.
        """
        return [
                (unicode(i), unicode(i))
                for i in range(6, 13)
                ] + [(u'13', u'older')]

    def queryset(self, request, queryset):
        """ Returns filtered by current class.
        """

        try:
            value = int(self.value())
        except (TypeError, ValueError):
            return queryset
        else:
            today =  datetime.date.today()
            if today.month >= 9:
                year = today.year + 1
            else:
                year = today.year
            if value == 13:
                return queryset.filter(
                        student__school_year__lt=(
                            (year-12) +
                            django_models.F('student__school_class')
                            )
                        )
            else:
                return queryset.filter(
                        student__school_year=(
                            (year-value) +
                            django_models.F('student__school_class')
                            )
                        )


class AcademicStatusFilter(admin.SimpleListFilter):
    """ Allows to filter by academic status.
    """

    title = _(u'status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """ Returns the list of years.
        """
        return models.Academic.LEAVING_REASON + (
                (u'N', _(u'studies')),
                )

    def queryset(self, request, queryset):
        """ Returns filtered by year.
        """
        if self.value() is None:
            return queryset
        else:
            if self.value() == u'N':
                value = None
            else:
                value = self.value()
            return queryset.filter(leaving_reason=value)


class YearEnteredFilter(admin.SimpleListFilter):
    """ Allows to filter by entered year.
    """

    title = _(u'year entered')
    parameter_name = 'year_entered'

    def lookups(self, request, model_admin):
        """ Returns the list of years.
        """
        entered = models.Academic.objects.all()
        first = entered.order_by('entered')[0]
        last = entered.order_by('-entered')[0]
        for year in range(first.entered.year, last.entered.year + 1):
            yield (unicode(year), unicode(year))

    def queryset(self, request, queryset):
        """ Returns filtered by year.
        """
        try:
            year = int(self.value())
        except (ValueError, TypeError):
            return queryset
        else:
            from datetime import date
            return queryset.filter(
                    entered__gte=date(year, 1, 1),
                    entered__lte=date(year, 12, 31),
                    )


class AcademicWorkbookAdmin(utils.ModelAdmin):
    """ Administration for academic.
    """

    list_display = (
            'student',
            'section',
            'get_phones',
            'get_emails',
            'current_school_class',
            'entered',
            'left',
            'leaving_reason',
            'current_school',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            'entered',
            'left',
            'section__title',
            'student__schools__title',
            )

    list_filter = (
            'section',
            AcademicStatusFilter,
            SchoolClassFilter,
            YearEnteredFilter,
            )

    list_max_show_all = 100
    list_per_page = 10

    def current_school_class(self, obj):
        """ Forwarding to student.
        """
        return obj.student.current_school_class()

    def get_phones(self, obj):
        """ Returns concatenation of all used phone numbers.
        """

        return db_utils.join(
                obj.student.phone_set.exclude(used=False),
                'number')
    get_phones.short_description = _("Phone numbers")

    def get_emails(self, obj):
        """ Returns concatenation of all used emails.
        """

        return db_utils.join(
                obj.student.email_set.exclude(used=False),
                'address')
    get_emails.short_description = _("Email addresses")

    def current_school(self, obj):
        """ Forwarding to student.
        """

        return obj.student.current_school().title
    current_school.short_description = _("current school")



class AchievementAdmin(utils.ModelAdmin):
    """ Administration for achievement.
    """

    list_display = (
            'id',
            'student',
            'academic',
            'competition',
            'competition_type',
            'place',
            )

    list_filter = (
            'competition_type',
            'place',
            )

    search_fields = (
            'id',
            'student__first_name',
            'student__last_name',
            'student__old_last_name',
            'competition',
            )

    raw_id_fields = (
            'student',
            'academic',
            )

    sheet_mapping = (
            (_(u'ID'), ('id',)),
            (_(u'First name'), ('student', 'first_name',)),
            (_(u'Last name'), ('student', 'last_name',)),
            (_(u'School'), ('student', 'current_school', 'title')),
            (_(u'Class'), ('student', 'current_school_class')),
            (_(u'Section'), ('academic', 'section', 'title')),
            (_(u'Competition'), ('competition',)),
            (_(u'Competition type'), ('get_competition_type_display',)),
            (_(u'Place'), ('get_place_display',)),
            )


class StudentAdmin(students_admin.StudentAdmin):
    """ Administration for student, who is also an academic.
    """

    inlines = students_admin.StudentAdmin.inlines + [
            AcademicInline,
#           AchievementInline,          # FIXME: Runs into infinitive loop.
            ]
    list_max_show_all = 100
    list_per_page = 10


actions.register(
        'nmadb-academics-import-academic',
        _(u'Import academics'),
        'nmadb-academics-import-academic')

admin.site.unregister(students_models.Student)
admin.site.register(students_models.Student, StudentAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Academic, AcademicAdmin)
admin.site.register(AcademicWorkbookProxy, AcademicWorkbookAdmin)
admin.site.register(models.Achievement, AchievementAdmin)

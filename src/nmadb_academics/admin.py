from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_academics import models
from nmadb_students import models as students_models
from nmadb_students import admin as students_admin
from nmadb_utils import admin as utils


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


admin.site.unregister(students_models.Student)
admin.site.register(students_models.Student, StudentAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Academic, AcademicAdmin)
admin.site.register(models.Achievement, AchievementAdmin)

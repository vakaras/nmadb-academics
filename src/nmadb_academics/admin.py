from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_academics import models
from nmadb_students import models as students_models
from nmadb_students import admin as students_admin


class SectionAdmin(admin.ModelAdmin):
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


class AcademicAdmin(students_admin.StudentAdmin):
    """ Administration for academic.
    """

    inlines = students_admin.StudentAdmin.inlines + [
            AcademicInline,
#           AchievementInline,          # FIXME: Runs into infinitive loop.
            ]


admin.site.unregister(students_models.Student)
admin.site.register(students_models.Student, AcademicAdmin)
admin.site.register(models.Section, SectionAdmin)

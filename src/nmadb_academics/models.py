from django.db import models
from django.utils.translation import ugettext as _

from nmadb_students.models import Student


class Section(models.Model):
    """ Information about section.
    """

    title = models.CharField(
            max_length=45,
            unique=True,
            )

    abbreviation = models.CharField(
            max_length=4,
            unique=True,
            )

    established = models.DateField(
            )

    abolished = models.DateField(
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'title',]

    def __unicode__(self):
        return unicode(self.title)


class Academic(models.Model):
    """ Information about academic.
    """

    LEAVING_REASON = (
            (u'F', _(u'finished'),),
            (u'W', _(u'withdrew'),),
            (u'R', _(u'removed'),),
            (u'C', _(u'changed'),),
            )

    student = models.ForeignKey(
            Student,
            )

    section = models.ForeignKey(
            Section,
            )

    entered = models.DateField(
            )

    left = models.DateField(
            blank=True,
            null=True,
            )

    leaving_reason = models.CharField(
            blank=True,
            null=True,
            choices=LEAVING_REASON,
            max_length=3,
            )

    comment = models.TextField(
            blank=True,
            null=True,
            )

    class Meta(object):
        ordering = [u'student', u'section',]

    def __unicode__(self):
        return u'{0.student} {0.section}'.format(self)


class Achievement(models.Model):
    """ Academics achievements information.
    """

    COMPETITION_TYPES = (
            (u'R', _(u'regional'),),
            (u'N', _(u'national'),),
            (u'I', _(u'international'),),
            )

    PLACES = (
            (0, _(u'other'),),
            (1, _(u'honorable mention'),),
            (2, _(u'third'),),
            (3, _(u'second'),),
            (4, _(u'first'),),
            )

    student = models.ForeignKey(
            Student,
            )

    academic = models.ForeignKey(
            Academic,
            blank=True,
            null=True,
            help_text=_(u'Set if achievement is from academic\'s field.'),
            )

    competition = models.CharField(
            max_length=128,
            )

    competition_type = models.CharField(
            max_length=3,
            choices=COMPETITION_TYPES,
            )

    place = models.CharField(
            max_length=3,
            choices=PLACES,
            )

    def __unicode__(self):
        return u'{0.competition_type} {0.place}'.format(self)

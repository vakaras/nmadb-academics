from django.db import models
from django.utils.translation import ugettext_lazy as _

from nmadb_students.models import Student


class Section(models.Model):
    """ Information about section.
    """

    title = models.CharField(
            max_length=45,
            unique=True,
            verbose_name=_(u'title'),
            )

    abbreviation = models.CharField(
            max_length=4,
            unique=True,
            verbose_name=_(u'abbreviation'),
            )

    established = models.DateField(
            verbose_name=_(u'established'),
            )

    abolished = models.DateField(
            blank=True,
            null=True,
            verbose_name=_(u'abolished'),
            )

    class Meta(object):
        ordering = [u'title',]
        verbose_name = _(u'section')
        verbose_name_plural = _(u'sections')

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
            (u'U', _(u'unknown')),      # The reason, why academic
                                        # has left is uknown.
                                        # Also, his leaving date
                                        # is unknown too.
            )

    student = models.ForeignKey(
            Student,
            verbose_name=_(u'student'),
            )

    section = models.ForeignKey(
            Section,
            verbose_name=_(u'section'),
            )

    entered = models.DateField(
            verbose_name=_(u'entered'),
            )

    left = models.DateField(
            blank=True,
            null=True,
            verbose_name=_(u'left'),
            )

    leaving_reason = models.CharField(
            blank=True,
            null=True,
            choices=LEAVING_REASON,
            max_length=3,
            verbose_name=_(u'leaving reason'),
            )

    comment = models.TextField(
            blank=True,
            null=True,
            verbose_name=_(u'comment'),
            )

    class Meta(object):
        ordering = [u'student', u'section',]

    def __unicode__(self):
        return u'{0.student} {0.section}'.format(self)

    class Meta(object):
        verbose_name = _(u'academic')
        verbose_name_plural = _(u'academics')


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
            verbose_name=_(u'student'),
            )

    academic = models.ForeignKey(
            Academic,
            blank=True,
            null=True,
            verbose_name=_(u'academic'),
            help_text=_(u'Set if achievement is from academic\'s field.'),
            )

    competition = models.CharField(
            max_length=128,
            verbose_name=_(u'competition'),
            )

    competition_type = models.CharField(
            max_length=3,
            verbose_name=_(u'type'),
            choices=COMPETITION_TYPES,
            )

    place = models.CharField(
            max_length=3,
            choices=PLACES,
            verbose_name=_(u'place'),
            )

    def __unicode__(self):
        return u'{0.competition_type} {0.place}'.format(self)

    class Meta(object):
        verbose_name = _(u'achievement')
        verbose_name_plural = _(u'achievements')

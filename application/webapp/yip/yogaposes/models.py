from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from conditions.models import Condition


class YogaPose(models.Model):
    english_name = models.CharField(max_length=150, blank=True)
    sanskrit_name = models.CharField(max_length=150, blank=True)
    # Some poses are known by multiple names
    alternate_name_one = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_two = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_three = models.CharField(max_length=150, null=True, blank=True)
    alternate_name_four = models.CharField(max_length=150, null=True, blank=True)

    # Somwhat of a sloppy workaround to accomodate the Workarounds system not being used.
    workaround_text = models.TextField(null=True, blank=True)

    image = models.ImageField(upload_to='static/img/yogaposes')
    contraindicated_conditions = models.ManyToManyField(Condition)
    video = models.CharField(max_length=1000, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("Yoga Pose")
        verbose_name_plural = _("Yoga Poses")
        ordering = ["sanskrit_name", "english_name"]

    
    def __str__(self):
        return self.sanskrit_name

    def save(self, *args, **kwargs):
        """
        Set english_name to sanskrit_name if no english_name exists,
        and set sanskrit_name to english_name if no sanskrit_name exists.
        """
        if self.english_name == "":
            self.english_name = self.sanskrit_name
        elif self.sanskrit_name == "":
            self.sanskrit_name = self.english_name
        super(YogaPose, self).save(*args, **kwargs)

    def image_tag(self):
        """
        Injects html for viewing images in the admin.
        """
        if self.image:
            return u'<img src="/%s" style="max-height:100px;"/>' % self.image
        else:
            pass

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class BeneficialPoses(models.Model):
    """
    Map a condition to the yoga poses beneficial to it.
    """
    condition = models.OneToOneField(Condition, on_delete=models.CASCADE)
    poses = models.ManyToManyField(YogaPose, related_name='beneficial_poses', blank=True, default=None)
    why_these_poses_help = models.TextField(null=True, blank=True)
    image_one = models.ImageField(upload_to='static/img/beneficial_poses', null=True, blank=True)
    image_two = models.ImageField(upload_to='static/img/beneficial_poses', null=True, blank=True)
    image_three = models.ImageField(upload_to='static/img/beneficial_poses', null=True, blank=True)
    image_dropdown = models.ManyToManyField(YogaPose, related_name='beneficial_poses_images', blank=True, default=None)
    video = models.CharField(max_length=1000, null=True, blank=True)
    video_title = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = _("Beneficial Poses and Explanations")
        verbose_name_plural = _("Beneficial Poses and Explanations")


class WorkAroundYogaPose(models.Model):
    """
    This class maps a combined yoga pose and condition to a workaround yoga
    pose that the user can do instead of the original pose.
    """
    title = models.CharField(max_length=300, null=True, blank=True)
    workaround_yogapose = models.ManyToManyField(YogaPose, related_name='workaround')
    yogapose = models.ManyToManyField(YogaPose, related_name='original_pose')
    condition = models.ManyToManyField(Condition)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.title


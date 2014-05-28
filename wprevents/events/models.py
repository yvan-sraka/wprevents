from django.conf import settings
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from uuslug import uuslug as slugify


class FunctionalArea(models.Model):
  class Meta:
    permissions = (
      ('can_administrate_functional_areas', 'Can administrate functional areas'),
    )

  name = models.CharField(max_length=120, blank=False)
  slug = models.SlugField(max_length=50, blank=False)
  color = models.CharField(max_length=7, blank=False, default="blue")

  def __unicode__(self):
    return self.name


class Space(models.Model):
  class Meta:
    permissions = (
      ('can_administrate_spaces', 'Can administrate spaces'),
    )

  COUNTRIES = settings.COUNTRIES.items()

  name = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)

  address = models.CharField(max_length=150)
  address2 = models.CharField(max_length=150, blank=True)
  city = models.CharField(max_length=50, blank=False, default='')
  country = models.CharField(max_length=50, default='US', choices=COUNTRIES)
  postal_code = models.CharField(max_length=8, blank=True)

  lat = models.FloatField(null=True)
  lon = models.FloatField(null=True)

  photo_url = models.URLField(max_length=300, null=True, blank=True)

  def __unicode__(self):
    return '%s' % self.name

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name, instance=self)
    super(Space, self).save(*args, **kwargs)


class EventManager(models.Manager):
  def past_events(self):
    return self.filter(end__lte=datetime.now())

  def upcoming_events(self):
    return self.filter(start__gte=datetime.now())

  def current_events(self):
    now = datetime.now()

    return self.filter(start__lte=now).filter(end__gte=now)

  def search(self, space_name, area_name, search_string):
    events = Event.objects.filter(
      space__slug__contains=space_name
    ).filter(
      areas__slug__contains=area_name
    ).filter(
      title__icontains=search_string
    ).distinct()

    return events


class Event(models.Model):
  class Meta:
    ordering = ['-start']
    permissions = (
      ('can_administrate_events', 'Can administrate'),
    )

  objects = EventManager()

  created = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  title = models.CharField(max_length=120)
  slug = models.SlugField(max_length=50, blank=True)
  description = models.TextField(blank=True)
  details = models.TextField(blank=True)

  start = models.DateTimeField(default=datetime.now)
  end = models.DateTimeField(default=datetime.now)

  space = models.ForeignKey(Space, null=True, blank=True, related_name='events_hosted', on_delete=models.SET_NULL)
  owner = models.ForeignKey(User, null=True, blank=True, related_name='events_created') # todo: remove null/blank

  areas = models.ManyToManyField(FunctionalArea, blank=True)

  def __unicode__(self):
    return '#%s %s' % (self.id, self.title)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title, instance=self)
    super(Event, self).save(*args, **kwargs)

  def get_duplicate_candidates(self, q=''):
    event_day = datetime.date(self.start)
    day_after_event = datetime.date(self.end) + timedelta(days=1)

    duplicate_candidates = Event.objects.filter(start__gte=event_day).filter(end__lte=day_after_event).exclude(id=self.id).filter(title__icontains=q)

    return duplicate_candidates

  def remove_duplicate(self, id):
    Event.objects.filter(id=id).delete()

  @property
  def area_names(self):
    return [area.name for area in self.areas.all()]

  @property
  def start_day(self):
    return self.start.strftime('%d')

  @property
  def start_month(self):
    return self.start.strftime('%b')

  @property
  def start_date(self):
    return self.start.strftime('%Y-%m-%d')

  @property
  def end_date(self):
    return self.end.strftime('%Y-%m-%d')
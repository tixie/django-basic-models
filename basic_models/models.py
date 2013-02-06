# Copyright 2011 Concentric Sky, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django import forms
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.template.defaultfilters import slugify
from copy import deepcopy
import re

from basic_models.managers import *
import cachemodel



_compat_auth_user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class ActiveModel(cachemodel.CacheModel):
    is_active = models.BooleanField(default=True, db_index=True)
    objects = ActiveModelManager()
    active_objects = FilteredActiveObjectsManager()

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserModel(models.Model):
    created_by = models.ForeignKey(_compat_auth_user_model, related_name='%(class)s_created', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(_compat_auth_user_model, related_name='%(class)s_updated', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class DefaultModel(UserModel, TimestampedModel, ActiveModel):
    class Meta:
        abstract = True


class SlugModel(DefaultModel):
    name = models.CharField(max_length=1024)
    slug = models.CharField(max_length=255, unique=True, blank=True)

    objects = SlugModelManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return [self.slug]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SlugModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class OnlyOneActiveModel(ActiveModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(OnlyOneActiveModel, self).save(*args, **kwargs)
        if self.is_active:
            self.__class__.objects.active().exclude(pk=self.pk).update(is_active=False)

    def publish(self):
        super(OnlyOneActiveModel, self).publish()
        pass

    def clone(self, *args, **kwargs):
        new_obj = deepcopy(self)
        new_obj.id = None
        new_obj.is_active = False
        new_obj.save()
        reverse_foreignkeys = self._meta.get_all_related_objects()
        for relation in reverse_foreignkeys:
            relation_items = getattr(self, relation.get_accessor_name(), None) 
            for item in relation_items.all():
                new_item = deepcopy(item)
                new_item.id = None
                setattr(new_item, relation.field.name, new_obj)
                new_item.save()
        reverse_m2ms = self._meta.get_all_related_many_to_many_objects()
        for relation in reverse_m2ms:
            relation_items = getattr(self, relation.get_accessor_name(), None) 
            for item in relation_items.all():
                new_item = deepcopy(item)
                new_item.id = None
                setattr(new_item, relation.field.name, new_obj)
                new_item.save()
        return new_obj
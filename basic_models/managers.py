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

from django.core.cache import cache
from django.conf import settings
from django.db.models.query import QuerySet
from django.db import models


class CustomQuerySetManager(models.Manager):
    def __init__(self, query_set=None):
        self._custom_query_set = query_set
        super(CustomQuerySetManager, self).__init__()

    def get_queryset(self):
        if self._custom_query_set:
            return self._custom_query_set(self.model)
        return QuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith('_'):
            # Helps avoid problems when pickling a model.
            raise AttributeError
        # expose queryset methods as manager methods as well.
        return getattr(self.get_queryset(), attr, *args)


class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ActiveModelManager(CustomQuerySetManager):
    def __init__(self):
        super(ActiveModelManager, self).__init__(query_set=ActiveQuerySet)


class FilteredActiveObjectsManager(ActiveModelManager):
    def get_queryset(self):
        return super(FilteredActiveObjectsManager, self).get_queryset().filter(is_active=True)


class DefaultModelManager(ActiveModelManager):
    pass


class SlugModelManager(DefaultModelManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class OnlyOneActiveManager(models.Manager):
    def get_active(self):
        cache_key = 'active_%s' % (self.model.__name__)
        active = cache.get(cache_key)
        if active is None:
            active = self.filter(is_active=True).order_by('-updated_at')
            if len(active) < 1:
                # no active one!... just pick the last one that was changed
                active = self.all().order_by('-updated_at')
                if len(active) < 1:
                    return None
            active = active[0]
            cache.set(cache_key, active, getattr(settings, "DEFAULT_CACHE_TIMEOUT", 900))
        return active

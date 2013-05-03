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

from django.db.models.query import QuerySet
from django.db import models


class CustomQuerySetManager(models.Manager):
    def __init__(self, query_set=None):
        self._custom_query_set = query_set
        super(CustomQuerySetManager, self).__init__()

    def get_query_set(self):
        if self._custom_query_set:
            return self._custom_query_set(self.model)
        return QuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith('_'):
            # Helps avoid problems when pickling a model.
            raise AttributeError
        # expose queryset methods as manager methods as well.
        return getattr(self.get_query_set(), attr, *args)


class ActiveQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ActiveModelManager(CustomQuerySetManager):
    def __init__(self):
        super(ActiveModelManager, self).__init__(query_set=ActiveQuerySet)


class FilteredActiveObjectsManager(ActiveModelManager):
    def get_query_set(self):
        return super(FilteredActiveObjectsManager, self).get_query_set().filter(is_active=True)


class DefaultModelManager(ActiveModelManager):
    pass


class SlugModelManager(DefaultModelManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

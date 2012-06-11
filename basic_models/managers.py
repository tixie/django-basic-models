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
from cachemodel import models as cachemodels


class HasActiveManager(cachemodels.CacheModelManager):
    use_for_related_fields = True

    def active(self):
        return self.filter(is_active=True)

class IsActiveManager(cachemodels.CacheModelManager):
    def get_query_set(self):
        return super(IsActiveManager, self).get_query_set().filter(is_active=True)

    def active(self):
        return self.all()

class SlugModelManager(HasActiveManager):
    def get_by_slug(self, slug, cache_timeout=None):
        return self.get_by("slug", slug, cache_timeout)

class IsActiveSlugModelManager(IsActiveManager):
    def get_by_slug(self, slug, cache_timeout=None):
        return self.get_by("slug", slug, cache_timeout)

class OnlyOneActiveManager(cachemodels.CacheModelManager):
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
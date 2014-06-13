![Concentric Sky](http://concentricsky.com/media/uploads/images/csky_logo.jpg)

# Django Basic Models

Django Basic Models is an open-source Django library developed by [Concentric Sky](http://concentricsky.com/). It provides abstract models that are commonly needed for Django projects.


### Table of Contents
- [Installation](#installation)
- [Getting Started](#getting-started)
- [License](#license)
- [About Concentric Sky](#about-concentric-sky)


## Installation

    pip install git+https://github.com/concentricsky/django-skythumbnails.git


## Getting Started

The models available to inherit from are ActiveModel, TimestampedModel, UserModel, DefaultModel, SlugModel, OnlyOneActiveModel. To use them, import basic_models in your models.py file and inherit from one 

	from basic_models import SlugModel

	class MyModel(SlugModel):
		pass


### ActiveModel

ActiveModel provides a boolean field called `is_active`, and allows filtering by that field with the standard manager as well as a custom `active_objects` manager. 

```
# Both return only objects with is_active=True
MyModel.objects.active()
MyModel.active_objects.all()
```

### TimestampedModel

TimestampedModel provides two datetime fields, `created_at` and `updated_at` that auto update on save.

### UserModel

UserModel provides two foreign keys to the auth user model, `created_by` and `updated_by`. Both fields should be set on save using the request.user.

### DefaultModel

DefaultModel combines the three models above: UserModel, TimestampedModel, and ActiveModel.

### SlugModel

SlugModel extends DefaultModel and adds `name` and `slug` charfields.

### OnlyOneActiveModel

OnlyOneActiveModel extends ActiveModel, but deactivates all other instances of the model if one is activated. It also provides a manager function called `get_active()` that returns the one active instance for the model.



## License

This project is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). Details can be found in the LICENSE.md file.


## About Concentric Sky

_For nearly a decade, Concentric Sky has been building technology solutions that impact people everywhere. We work in the mobile, enterprise and web application spaces. Our team, based in Eugene Oregon, loves to solve complex problems. Concentric Sky believes in contributing back to our community and one of the ways we do that is by open sourcing our code on GitHub. Contact Concentric Sky at hello@concentricsky.com._

from django.contrib import admin
from django.db import models


def create_model(name, fields=None, app_label='',
                 _module='', options=None, admin_opts=None):
    """
    https://code.djangoproject.com/wiki/DynamicModels
    This function provides everything necessary to make a fully functional
    Django model from scratch, even given data that's not available until the
    application is up and running.

    The arguments it takes work as follows:
    name       -    The name of the model to be created
    fields     -    A dictionary of fields the model will have (managers and
                        methods would go in this dictionary as well)
    app_label  -    A custom application label for the model (this does not
                        have to exist in your project, but see the Admin
                        drawback below)
    module     -    An arbitrary module name to use as the model's source
                        (prior to [5163], this had to be a real module path
                        that had in fact been loaded)
    options    -    A dictionary of options, as if they were provided to the
                        inner Meta class
    admin_opts -    A dictionary of admin options, as if they were provided t
                        o the Admin class (again, see Admin drawback below)
    """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': _module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_opts:
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model


simple_model_fields = {
    'name': models.CharField(max_length=20),
    'description': models.CharField(max_length=20)
}
simple_model_fields_name = [
    k for k, v in simple_model_fields.items()
]


def dict_keys(obj: dict):
    return sorted([k for k, v in obj.items()])


def class_attr_name(klass):
    return [a[0] for a in class_attr(klass)]


def class_attr(klass):
    def is_special_attr(a):
        return a[0].startswith("__") or a[0].endswith("__")

    return [att for att in filter(lambda a: not (is_special_attr(a)),
                                  klass.__dict__.items())]

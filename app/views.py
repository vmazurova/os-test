import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, Vyrobce, Vyrobek

def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ["name", "personal_celphone", "birthday", "contact_group.name"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                ],
                "expanded": False,
            },
        ),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                ],
                "expanded": False,
            },
        ),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                    "note",
                ],
                "expanded": False,
            },
        ),
    ]

class VyrobceModelView(ModelView):
    datamodel = SQLAInterface(Vyrobce)

    list_columns = ["name"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name" ]}),
    ]

class VyrobekModelView(ModelView):
    datamodel = SQLAInterface(Vyrobek)

    list_columns = ["name", "vyrobce"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Summary", {"fields": ["name", "vyrobce" ]}),
    ]

    add_fieldsets = [
        ("Summary", {"fields": ["name", "vyrobce" ]}),
    ]

    edit_fieldsets = [
        ("Summary", {"fields": ["name", "vyrobce" ]}),
    ]
class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = "Grouped Birth contacts"
    chart_type = "AreaChart"
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "year",
            "formatter": pretty_year,
            "series": [(aggregate_count, "group")],
        },
    ]


db.create_all()
fill_gender()
appbuilder.add_view(
    GroupModelView,
    "List Groups",
    icon="fa-folder-open-o",
    category="Contacts",
    category_icon="fa-envelope",
)
appbuilder.add_view(
    ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts"
)
appbuilder.add_view(
    VyrobceModelView, "Vyrobce", icon="fa-child", category="Contacts"
)
appbuilder.add_view(
    VyrobekModelView, "Vyrobky", icon="fa-toolbox", category="Contacts"
)
appbuilder.add_separator("Contacts")
appbuilder.add_view(
    ContactTimeChartView,
    "Contacts Birth Chart",
    icon="fa-dashboard",
    category="Contacts",
)


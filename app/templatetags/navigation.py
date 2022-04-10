from django import template

register = template.Library()


@register.simple_tag
def navigation():
    return [
        {
            "title": "",
            "items": [
                {
                    "path": "/samples",
                    "icon": "fas fa-vial",
                    "title": "Vzorky",
                },
                {
                    "path": "/analyses",
                    "icon": "fas fa-microscope",
                    "title": "Analýzy",
                },
                {
                    "path": "/grants",
                    "icon": "fas fa-file-invoice-dollar",
                    "title": "Granty",
                    "gates": ["garant", "admin"],
                },
            ],
        },
        {
            "title": "Administrácia",
            "gates": ["admin"],
            "items": [
                {
                    "path": "/users",
                    "icon": "fas fa-user-friends",
                    "title": "Správa užívateľov",
                },
                {
                    "path": "/administration",
                    "icon": "fas fa-tools",
                    "title": "Správa laboratórií",
                },
            ],
        },
        {
            "title": "Účet",
            "items": [
                {
                    "path": "/change-password",
                    "icon": "fas fa-lock",
                    "title": "Zmena hesla",
                },
                {
                    "path": "/logout",
                    "icon": "fas fa-sign-out-alt",
                    "title": "Odhlásiť sa",
                },
            ],
        },
    ]

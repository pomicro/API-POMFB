template = {
    "swagger": "2.0",
    "info": {
        "title": "API POMFB",
        "description": "APIs for Call Centre Pak Oman Microfinance Bank",
        "contact": {
            "responsibleOrganization": "POMFB",
            "responsibleDeveloper": "Suneel Kumar",
            "email": "suneel.kumar@pomicro.com",
            "url": "www.linkedin.com/in/SuneelKumarKanjani",
        },
        "termsOfService": "www.pomiro.com",
        "version": "1.0"
    },
    "basePath": "",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

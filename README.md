# ships django-app

Requirements:
- python3 with pip3
- django
- https://github.com/pyfa-org/eos
- Phobos dump
 -> having eos run atleast once with the example


# Setup:
1. Download into django project folder
2. Change myproject/urls.py into:

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ships/', include('ships.urls')),
    path('admin/', admin.site.urls),
]
```

3. change ships/views.py for your phobos folder (making these into a settings.py at some point)
4. ask me if it doesnt work
5. gg


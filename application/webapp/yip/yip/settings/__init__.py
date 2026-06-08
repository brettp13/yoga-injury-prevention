from yip.settings.base import *


# Ugly
try:
    from yip.settings.local import *
except:
    try:
        from yip.settings.development import *
    except:
        from yip.settings.production import *

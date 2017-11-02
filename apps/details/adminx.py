import xadmin

from .models import Detail

class DetailInfoAdmin(object):
    list_display = ['user','title','add_time']
    
    
    
xadmin.site.register(Detail,DetailInfoAdmin)
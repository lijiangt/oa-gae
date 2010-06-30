def header(request):
    return {
        'meta': request.META,
    }
    
def custom_setting(request):
    return  {
             'custom':request.session.get('custom_setting',None),
             }
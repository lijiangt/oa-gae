def header(request):
    return {
        'meta': request.META,
    }

# TODO    
def custom_setting(request):
    return  {
#             'custom':request.session.get('custom_setting',None),
             'custom':None,
             }
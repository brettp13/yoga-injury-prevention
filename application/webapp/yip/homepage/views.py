from django.shortcuts import render


def homepage(request, path='', *args, **kwargs):
    """
    Serve the base html page for the angular application.
    Check request.session to see if a traffic_source variable has been set.
    Otherwise, we can assume the traffic was organic.
    """
    try:
        traffic_source = request.session['traffic_source']
    except:
        traffic_source = 'organic'
    return render(request, 'home.html', context={'traffic_source': traffic_source})

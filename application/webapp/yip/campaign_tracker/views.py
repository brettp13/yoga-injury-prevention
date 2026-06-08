from django.shortcuts import redirect


def from_alex(request):
    """
    Set the 'traffic_source' header to indicate that 
    this site hit came from one of Alex's initiatives.
    """
    request.session['traffic_source'] = 'alex'
    return redirect('/')


def from_iayt(request):
    """
    Traffic from the iayt marketing campaign.
    """
    request.session['traffic_source'] = 'iayt'
    return redirect('/')

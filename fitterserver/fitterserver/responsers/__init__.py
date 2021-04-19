from django.http import HttpResponse  , Http404

def test_response(request):
	print ("say hello!")
	return HttpResponse("say hello!")
from .models import program

def allPrograms(request):
	if 'admin' in request.path:
		return{}
	else:
		p = program.objects.all()
	return dict(all_programs = p)
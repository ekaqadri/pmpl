from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
	comment = "Yey, waktunya berlibur"
	return render(request, 'home.html', {'comment': comment})

def new_list(request):
	list_ = List.objects.create()
	item = Item(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect(list_)

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	count_list = Item.objects.filter(list_id=list_id).count()
	error = None
	comment = ""

	if count_list == 0:
		comment = "Yey, waktunya berlibur"
	elif count_list < 5:
		comment = "Sibuk tapi santai"
	else:
		comment = "Oh tidak"

	if request.method == 'POST':
		try:
			item = Item(text=request.POST['item_text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			error = "You can't have an empty list item"

	return render(request, 'list.html', {'list': list_, 'comment': comment, 'error': error})

from audioop import reverse
from multiprocessing import context
from re import template
from unittest import loader
from django.shortcuts import get_object_or_404, redirect, render,HttpResponseRedirect
from .models import Places,Place_rating
from django.views import View, generic
from .models import Destimages, Comment
from django.db.models import Q
from django.views.generic import FormView 
from django.views.generic.detail import SingleObjectMixin 
from .forms import comment_form,rateform
from django.urls import reverse_lazy 
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from recommender.views import hybrid_recommender
from ratinghome.models import Rateinfo


@method_decorator(login_required, name='dispatch')
class placelistview(generic.ListView):
    model= Places
    template_name= 'destination/place_list.html'
    context_object_name = 'object'
  
    def get_context_data(self, **kwargs):
        recommendations = hybrid_recommender(self.request.user)
        
        if len(recommendations)==2:
            top = recommendations[0]
            other = recommendations[1]
        
            topqueryset = Places.objects.filter(rateinfo__pID__in = top)
            otherqueryset = Places.objects.filter(rateinfo__pID__in = other)
            context = super(placelistview, self).get_context_data(**kwargs)
            context.update({
                'top' : sorted(topqueryset, key=lambda x: top.index(x.rateinfo.pID)),
                'recommendations': sorted(otherqueryset, key=lambda x: other.index(x.rateinfo.pID)),
                'popular': Places.objects.filter(ispopular=True),
            })
            return context
        else:
            queryset= Places.objects.filter(rateinfo__pID__in=recommendations)
            
       
            context = super(placelistview, self).get_context_data(**kwargs)
            context.update({
                'top' : [],
                'recommendations': sorted(queryset, key=lambda x: recommendations.index(x.rateinfo.pID)),
                'popular': Places.objects.filter(ispopular=True),
            })
            return context
    

   
@login_required
def placedetailview(request,pk):
    place=get_object_or_404(Places,id=pk)
    comment = request.POST.get('msg')
    if comment== None or len(comment)==0:
        data=Places.objects.get(id=pk)         
        return render(request,'destination/place_view.html',{'data':data }) 

    else :
        data= Comment()
        data.user= request.user
        data.place_id=pk
        data.comment_body = comment
        data.save()
        data=Places.objects.get(id=pk)         
        return render(request,'destination/place_view.html',{'data':data }) 

    
        

   

@login_required
def Rateview(request, r_id):
     url = request.META.get('HTTP_REFERER')
     if request.method == 'POST':
        try:
            rating = Place_rating.objects.get(user__id=request.user.id, place__id=r_id)
            form = rateform(request.POST, instance=rating)
            form.save()
            
            return redirect('placeview', r_id)
        except Place_rating.DoesNotExist:
            form = rateform(request.POST)
            if form.is_valid():
                data = Place_rating()
                data.rate = form.cleaned_data['rate']
                data.place_id = r_id
                data.user_id = request.user.id
                data.save()
               
                return redirect(url)

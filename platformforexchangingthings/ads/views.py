from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.db.models import Q


class AdsListView(ListView):
    model = Ad
    template_name = 'ads/ads.html'
    context_object_name = 'ads'
    paginate_by = 6

    def get_queryset(self):
        queryset = Ad.objects.filter(is_draft=False).order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        category = self.request.GET.get('category')
        condition = self.request.GET.get('condition')

        if keyword:
            queryset = queryset.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        if category:
            queryset = queryset.filter(category=category)
        if condition:
            queryset = queryset.filter(condition=condition)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Ad.objects.values_list('category', flat=True).distinct()
        context['conditions'] = Ad.objects.values_list('condition', flat=True).distinct()
        return context


@login_required
def my_ads(request):
    ads = Ad.objects.filter(user=request.user).order_by('created_at')

    keyword = request.GET.get('keyword')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    if keyword:
        ads = ads.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)

    paginator = Paginator(ads, 6)
    page_number = request.GET.get('page')
    page_ads = paginator.get_page(page_number)

    categories = Ad.objects.values_list('category', flat=True).distinct()
    conditions = Ad.objects.values_list('condition', flat=True).distinct()

    context = {
        'ads': page_ads,
        'categories': categories,
        'conditions': conditions,
    }

    return render(request, 'ads/my_ads.html', context)


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.is_draft = True
            ad.save()
            return redirect('confirm_ad', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def confirm_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.is_draft = False
        ad.save()
        return redirect('my_ads')
    return render(request, 'ads/ad_confirm.html', {'ad': ad})


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('my_ads')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('my_ads')
    return render(request, 'ads/delete_ad_confirm.html', {'ad': ad})


@login_required
def create_exchange_proposal(request, ad_receiver):
    ad_receiver_instance = get_object_or_404(Ad, id=ad_receiver)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.user, request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver_instance
            proposal.status = 'Ожидает'
            proposal.save()
            return redirect('sent_proposals')
    else:
        form = ExchangeProposalForm(request.user)
    return render(request, 'ads/create_exchange_proposal.html', {'form': form})


@login_required
def sent_proposals(request):
    proposals = ExchangeProposal.objects.filter(Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)).order_by('-created_at')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')
    status = request.GET.get('status')

    if sender:
        proposals = proposals.filter(ad_sender__title__icontains=sender)
    if receiver:
        proposals = proposals.filter(ad_receiver__title__icontains=receiver)
    if status:
        proposals = proposals.filter(status=status)

    paginator = Paginator(proposals, 6)
    page_number = request.GET.get('page')
    page_proposals = paginator.get_page(page_number)

    return render(request, 'ads/sent_proposals.html', {'proposals': page_proposals})


@login_required
def update_exchange_proposal(request, proposal_id, status):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    print(proposal.ad_receiver.user)
    if proposal.ad_receiver.user == request.user:
        proposal.status = status
        proposal.save()
        return redirect('sent_proposals')
    return redirect('sent_proposals')

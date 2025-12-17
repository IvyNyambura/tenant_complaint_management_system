from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import Complaint, ComplaintUpdate
from .forms import ComplaintForm, ComplaintUpdateForm
from .services import assign_to_manager, update_status, set_due_date

def is_manager(user): return hasattr(user, 'role') and user.role in ['MANAGER','ADMIN']
def is_tenant(user): return hasattr(user, 'role') and user.role == 'TENANT'

@login_required
def dashboard(request):
    if is_manager(request.user):
        stats = Complaint.objects.values('status').annotate(total=Count('id'))
        recent = Complaint.objects.order_by('-created_at')[:10]
    else:
        stats = Complaint.objects.filter(tenant=request.user).values('status').annotate(total=Count('id'))
        recent = Complaint.objects.filter(tenant=request.user).order_by('-created_at')[:10]
    return render(request, 'complaints/dashboard.html', {'stats': stats, 'recent': recent})

@login_required
@user_passes_test(is_tenant)
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.tenant = request.user
            complaint.save()
            set_due_date(complaint)
            messages.success(request, f"Complaint submitted: {complaint.tracking_number}")
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintForm()
    return render(request, 'complaints/complaint_form.html', {'form': form})

@login_required
def complaint_list(request):
    if is_manager(request.user):
        qs = Complaint.objects.all().order_by('-created_at')
    else:
        qs = Complaint.objects.filter(tenant=request.user).order_by('-created_at')
    return render(request, 'complaints/complaint_list.html', {'complaints': qs})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if is_tenant(request.user) and complaint.tenant != request.user:
        messages.error(request, "Not authorized.")
        return redirect('complaints:list')
    updates = ComplaintUpdate.objects.filter(complaint=complaint).order_by('-created_at')
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint, 'updates': updates})

@login_required
@user_passes_test(is_manager)
def complaint_assign(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    assign_to_manager(complaint, request.user)
    messages.info(request, "Complaint acknowledged and assigned to you.")
    return redirect('complaints:detail', pk=pk)

@login_required
@user_passes_test(is_manager)
def complaint_update(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = ComplaintUpdateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        upd = form.save(commit=False)
        upd.complaint = complaint
        upd.actor = request.user
        upd.save()
        update_status(complaint, upd.status)
        messages.success(request, "Status updated.")
        return redirect('complaints:detail', pk=pk)
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint, 'form': form})
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ManageCourseListView(ListView):
    model = Course
    template_name = 'courses/manage/course/list.html'

    def get_queryset(self):
        qs = super(ManageCourseListView, self).get_queryset()
        return qs.filter(owner=self.request.user)


""" Mixins """
class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/list.html'

class ManageCourseListView(OwnerEditMixin, ListView):
    template_name = 'courses/manage/course/list.html'

# Create
class CourseCreateView(OwnerCourseEditMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'courses.add_course'

# Update
class CourseUpdateView(OwnerCourseEditMixin, UpdateView, PermissionRequiredMixin):
    permission_required = 'courses.change_course'

# Delete
class CourseDeleteView(OwnerCourseMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'courses/manage/course/list.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'



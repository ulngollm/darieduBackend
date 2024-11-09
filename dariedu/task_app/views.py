from django.db.models import F
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .exceptions import BadRequest
from .models import Task, Delivery, DeliveryAssignment, TaskCategory
from .permissions import IsAbleCompleteTask, IsCurator, is_confirmed
from .serializers import TaskSerializer, DeliverySerializer, DeliveryAssignmentSerializer, TaskVolunteerSerializer, \
    TaskCategorySerializer  #DeliveryVolunteerSerializer


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that provides methods to work with tasks.

    Actions:
        list: get a list of available tasks + filtering by date (for start_date) YYYY-MM-DD, category and city
        my: get a user specific tasks (supports filtering)
        accept: accept an available task
        refuse: refuse a user specific active uncompleted task
        complete: mark task as completed and add points to volunteers
        curator_of: get list of tasks where current user is curator
        categories: get list of task categories
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['start_date', 'end_date']
    filterset_fields = ['category', 'city']

    def get_queryset(self):
        """
        Get queryset for specific action.

        Actions:
            list: all available tasks + filtering by date (for start_date) YYYY-MM-DD, category and city
            my: user specific tasks + filtering against query params
            accept: all available tasks
            refuse: user specific active uncompleted tasks
            complete: active uncompleted tasks only
            curator_of: all tasks where current user is the curator
        """

        if self.action == 'list':
            # all available tasks
            user_tasks = self.request.user.tasks.values_list('id', flat=True)
            date = self.request.query_params.get('date', None)
            queryset = Task.objects.filter(
                is_active=True,
                is_completed=False,
                end_date__gt=timezone.now(),
                volunteers_needed__gt=F('volunteers_taken')
            ).exclude(id__in=user_tasks)
            if date:
                try:
                    date = timezone.datetime.strptime(date, '%Y-%m-%d')
                    queryset = queryset.filter(start_date__date=date)
                except ValueError:
                    pass
            return queryset

        if self.action == 'my':
            user = self.request.user
            queryset = user.tasks.all()

            after = self.request.query_params.get('after', None)
            before = self.request.query_params.get('before', None)
            active = self.request.query_params.get('is_active', None)
            completed = self.request.query_params.get('is_completed', None)
            if after:
                try:
                    after = timezone.datetime.strptime(after, '%Y-%m-%d')
                    queryset = queryset.filter(end_date__date__gte=after)
                except ValueError:
                    pass
            if before:
                try:
                    before = timezone.datetime.strptime(before, '%Y-%m-%d')
                    queryset = queryset.filter(start_date__date__lte=before)
                except ValueError:
                    pass
            if active is not None and active.lower() == 'true':
                queryset = queryset.filter(is_active=True).distinct()
            if completed is not None and completed.lower() == 'true':
                queryset = queryset.filter(is_completed=True).distinct()
            return queryset

        elif self.action == 'refuse':
            # the user can only abandon his active uncompleted task
            return self.request.user.tasks.filter(is_active=True, is_completed=False)

        elif self.action == 'complete':
            # curator can complete only active and uncompleted tasks
            return Task.objects.filter(is_active=True, is_completed=False)

        elif self.action == 'curator_of':
            # return tasks where the current user is curator
            return self.request.user.task_curator.filter(is_active=True, is_completed=False)

        # all available tasks
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'complete':
            pass
            # для метода завершения задачи куратором
            permission_classes = [IsAbleCompleteTask]
        elif self.action == 'curator_of':
            permission_classes = [IsCurator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return TaskSerializer
        else:
            return TaskVolunteerSerializer

    @action(detail=False, methods=['get'], url_name='my_tasks')
    @is_confirmed
    def my(self, request):
        """
        Get current user's tasks.
        Returns all user's tasks by default.
        Authenticated only.
        Filters:
        is_active - filter tasks by active status, for available is true, true or false
        is_completed - filter tasks by completed status, for history is true, true or false
        after - filter tasks by start date
        before - filter tasks by end date
        Пример фильтров для календаря: api/tasks/my/?after=2024-10-05&before=2024-10-20
        Формат даты: YYYY-MM-DD
        можно использовать вместе или по отдельности
        """
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='task_accept')
    @is_confirmed
    def accept(self, request, pk=None):
        """
        Accept an available task.
        Post request body should be empty. Will be ignored anyway.
        Authenticated only.
        """
        task = self.get_object()

        if request.user in task.volunteers.all():
            return Response({"error": "You've already taken this task!"}, status=status.HTTP_400_BAD_REQUEST)

        if task.volunteers_taken >= task.volunteers_needed:
            return Response({"error": "This task is full!"}, status=status.HTTP_400_BAD_REQUEST)

        Task.objects.filter(pk=task.pk).update(volunteers_taken=F('volunteers_taken') + 1)
        task.volunteers.add(request.user)

        task.refresh_from_db()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='task_refuse')
    @is_confirmed
    def refuse(self, request, pk=None):
        """
        Abandon the task.
        Can only abandon an active uncompleted task.
        Post request body should be empty. Will be ignored anyway.
        Authenticated only.
        """
        task = self.get_object()

        if request.user not in task.volunteers.all():
            return Response({"error": "You haven't taken this task!"}, status=status.HTTP_400_BAD_REQUEST)
        Task.objects.filter(pk=task.pk).update(volunteers_taken=F('volunteers_taken') - 1)

        task.volunteers.remove(request.user)

        task.refresh_from_db()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_name='task_complete')
    @is_confirmed
    def complete(self, request, pk=None):
        """
        Complete the task.
        Can only complete an active uncompleted task.
        Post request body should be empty. Will be ignored anyway.
        Curators only.
        """
        task = self.get_object()

        if task.is_completed:
            return Response({"error": "This task is already completed!"}, status=status.HTTP_400_BAD_REQUEST)

        task.is_completed = True
        task.is_active = False
        task.save()

        for volunteer in task.volunteers.all():
            volunteer.update_volunteer_hours(
                hours=volunteer.volunteer_hour + task.volunteer_price,
                point=volunteer.point + task.volunteer_price
            )

        curator = task.curator
        curator.update_volunteer_hours(
            hours=curator.volunteer_hour + task.curator_price,
            point=curator.point + task.curator_price
        )

        task.refresh_from_db()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='task_curator_of')
    @is_confirmed
    def curator_of(self, request):
        """
        Get all tasks where current user is the curator of the task.
        Curators only.
        """
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_name='task_categories')
    def get_categories(self, request):
        """
        Вывод категорий задач
        """
        categories = TaskCategory.objects.all()
        serializer = TaskCategorySerializer(categories, many=True)
        return Response(serializer.data)


class DeliveryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Delivery.objects.all()

        free = self.request.query_params.get('free', None)
        active = self.request.query_params.get('active', None)
        completed = self.request.query_params.get('completed', None)
        date = self.request.query_params.get('date', None)

        # TODO it works only for list. need to add for volunteers and curators deliveries
        if date:
            try:
                date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
                self.queryset = self.queryset.filter(date__date=date)
            except ValueError:
                pass

        if action == 'deliveries_curator' and self.request.user.is_staff:
            return queryset.filter(is_active=True, curator=user)

        if free is not None and free.lower() == 'true':
            queryset = queryset.filter(is_free=True).distinct()
        if active is not None and active.lower() == 'true':
            queryset = queryset.filter(is_active=True, assignments__volunteer=user).distinct()
        if completed is not None and completed.lower() == 'true':
            queryset = queryset.filter(is_completed=True, assignments__volunteer=user).distinct()
        return queryset

    @action(detail=False, methods=['get'], url_path='volunteer')
    def volunteer_deliveries(self, request):
        free_deliveries = self.get_queryset().filter(is_free=True).exclude(
            assignments__volunteer=request.user).distinct()
        active_deliveries = self.get_queryset().filter(is_active=True, assignments__volunteer=request.user).distinct()
        completed_deliveries = self.get_queryset().filter(is_completed=True,
                                                          assignments__volunteer=request.user).distinct()
        free_serializer = self.get_serializer(free_deliveries, many=True)
        active_serializer = self.get_serializer(active_deliveries, many=True)
        completed_serializer = self.get_serializer(completed_deliveries, many=True)
        response_data = {
            'свободные доставки': free_serializer.data,
            'мои активные доставки': active_serializer.data,
            'мои завершенные доставки': completed_serializer.data
        }
        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='curator')
    @is_confirmed
    def deliveries_curator(self, request):
        total_deliveries = Delivery.objects.filter(in_execution=True)
        id_deliveries = total_deliveries.values_list('id', flat=True)
        active_deliveries = Delivery.objects.filter(is_active=True)
        id_active_deliveries = active_deliveries.values_list('id', flat=True)

        return Response({
            'выполняются доставки (id)': id_deliveries,
            'количество активных доставок (id)': id_active_deliveries,
        })

    @action(detail=True, methods=['post'], url_path='take')
    @is_confirmed
    def take_delivery(self, request, pk):
        delivery = self.get_object()

        if delivery.is_free:
            if not DeliveryAssignment.objects.filter(delivery=delivery, volunteer=request.user).exists():
                assignment = DeliveryAssignment.objects.create(delivery=delivery)
                assignment.save()
                assignment.volunteer.add(request.user)
                serializer = DeliveryAssignmentSerializer(assignment)
                return Response({status.HTTP_201_CREATED: serializer.data})
            else:
                return Response({'error': 'You have already taken this delivery'}, status=400)
        else:
            return Response({'error': 'Delivery is already taken'}, status=400)

    @action(detail=True, methods=['post'], url_path='cancel')
    @is_confirmed
    def cancel_delivery(self, request, pk):
        delivery = self.get_object()
        delivery_assignment = delivery.assignments.filter(volunteer=request.user).first()

        if delivery_assignment:
            delivery_assignment.volunteer.remove(request.user)
            return Response({'message': 'Delivery cancelled successfully'}, status=200)
        else:
            return Response({'error': 'You are not authorized to cancel this delivery'}, status=403)

    @action(detail=True, methods=['post'], url_path='complete')
    @is_confirmed
    def complete_delivery(self, request, pk):
        delivery = self.get_object()
        if self.request.user != delivery.curator:
            return Response({'error': 'You are not authorized to complete this delivery'}, status=403)
        else:
            if delivery.is_completed:
                return Response({'error': 'Delivery is already completed'}, status=400)
            else:
                delivery.is_completed = True
                delivery.in_execution = False
                delivery.is_active = False
                delivery.is_free = False
                curator = delivery.curator
                curator.update_volunteer_hours(hours=curator.volunteer_hour + 4,
                                               point=curator.point + 4)
                curator.save()
                for assignment in delivery.assignments.all():
                    for volunteer in assignment.volunteer.all():
                        volunteer.update_volunteer_hours(
                            hours=volunteer.volunteer_hour + delivery.price,
                            point=volunteer.point + delivery.price
                        )
                        volunteer.save()
                delivery.save()
                return Response({'message': 'Delivery completed successfully'}, status=200)

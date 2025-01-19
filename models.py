from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal

user_registrated = Signal()


class Dolzn(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name


class AdvUser(AbstractUser):
    dolzn = models.ForeignKey(Dolzn, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Должность')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.username

    def get_current_user(request):
        user = request.user
        return user

    def delete(self, *args, **kwargs):
        for bb in self.additionalimage_set.all():
            bb.delete()
        super().delete(*args, **kwargs)


class Project(models.Model):
    STATUS_CHOICE = (
        ("В работе", "В работе"),
        ("Завершен", "Завершен"),
    )
    name = models.CharField('Название', max_length=255)
    date_start = models.DateField('Дата начала')
    date_end = models.DateField('Дата сдачи')
    status = models.CharField("Статус проекта", choices=STATUS_CHOICE, max_length=50)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class TypeWork(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Вид работы'
        verbose_name_plural = 'Виды работ'

    def __str__(self):
        return self.name


class WorkerInProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    worker = models.ManyToManyField(AdvUser, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'Сотрудник в проекте'
        verbose_name_plural = 'Сотрудники в проекте'


class WorkOnProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    worker = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Сотрудник')
    description = models.TextField('Описание')
    type_work = models.ForeignKey(TypeWork, on_delete=models.CASCADE, verbose_name='Вид работы')
    dat = models.DateField("Дата")

    class Meta:
        verbose_name = 'Работа по проекту'
        verbose_name_plural = 'Работы по проектам'

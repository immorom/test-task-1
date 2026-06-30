from django.db    import models
from django.utils import timezone

class Status(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = "Статус"
        verbose_name_plural = "Статусы"
    
    name = models.CharField(max_length=25, verbose_name="Название")

class OperationType(models.Model):
    def  __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = "Тип"
        verbose_name_plural = "Типы"
    
    name = models.CharField(max_length=25, verbose_name="Название")

class Category(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = "Категория"
        verbose_name_plural = "Категории"
    
    operationType = models.ForeignKey(OperationType, on_delete=models.CASCADE, verbose_name="Тип")

    name = models.CharField(max_length=25, verbose_name="Название")

class Subcategory(models.Model):
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    name = models.CharField(max_length=25, verbose_name="Название")

class Transaction(models.Model):
    class Meta:
        verbose_name        = "ДДС"
        verbose_name_plural = "ДДС"

    status        = models.ForeignKey(Status,        on_delete=models.PROTECT, verbose_name="Статус")
    operationType = models.ForeignKey(OperationType, on_delete=models.PROTECT, verbose_name="Тип")
    category      = models.ForeignKey(Category,      on_delete=models.PROTECT, verbose_name="Категория")
    subcategory   = models.ForeignKey(Subcategory,   on_delete=models.PROTECT, verbose_name="Подкатегория")

    amount  = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    date    = models.DateField(default=timezone.now, verbose_name="Дата создания записи")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
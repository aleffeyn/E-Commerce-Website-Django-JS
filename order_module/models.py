from django.db import models

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey('account_module.User' , on_delete=models.CASCADE , verbose_name='User')
    is_paid = models.BooleanField(verbose_name='Order Status')
    payment_date = models.DateTimeField(null=True, blank=True ,verbose_name= 'Payment Date')

    def calculate_total_amount(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product.price * order_detail.count
        return total_amount

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , verbose_name='Order')
    product = models.ForeignKey('product_module.Product' , on_delete=models.CASCADE , verbose_name='Product')
    final_price = models.IntegerField(null=True, blank=True , verbose_name='Final Price')
    count = models.IntegerField(verbose_name='Count')

    def get_total_price(self):
        return self.product.price * self.count

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Orders Details'


    def __str__(self):
        return str(self.order)


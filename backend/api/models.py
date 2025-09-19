from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)   # prevent duplicates
    sector = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class IPO(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('closed', 'Closed'),
        ('listed', 'Listed'),
    ]

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='ipos'
    )
    price_band = models.CharField(max_length=100, blank=True)
    open_date = models.DateField()
    close_date = models.DateField()
    issue_size = models.CharField(max_length=100, blank=True)
    issue_type = models.CharField(max_length=100, blank=True)
    listing_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='upcoming'
    )
    ipo_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    listing_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_market_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rhp_pdf = models.FileField(upload_to='docs/', null=True, blank=True)
    drhp_pdf = models.FileField(upload_to='docs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-open_date']
        verbose_name = "IPO"
        verbose_name_plural = "IPOs"

    def __str__(self):
        return f"{self.company.name} ({self.get_status_display()})"

    @property
    def listing_gain(self):
        """% gain on listing day"""
        if self.ipo_price and self.listing_price:
            return round(((self.listing_price - self.ipo_price) / self.ipo_price) * 100, 2)
        return None

    @property
    def current_return(self):
        """% return vs IPO price at current market price"""
        if self.ipo_price and self.current_market_price:
            return round(((self.current_market_price - self.ipo_price) / self.ipo_price) * 100, 2)
        return None

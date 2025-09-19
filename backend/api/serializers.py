from rest_framework import serializers
from .models import Company, IPO

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'sector', 'description', 'website', 'logo', 'created_at']
        read_only_fields = ['id', 'created_at']


class IPOSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )

    listing_gain = serializers.SerializerMethodField()
    current_return = serializers.SerializerMethodField()

    class Meta:
        model = IPO
        fields = [
            'id', 'company', 'company_id',
            'price_band', 'open_date', 'close_date', 'issue_size',
            'issue_type', 'listing_date', 'status', 'ipo_price',
            'listing_price', 'current_market_price', 'rhp_pdf', 'drhp_pdf',
            'listing_gain', 'current_return', 'created_at',
        ]
        read_only_fields = ['id', 'company', 'listing_gain', 'current_return', 'created_at']

    def get_listing_gain(self, obj):
        return obj.listing_gain

    def get_current_return(self, obj):
        return obj.current_return

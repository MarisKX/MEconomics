from rest_framework import serializers
from .models import Company, GovInstitution


owner_type_choice_field = serializers.ChoiceField(
    choices=[
        ('0', 'Private'),
        ('1', 'Company'),
        ('2', 'Government Institution'),
    ],
    write_only=True,
    required=False,
    help_text="Choose the type of owner.",
)


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for listing companies.
    """
    owner_name = serializers.SerializerMethodField()
    owner_type = serializers.SerializerMethodField()
    owner_type_choice_field = owner_type_choice_field

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'registration_number',
            'established',
            'invoice_prefix',
            'warehouse',
            'owner_type',
            'owner_type_choice_field',
            'owner_name',
            'employee_count',
        ]

    def get_owner_name(self, obj):
        """
        Return the name of the owner, either from owner_pp or owner_com.
        """
        if obj.owner_pp:
            return obj.owner_pp.full_name
        elif obj.owner_com:
            return obj.owner_com.name
        return None

    def get_owner_type(self, obj):
        """
        Return the human-readable version of the owner_type choice.
        """
        return obj.get_owner_type_low_display()

    def create(self, validated_data):
        if validated_data.get('owner_pp'):
            validated_data['owner_type_low'] = '0'
        elif validated_data.get('owner_com'):
            validated_data['owner_type_low'] = '1'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update and return a company"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CompanyDetailSerializer(CompanySerializer):
    """
    Serializer for displaying detailed information about a company.
    """
    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + [
            'id',
            'owner_pp',
            'owner_com',
            'name_low',
            'manufacturer_code',
            'street_adress_1',
            'street_adress_2',
            'city',
            'post_code',
            'country',
            'total_salaries_cost',
            'total_bruto_salaries',
            'total_salary_vsaoi_dd',
            'total_salary_vsaoi_dn',
            'total_salary_iin',
            'total_salary_netto',
            'average_salary_brutto',
        ]


class GovInstitutionSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Government Institutions.
    """
    class Meta:
        model = GovInstitution
        fields = [
            'id',
            'name',
            'registration_number',
            'established',
            'authority',
            'employee_count',
        ]

    def create(self, validated_data):
        """Create and return a new citizen"""
        return GovInstitution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a citizen"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class GovInstitutionDetailSerializer(GovInstitutionSerializer):
    """
    Serializer for displaying detailed information
    about a Government Institution.
    """
    class Meta(GovInstitutionSerializer.Meta):
        fields = GovInstitutionSerializer.Meta.fields + [
            'id',
            'name_low',
            'street_adress_1',
            'street_adress_2',
            'city',
            'post_code',
            'country',
            'total_salaries_cost',
            'total_bruto_salaries',
            'total_salary_vsaoi_dd',
            'total_salary_vsaoi_dn',
            'total_salary_iin',
            'total_salary_netto',
            'average_salary_brutto',
        ]

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience

# ==========================================================
# SERIALIZER PROJECT
# ==========================================================
class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


# ==========================================================
# SERIALIZER EXPERIENCE
# ==========================================================
class ExperienceSerializer(serializers.ModelSerializer):
    # SerializerMethodField berarti nilai field ini dihitung menggunakan method, bukan langsung diambil dari kolom database.
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", 
            "category", "category_display",
            "thumbnail", 
            "started_at", "ended_at", "is_ongoing", 
            "star_count", "is_starred",
        ]

        # Field yang hanya boleh dibaca.
        read_only_fields = [
            "id",
            "started_at",
        ]

    # Validasi fields sebelum data disimpan.
    def validate_title(self, value):
        # strip_tags menghapus tag HTML, sedangkan strip menghapus spasi di awal dan akhir teks.
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value
 
    def validate_description(self, value):
        return strip_tags(value).strip()


    # Menghitung jumlah pengguna yang memberi star pada Experience.
    def get_star_count(self, obj):
        return obj.starred_by.count()

    # Mengembalikan status star untuk pengguna yang sedang mengakses API.
    def get_is_starred(self, obj):
        request = self.context.get("request")

        # Pengunjung yang belum login tidak memiliki status star.
        if request is None or not request.user.is_authenticated:
            return False
        
        # Cek apakah pengguna tersebut ada di relasi starred_by.
        return obj.starred_by.filter(pk=request.user.pk).exists()

    def get_starred_by_names(self, obj):
            return ", ".join(user.username for user in obj.starred_by.all())
    

    def get_is_ongoing(self, obj):
        return obj.is_ongoing

    def get_category_display(self, obj):
        return obj.get_category_display()

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('api/', include('accounts.urls')),
# #     path('api/listings', include('listings.urls')),
# #     path("api/payments/", include("payments.urls")),
# #     path("api/auth/", include("accounts.urls")),
# # ]

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     # AUTH
#     path("api/auth/", include("accounts.urls")),

#     # LISTINGS
#     path("api/listings/", include("listings.urls")),

#     # PAYMENTS
#     path("api/payments/", include("payments.urls")),
# ]


# urlpatterns +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH
    path("api/auth/", include("accounts.urls")),

    # LISTINGS
    path("api/listings/", include("listings.urls")),

    # PAYMENTS
    path("api/payments/", include("payments.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

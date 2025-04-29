from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    # path('not-found/', views.custom_404_view),
    path('',views.home, name='home'), 
    path('about/',views.about, name='about'), 
    path('contact/',views.contact, name='contact'), 
    path('profile/',views.ProfileView.as_view(), name='profile'), 
    path('address/',views.address, name='address'), 
    path('update-address/<int:pk>',views.UpdateAddress.as_view(), name='update_address'), 
    path('add-to-cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('cart/',views.show_cart, name='cart'),

    path('change-password/',auth_view.PasswordChangeView.as_view(template_name='app/changePassword.html', 
    form_class=MyPasswordChangeForm, success_url='/password-change-done'), name='change_password'), 

    path('password-change-done/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordChangeDone.html'), name='password_change_done'), 
    path('category/<slug:val>',views.CategoryView.as_view(), name='category'),    
    path('category-title/<val>',views.CategoryTitle.as_view(), name='category-title'),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('registration/',views.CustomerRegistrationView.as_view(), name='registration'), 

    path('login/',auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'), 
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/passwordReset.html', 
    form_class=MyPasswordResetForm), name='password_reset'), 
    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/passwordResetConfirm.html', 
    form_class=MySetPasswordForm), name='password_reset_confirm'), 
    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/passwordResetComplete.html'), 
    name='password_reset_complete'), 
    path('password-reset-done/',auth_view.PasswordResetDoneView.as_view(template_name='app/passwordResetDone.html'), 
    name='password_reset_done'), 
    path('logout/',auth_view.LogoutView.as_view(next_page='login'), name='logout'), 
    path('cart/update/', views.UpdateCart.as_view(), name='update_cart_quantity'),
    path('search/', views.search_view, name='search_view'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# userform/forms.py
from django import forms
from django.core.exceptions import ValidationError
import re
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'age']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age'
            }),
        }
    
    def clean_name(self):
        """Custom validation for name field"""
        name = self.cleaned_data.get('name')
        if name:
            # Check if name contains only letters and spaces
            if not re.match(r'^[a-zA-Z\s]+$', name):
                raise ValidationError('Name should only contain letters and spaces.')
            
            # Check minimum length
            if len(name.strip()) < 2:
                raise ValidationError('Name must be at least 2 characters long.')
            
            # Check maximum length
            if len(name) > 100:
                raise ValidationError('Name cannot exceed 100 characters.')
                
        return name.strip().title()  # Return formatted name
    
    def clean_email(self):
        """Custom validation for email field"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                raise ValidationError('A user with this email already exists.')
        return email.lower()  # Return lowercase email
    
    def clean_phone(self):
        """Custom validation for phone field"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove all non-digit characters
            phone_digits = re.sub(r'\D', '', phone)
            
            # Check if phone number has valid length (10-15 digits)
            if len(phone_digits) < 10:
                raise ValidationError('Phone number must be at least 10 digits long.')
            if len(phone_digits) > 15:
                raise ValidationError('Phone number cannot exceed 15 digits.')
            
            # Format phone number
            if len(phone_digits) == 10:
                formatted_phone = f"({phone_digits[:3]}) {phone_digits[3:6]}-{phone_digits[6:]}"
            else:
                formatted_phone = phone_digits
            
            return formatted_phone
        return phone
    
    def clean_age(self):
        """Custom validation for age field"""
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 1:
                raise ValidationError('Age must be at least 1 year.')
            if age > 120:
                raise ValidationError('Please enter a valid age (maximum 120).')
        return age
    
    def clean(self):
        """Additional form-level validation"""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        age = cleaned_data.get('age')
        
        
        if age and age < 18 and name:
            
            pass
        
        return cleaned_data
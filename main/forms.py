from django import forms


class InputForm(forms.Form):
    coords_input= forms.CharField(
        widget=forms.TextInput(attrs={'size':50}), 
        label='Enter your data in any format:', max_length=100
        )    


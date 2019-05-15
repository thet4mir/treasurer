from django import forms
from .models import Drug, Order, Ordered_drug, Ordered_staff, Other_staff, Emchilgee, Drug_important, Onosh, History
from account.models import User, Worker, Costumer

class OrderForm(forms.ModelForm):

    worker = forms.ModelChoiceField(queryset=Worker.objects.filter(position__name = "Сувилагч"))

    class Meta:
        model = Order

        fields = [
            'ordered_date',
            'worker',
        ]
        widgets = {
            'ordered_date': forms.DateInput(attrs={"type": "date", 'class': 'form-control form-control-sm', 'read_only': 'read_only'}),
            'worker': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class Ordered_drugForm(forms.ModelForm):

    class Meta:
        model = Ordered_drug

        fields = [
            'drug',
            'qty',
        ]
        widgets = {
            'drug': forms.Select(attrs={'class': 'ordered_drug-fields form-control form-control-sm'}),
            'qty': forms.TextInput(attrs={'class': 'ordered_drug-fields form-control form-control-sm'}),
        }

class Ordered_staffForm(forms.ModelForm):
    class Meta:
        model = Ordered_staff

        fields = [
            'staff',
            'qty',
        ]
        widgets = {
            'staff': forms.Select(attrs={'class': 'ordered_staff-fields form-control form-control-sm'}),
            'qty': forms.TextInput(attrs={'class': 'ordered_staff-fields form-control form-control-sm'}),
        }

class OnoshForm(forms.ModelForm):
    class Meta:
        model = Onosh

        fields = [
            'category',
            'disc',
            'code',
        ]
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'disc': forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
            'code': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History

        fields = [
            'costumer',
            'doctor',
            'disc',
        ]
        widgets = {
            'costumer': forms.Select(attrs={'class': 'history-fields form-control form-control-sm'}),
            'doctor': forms.Select(attrs={'class': 'history-fields form-control form-control-sm'}),
            'disc': forms.TextInput(attrs={'class': 'history-fields form-control form-control-sm'}),
        }

class Emchilgee_form(forms.ModelForm):

    worker = forms.ModelChoiceField(queryset=Worker.objects.filter(position__name = "Сувилагч"))

    class Meta:
        model = Emchilgee

        fields = [
            'start_date',
            'end_date',
            'worker',
            'costumer',
            'onosh',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={"type": "date", 'class': 'form-control form-control-sm'}),
            'end_date': forms.DateInput(attrs={"type": "date", 'class': 'form-control form-control-sm'}),
            'worker': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'costumer': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'onosh': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }


class Drug_important_form(forms.ModelForm):
    class Meta:
        model = Drug_important

        fields = [
            'emchilgee_list',
            'name',
            'shirheg',
        ]
        widgets = {
            'emchilgee_list': forms.Select(attrs={'class': "drug_important-fields form-control form-control-sm"}),
            'name': forms.Select(attrs={'class': "drug_important-fields form-control form-control-sm"}),
            'shirheg': forms.TextInput(attrs={'class': "drug_important-fields form-control form-control-sm"}),
        }


class Drug_create_form(forms.ModelForm):
    class Meta:
        model = Drug

        fields = [
            'drug_code',
            'drug_name',
            'instructions',
            'serial_number',
            'producted_date',
            'hadgalah_hugatsaa',
            'uildver_ner',
            'sanuulga',
            'drug_type',
            'savalgaa',
            'hemjee',
            'helber',
            'storage_condition',
        ]
        widgets = {
            'drug_code':            forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'drug_name':            forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'instructions':         forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'serial_number':        forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'producted_date':       forms.DateInput(attrs={"type": "date", 'class': 'form-control form-control-sm'}),
            'hadgalah_hugatsaa':    forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'uildver_ner':          forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'sanuulga':             forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'drug_type':            forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'savalgaa':             forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'hemjee':               forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'helber':               forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'storage_condition':    forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

        labels = {
            'drug_code':            ('Эмийн код'),
            'drug_name':            ('Эмийн нэр'),
            'instructions':         ('Эмийн тухай'),
            'serial_number':        ('сериал дугаар'),
            'producted_date':       ('Үйлдвэрлэсэн он'),
            'hadgalah_hugatsaa':    ('Хадгалах хугацаа'),
            'uildver_ner':          ('Үйлдвэрийн нэр'),
            'sanuulga':             ('Санамж'),
            'drug_type':            ('Эмийн төрөл'),
            'savalgaa':             ('Савалгаа'),
            'hemjee':               ('Хэмжээ'),
            'helber':               ('Хэлбэр'),
            'storage_condition':    ('Хадгалах нөхцөл'),
        }

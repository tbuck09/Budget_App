from django import forms

from .models import Transaction


class TransactionCreateForm(forms.ModelForm):
    note = forms.CharField(
        required=False,
        max_length=10000,
        widget=forms.Textarea(
            attrs={
                "class": "text-box notes-text-box",
                "rows": 5
            }
        )
    )
    description = forms.CharField(max_length=120, required=False)

    class Meta:
        model = Transaction
        fields = [
            "amount",
            "category",
            "date",
            "description",
            "note"
        ]

    # Custom data validation measures
    # NOTE: clean_<item_name> must be literally the item name for this to work.
    # def clean_category(self, *args, **kwargs):
    #     category= self.cleaned_data.get("category")
    #     if "cool" in category.lower():
    #         return category
    #     else:
    #         raise forms.ValidationError("This category isn't cool enough. Do over, bruh.")


class RawTransactionCreateForm(forms.Form):
    date = forms.DateField(required=True)
    category = forms.CharField(max_length=50, required=True)
    amount = forms.DecimalField(required=True)
    description = forms.CharField(max_length=120, required=False)
    note = forms.CharField(
        required=False,
        max_length=10000,
        widget=forms.Textarea(
            attrs={
                "class": "text-box notes-text-box",
                "rows": 5
            }
        )
    )

# Date Picker
# https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
# class DateForm(forms.Form):
#     date = forms.DateTimeField(
#         format("%d/%m/%Y"),
#         widget=forms.DateTimeInput(attrs={
#             "class": "form-control datepicker-input datepicker-1",
#             "data_target": "#datetimepicker1"
#         })
#     )

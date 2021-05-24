from django import forms

class ReplaceWordCSVUploadForm(forms.Form):
    # formのname 属性が 'file' になる
    csv_file = forms.FileField(required=False, label='CSVから登録')
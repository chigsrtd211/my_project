from django import forms
from .models import PG_Facility_Master,PG_PostAds,PG_Facility,PG_Images, PG_Amenities, PG_Comments

class FacilityMasterCreationForm(forms.ModelForm):
    class Meta:
        model = PG_Facility_Master
        fields =('facility_name',)

# -------------------------------------------------------------------
class PGAmenitiesCreationForm(forms.ModelForm):
    class Meta:
        model = PG_Amenities
        fields = ('ac','wifi','laundry','attached_washroom','room_cleaning','washing_machine','full_water_supply','food','kitchen_appliances','parking','wardrobe','furnished_room','cctv_security','other')

#  -------------------------------------------------------------------

class PGCreationForm(forms.ModelForm):
    class Meta:
        model = PG_PostAds
        # fields = '__all__'
        fields = ('pg_name','avail_status','gender_preference','no_of_rooms','occupacy','price','description','pg_type','website','address','street','area','city','state','state','country','zipcode','profile_image','instructions_docs')

# -------------------------------------------------------------------

class FacilityCreationForm(forms.ModelForm):
    class Meta:
        model = PG_Facility
        fields = '__all__'

# -------------------------------------------------------------------

class PGImagesCreationForm(forms.ModelForm):
    class Meta:
        model = PG_Images
        fields = ('pg_images',)

# -------------------------------------------------------------------

class PGCommentsCreationForm(forms.ModelForm):
    class Meta:
        model = PG_Comments
        # fields = '__all__'
        fields = ('comment',)

# -------------------------------------------------------------------
class ContactOwnerForm(forms.Form):
    
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    
# -------------------------------------------------------------------

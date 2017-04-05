from django.core.exceptions import ValidationError 

#validation tweet field
def validate_content(value):
	content = value 
	if content == "abc":
		raise ValidationError("Content can't be ABC")
	return value
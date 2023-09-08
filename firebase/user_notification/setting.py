UN_doctype_user = "User"
UN_field_to_user = "email_id"

# Change on Doctype too
UN_field_un = "customer"

# Untuk pake apakah image yang dikirimkan ke applikasi menggunakkan full path dari image atau tidak
image_using_complete_url = True

def get_un_variabel(variable):
    if variable == "customer":
        return "user"
    if variable == "Customer":
        return "User"
    if variable == "tabCustomer":
        return "tabUser"
    if variable == "user":
        return "name"





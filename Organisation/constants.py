from enum import Enum

type_of_company = (('Govt', 'Govt'), ('Others', 'Others'))
deductor = (('Govt', 'Govt'), ('Union Govt', 'Union Govt'), ('LLP', 'LLP'), ('Partnership Firm', 'Partnership Firm'),
            ('OPC', 'OPC'), ('Section-8 Company', 'Section-8 Company'), ('Pvt Ltd', 'Pvt.Ltd'),
            ('Public Ltd', 'Public.Ltd'), ('Others', 'Others'))
gender = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))


class Messages(Enum):
    created = "{}, created successfully"
    updated = "{}, updated successfully"
    already_exist = "{}, already exist"
    deleted = "{}, deleted successfully"
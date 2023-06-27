from collections import UserDict
from datetime import datetime, timedelta 


N = 10


class Field:
    """Base class for fields in a record."""

    def __init__(self, value) -> None:
        self.__value = None        
        self.value = value

    @staticmethod
    def valid_value(value) -> bool:
        if value:
            return True
        return False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if self.valid_value(val):
            self.__value = val


class Name(Field):
    """Name field in a record."""


class Phone(Field):
    """Phone number field in a record."""

    @staticmethod
    def valid_value(value: str) -> bool:
        phone = ''.join(filter(str.isdigit, value))      
        if 8 < len(phone) < 13 and len(value) < 20:
            return True
        return False


class Birthday(Field):
    """Birthday field in a record."""

    @staticmethod
    def valid_value(birthday: datetime) -> bool:    
        if isinstance(birthday, datetime) and 0 < datetime.now().year - birthday.year <= 100:
            return True
        return False
    

class Record:
    """Record representing a contact in the address book."""

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        """
        Initialize a new record.

        Args:
            name (Name): The name of the contact.
            phone (Phone, optional): The phone number of the contact. Defaults to None.
        """

        self.name = name        
        self.phones = []
        if phone:        
            self.phones.append(phone)
        self.birthday = birthday    

    def days_to_birthday(self) -> int or None:
        """
        Calculate the number of days until the next birthday.

        Returns:
            int or None: The number of days until the next birthday, or None if the birthday is not set.
        """

        if self.birthday:
            current_date = datetime.now()        
            secelebration_birthday = datetime(current_date.year, self.birthday.value.month, self.birthday.value.day)        
            if current_date > secelebration_birthday:
                secelebration_birthday = datetime(current_date.year + 1, self.birthday.value.month, self.birthday.value.day)

            return (secelebration_birthday - current_date).days
        
        return None        

    def add_phone(self, phone: Phone) -> None:
        """
        Add a phone number to the record.

        Args:
            phone (Phone): The phone number to add.
        """
        try:
            if phone.value:
                self.phones.append(phone)
        except AttributeError:
            pass

    def remove_phone(self, phone: Phone) -> None:
        """
        Remove a phone number from the record.

        Args:
            phone (Phone): The phone number to remove.
        """

        for existing_phone in self.phones:
            if phone.value == existing_phone.value:
                self.phones.remove(existing_phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> None:
        """
        Edit a phone number in the record.

        Args:
            old_phone (Phone): The old phone number to replace.
            new_phone (Phone): The new phone number.
        """

        for idx, phone in enumerate(self.phones):
            if old_phone.value == phone.value:
                self.phones[idx] = new_phone


class AddressBook(UserDict):
    """Address book that extends UserDict."""

    def add_record(self, record: Record) -> None:
        """
        Add a record to the address book.

        Args:
            record (Record): The record to add.
        """

        self.data[record.name.value] = record

    def search(self, search_obj: object) -> str or list[str] or None:
        """
        Find a name by phone or a phone with a name in the address book.

        Args:
            search_obj: The search object representing either a Name or a Phone.

        Returns:
            Optional: The search results. If searching by Name, returns a list of phone numbers.
                If searching by Phone number, returns the name of the contact. Returns None if no match is found.
        """

        results = None

        if isinstance(search_obj, Name):
            for name, record in self.data.items():
                if search_obj.value == name:                    
                    results = list(map(lambda x: x.value, record.phones))

        elif isinstance(search_obj, Phone):
            for name, record in self.data.items():
                for phone in record.phones:
                    if search_obj.value == phone.value:
                        results = name

        return results    
   
    def __iter__(self):
        self.keys_iter = iter(self.data)
        return self 

    def __next__(self, n: int = N) -> str:
        """
        Get the next batch of records as a string representation.

        Args:
            n (int, optional): The number of records to retrieve. Defaults to N.

        Returns:
            str: The string representation of the next batch of records.
        """

        items = []
        try:
            for _ in range(n):
                key = next(self.keys_iter)
                items.append((key, self.data[key]))
        except StopIteration:
            if not items:
                raise StopIteration
            
        representation_record = '-' * 70 + '\n'
        representation_record += '|{:^33}|{:^20}|{:^13}|\n'.format("User", "Phones", "Birthday")
        representation_record += '-' * 70 + '\n'
        for name, user in items: 
            birthday = user.birthday.value.strftime("%d.%m.%Yp") if user.birthday else ''
            for i in range(len(user.phones)):                
                if i == 0:                    
                    representation_record += '| {:<32}|{:>19} |{:^13}|\n'.format(name, user.phones[i].value, birthday)
                else:
                    representation_record += '|{:<33}|{:>19} |{:^13}|\n'.format(' ', user.phones[i].value, ' ')
            if not user.phones:               
                representation_record += '| {:<32}|{:>19} |{:^13}|\n'.format(name, ' ', birthday)
            representation_record += '-' * 70 + '\n'
            

        return representation_record

 
if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name, phone)
    rec.add_phone(Phone('+38(098)765-43-31'))
    ab = AddressBook()
    ab.add_record(rec)
    
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)  
    assert ab['Bill'].phones[0].value == '1234567890'
    
    print('All Ok)')
    

    ab.add_record(Record(Name('John Doe'), Phone('4567891232'), Birthday(datetime(1991, 8, 24))))

    itr = iter(ab) 
    print(next(itr))

    print(ab['John Doe'].days_to_birthday())
    print(ab['Bill'].days_to_birthday())


    
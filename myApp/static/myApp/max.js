function formatPhoneNumber(value, event) {
      if (event.key < '0' || event.key > '9') {
        event.preventDefault();
        return value;
      }
      if (!value) return value;
      const phoneNumber = value.replace(/[^\d]/g, '');
      const phoneNumberLength = phoneNumber.length;
      if (phoneNumberLength < 4) return phoneNumber;
      if (phoneNumberLength < 7) {
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
      }
      return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 9)}`;
    }

    function phoneNumberFormatter(inputField, event) {
      if (event.key === 'Backspace') {
        // Allow the Backspace key event to delete characters
        return;
      }

      const currentValue = inputField.value;
      const formattedInputValue = formatPhoneNumber(currentValue, event);
      inputField.value = formattedInputValue;
    }


function removeNonNumeric() {
  var phoneNumberInput = document.getElementById('id_phoneNumber');
  phoneNumberInput.value = phoneNumberInput.value.replace(/\D/g, '');
}
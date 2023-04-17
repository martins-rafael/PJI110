function confirmDelete(form) {
  form.addEventListener('submit', event => {
    const confirmation = confirm('Tem certeza que deseja excluir? Essa operação não poderá ser desfeita!');

    if (!confirmation) {
      event.preventDefault();
    }
  })
}

function errorsNotAllowed(form) {
  form.addEventListener('submit', event => {
    const error = document.querySelector('.error');

    if (error) {
      event.preventDefault();
      alert('Por favor corrija todos os erros.');
    }
  })
}

const formValidate = document.querySelector('.form-validate');
const formsDelete = document.querySelectorAll('.form-delete');

if (formsDelete) {
  formsDelete.forEach(form => confirmDelete(form));
}

if (formValidate) {
  errorsNotAllowed(formValidate);
}

const Mask = {
  apply(input, func) {
    setTimeout(() => {
      input.value = Mask[func](input.value);
    }, 1);
  },
  rg(value) {
    value = value.replace(/\D/g, '');

    value = value.replace(/(\d{2})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1-$2');

    if (value.length > 12) {
      value = value.slice(0, -1);
    }

    return value;
  },
  cpf(value) {
    value = value.replace(/\D/g, '');

    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1-$2');

    if (value.length > 14) {
      value = value.slice(0, -1);
    }

    return value;
  }
};

const Validate = {
  apply(input, func) {
    Validate.clearErrors(input);

    let results = Validate[func](input.value);
    input.value = results.value;

    if (results.error) {
      Validate.displayError(input, results.error)
    }
  },
  displayError(input, error) {
    const div = document.createElement('div');
    div.classList.add('error');
    div.classList.add('badge');
    div.classList.add('rounded-pill');
    div.classList.add('bg-danger');
    div.classList.add('mt-2');
    div.innerHTML = error;
    input.parentNode.appendChild(div);

  },
  clearErrors(input) {
    const errorDiv = input.parentNode.querySelector('.error');
    if (errorDiv) {
      errorDiv.remove();
    }
  },
  isCpf(value) {
    let error = null;
    const cleanValues = value.replace(/\D/g, '');

    if (cleanValues.length !== 11) {
      error = 'CPF incorreto, o CPF deve conter 11 números';
    }

    return {
      error,
      value
    };
  },
  isRg(value) {
    let error = null;
    const cleanValues = value.replace(/\D/g, '');

    if (cleanValues.length !== 9) {
      error = 'RG incorreto, o RG deve conter 9 números';
    }

    return {
      error,
      value
    };
  },
  passwordLength(value) {
    let error = null;

    if (value.trim() === '') {
      error = 'A senha não pode conter apenas espaços';
    }

    if (value.length < 6) {
      error = 'A senha deve conter no mínimo 6 caracteres';
    }

    return {
      error,
      value
    };
  },
  isEmail(value) {
    let error = null;
    const mailFormat = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;

    if (!value.match(mailFormat)) {
      error = 'Email inválido';
    }

    return {
      error,
      value
    };
  }
}
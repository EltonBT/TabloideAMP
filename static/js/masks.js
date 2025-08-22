/**
 * Máscaras para formatação de campos de formulário
 * Aplica formatação automática em tempo real para CPF, CNPJ, telefone e CEP
 */

document.addEventListener('DOMContentLoaded', function() {
    // Aplicar máscaras baseadas no atributo data-mask
    const maskedFields = document.querySelectorAll('[data-mask]');
    
    maskedFields.forEach(function(field) {
        const maskType = field.getAttribute('data-mask');
        
        switch(maskType) {
            case 'cpf':
                applyCPFMask(field);
                break;
            case 'cnpj':
                applyCNPJMask(field);
                break;
            case 'telefone':
                applyPhoneMask(field);
                break;
            case 'cep':
                applyCEPMask(field);
                break;
        }
    });
});

// Função para remover caracteres não numéricos
function removeNonNumeric(value) {
    return value.replace(/\D/g, '');
}

// Máscara para CPF (000.000.000-00)
function applyCPFMask(field) {
    field.addEventListener('input', function(e) {
        let value = removeNonNumeric(e.target.value);
        
        if (value.length <= 11) {
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        }
        
        e.target.value = value;
    });
    
    // Validação básica de CPF
    field.addEventListener('blur', function(e) {
        const cpf = removeNonNumeric(e.target.value);
        if (cpf.length === 11 && !isValidCPF(cpf)) {
            showFieldError(e.target, 'CPF inválido');
        } else {
            clearFieldError(e.target);
        }
    });
}

// Máscara para CNPJ (00.000.000/0000-00)
function applyCNPJMask(field) {
    field.addEventListener('input', function(e) {
        let value = removeNonNumeric(e.target.value);
        
        if (value.length <= 14) {
            value = value.replace(/(\d{2})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1.$2');
            value = value.replace(/(\d{3})(\d)/, '$1/$2');
            value = value.replace(/(\d{4})(\d{1,2})$/, '$1-$2');
        }
        
        e.target.value = value;
    });
    
    // Validação básica de CNPJ
    field.addEventListener('blur', function(e) {
        const cnpj = removeNonNumeric(e.target.value);
        if (cnpj.length === 14 && !isValidCNPJ(cnpj)) {
            showFieldError(e.target, 'CNPJ inválido');
        } else {
            clearFieldError(e.target);
        }
    });
}

// Máscara para telefone (00) 00000-0000 ou (00) 0000-0000
function applyPhoneMask(field) {
    field.addEventListener('input', function(e) {
        let value = removeNonNumeric(e.target.value);
        
        if (value.length <= 11) {
            if (value.length <= 10) {
                // Telefone fixo: (00) 0000-0000
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{4})(\d)/, '$1-$2');
            } else {
                // Celular: (00) 00000-0000
                value = value.replace(/(\d{2})(\d)/, '($1) $2');
                value = value.replace(/(\d{5})(\d)/, '$1-$2');
            }
        }
        
        e.target.value = value;
    });
}

// Máscara para CEP (00000-000)
function applyCEPMask(field) {
    field.addEventListener('input', function(e) {
        let value = removeNonNumeric(e.target.value);
        
        if (value.length <= 8) {
            value = value.replace(/(\d{5})(\d)/, '$1-$2');
        }
        
        e.target.value = value;
    });
    
    // Busca automática de endereço via CEP (ViaCEP API)
    field.addEventListener('blur', function(e) {
        const cep = removeNonNumeric(e.target.value);
        if (cep.length === 8) {
            fetchAddressByCEP(cep);
        }
    });
}

// Validação de CPF
function isValidCPF(cpf) {
    // Elimina CPFs inválidos conhecidos
    if (cpf.length !== 11 || 
        cpf === '00000000000' ||
        cpf === '11111111111' ||
        cpf === '22222222222' ||
        cpf === '33333333333' ||
        cpf === '44444444444' ||
        cpf === '55555555555' ||
        cpf === '66666666666' ||
        cpf === '77777777777' ||
        cpf === '88888888888' ||
        cpf === '99999999999') {
        return false;
    }
    
    // Valida 1º dígito
    let add = 0;
    for (let i = 0; i < 9; i++) {
        add += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let rev = 11 - (add % 11);
    if (rev === 10 || rev === 11) rev = 0;
    if (rev !== parseInt(cpf.charAt(9))) return false;
    
    // Valida 2º dígito
    add = 0;
    for (let i = 0; i < 10; i++) {
        add += parseInt(cpf.charAt(i)) * (11 - i);
    }
    rev = 11 - (add % 11);
    if (rev === 10 || rev === 11) rev = 0;
    if (rev !== parseInt(cpf.charAt(10))) return false;
    
    return true;
}

// Validação de CNPJ
function isValidCNPJ(cnpj) {
    if (cnpj.length !== 14) return false;
    
    // Elimina CNPJs inválidos conhecidos
    if (cnpj === '00000000000000' ||
        cnpj === '11111111111111' ||
        cnpj === '22222222222222' ||
        cnpj === '33333333333333' ||
        cnpj === '44444444444444' ||
        cnpj === '55555555555555' ||
        cnpj === '66666666666666' ||
        cnpj === '77777777777777' ||
        cnpj === '88888888888888' ||
        cnpj === '99999999999999') {
        return false;
    }
    
    // Valida DVs
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;
    
    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }
    
    let resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(0))) return false;
    
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;
    
    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }
    
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado !== parseInt(digitos.charAt(1))) return false;
    
    return true;
}

// Busca endereço por CEP usando a API ViaCEP
function fetchAddressByCEP(cep) {
    if (cep.length !== 8) return;
    
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                // Preenche campos de endereço automaticamente se existirem
                const enderecoField = document.querySelector('[name="endereco"]');
                const cidadeField = document.querySelector('[name="cidade"]');
                const ufField = document.querySelector('[name="uf"]');
                
                if (enderecoField && data.logradouro) {
                    enderecoField.value = data.logradouro;
                }
                
                if (cidadeField && data.localidade) {
                    cidadeField.value = data.localidade;
                }
                
                if (ufField && data.uf) {
                    ufField.value = data.uf;
                }
            }
        })
        .catch(error => {
            console.log('Erro ao buscar CEP:', error);
        });
}

// Função para mostrar erro no campo
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

// Função para limpar erro do campo
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}